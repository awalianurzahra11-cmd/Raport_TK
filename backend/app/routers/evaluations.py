import os
import json
from datetime import datetime
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.app.template_helper import SafeTemplates
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.database import get_db
from backend.app.models import InputPenilaian, Siswa, Pengguna, Evaluation, Student, User
from backend.app.auth.jwt import decode_access_token
from backend.app.services.indicators import INDICATORS
from backend.app.services.evaluation_calculator import calculate_evaluation

templates_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "frontend", "templates"
)
templates = SafeTemplates(directory=templates_dir)

router = APIRouter(prefix="/evaluations")


def get_token_from_request(request: Request) -> Optional[str]:
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
    return token


def _get_user(req_or_token, db: Session):
    if isinstance(req_or_token, Request):
        token = get_token_from_request(req_or_token)
    elif isinstance(req_or_token, str):
        token = req_or_token
    else:
        token = None
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    return db.query(User).filter(User.id == int(payload["sub"])).first()


@router.get("/add", response_class=HTMLResponse)
async def evaluation_add_page(request: Request, db: Session = Depends(get_db), student_id: Optional[int] = None):
    user = _get_user(request, db)
    if not user:
        return RedirectResponse(url="/login")
    if user.role != "admin":
        return RedirectResponse(url="/dashboard")

    students = db.query(Student).order_by(Student.name).all()
    
    # Pre-select student and retrieve class & diagnosa
    preselected_student = None
    if student_id:
        preselected_student = db.query(Student).filter(Student.id == student_id).first()

    from datetime import date
    current_date = date.today().strftime('%Y-%m-%d')

    return templates.TemplateResponse(
        request, "evaluations/form.html",
        {
            "user": user,
            "students": students,
            "preselect_student_id": student_id,
            "preselected_student": preselected_student,
            "indicators": INDICATORS,
            "current_date": current_date
        }
    )


@router.post("/add")
async def evaluation_add(
    request: Request,
    student_id: int = Form(...),
    date_str: str = Form(..., alias="date"),
    class_name: str = Form(""),
    diagnosa: str = Form(""),
    db: Session = Depends(get_db),
):
    user = _get_user(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")

    form_data = await request.form()
    result = calculate_evaluation(form_data)

    eval_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    evaluation = Evaluation(
        student_id=student_id,
        date=eval_date,
        class_name=class_name or None,
        diagnosa=diagnosa or None,
        scores=json.dumps(result["scores"]),
        avg_cognitive=result["avg_cognitive"],
        avg_motoric=result["avg_motoric"],
        avg_language=result["avg_language"],
        avg_social=result["avg_social"],
        avg_independence=result["avg_independence"],
        composite_index=result["composite_index"],
        index_percentage=result["index_percentage"],
        predicate=result["predicate"]
    )
    
    db.add(evaluation)
    
    # Update student's profile class & diagnosis to reflect the latest evaluation if necessary
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        if class_name:
            student.class_name = class_name
        if diagnosa:
            student.special_needs = diagnosa
            
    db.commit()
    
    return RedirectResponse(url="/evaluations/rekap?student_id=" + str(student_id) + "&msg=Penilaian+kuantitatif+berhasil+disimpan", status_code=302)


@router.get("/rekap", response_class=HTMLResponse)
async def evaluation_rekap(request: Request, student_id: Optional[int] = None, db: Session = Depends(get_db)):
    user = _get_user(request, db)
    if not user:
        return RedirectResponse(url="/login")
    if user.role != "admin":
        return RedirectResponse(url="/dashboard")

    students = db.query(Student).order_by(Student.name).all()
    
    # If no student selected, pick the first one if available
    selected_student_id = student_id
    if not selected_student_id and students:
        selected_student_id = students[0].id
        
    selected_student = None
    history = []
    comparison_data = []
    
    # Data structures for Chart.js
    chart_dates = []
    chart_composite = []
    chart_cog = []
    chart_mot = []
    chart_lang = []
    chart_soc = []
    chart_ind = []
    
    # Comparison comparison trends
    comparison_trend = []
    
    if selected_student_id:
        selected_student = db.query(Student).filter(Student.id == selected_student_id).first()
        history = db.query(Evaluation).filter(Evaluation.student_id == selected_student_id).order_by(Evaluation.date.asc()).all()
        
        for ev in history:
            chart_dates.append(ev.date.strftime("%d %b %Y"))
            chart_composite.append(ev.composite_index)
            chart_cog.append(round(ev.avg_cognitive, 2))
            chart_mot.append(round(ev.avg_motoric, 2))
            chart_lang.append(round(ev.avg_language, 2))
            chart_soc.append(round(ev.avg_social, 2))
            chart_ind.append(round(ev.avg_independence, 2))

        # Check if there are at least 2 evaluations for comparison
        if len(history) >= 2:
            last_ev = history[-1]
            prev_ev = history[-2]
            
            domains = [
                ("Kognitif", last_ev.avg_cognitive, prev_ev.avg_cognitive),
                ("Motorik", last_ev.avg_motoric, prev_ev.avg_motoric),
                ("Bahasa & Komunikasi", last_ev.avg_language, prev_ev.avg_language),
                ("Sosial-Emosional", last_ev.avg_social, prev_ev.avg_social),
                ("Kemandirian", last_ev.avg_independence, prev_ev.avg_independence),
            ]
            
            for name, curr, prev in domains:
                diff = curr - prev
                if diff > 0:
                    status = "naik"
                elif diff < 0:
                    status = "turun"
                else:
                    status = "stabil"
                comparison_trend.append({
                    "name": name,
                    "prev": round(prev, 2),
                    "curr": round(curr, 2),
                    "diff": round(abs(diff), 2),
                    "status": status
                })

    # Cross-student comparison table
    # Get the latest evaluation for each student
    for s in students:
        latest_ev = db.query(Evaluation).filter(Evaluation.student_id == s.id).order_by(Evaluation.date.desc()).first()
        comparison_data.append({
            "student": s,
            "latest_evaluation": latest_ev
        })

    return templates.TemplateResponse(
        request, "evaluations/rekap.html",
        {
            "user": user,
            "students": students,
            "selected_student_id": selected_student_id,
            "selected_student": selected_student,
            "history": history[::-1], # newest first for table view
            "comparison_data": comparison_data,
            "comparison_trend": comparison_trend,
            
            # Chart inputs (JSON strings for JS)
            "chart_dates": json.dumps(chart_dates),
            "chart_composite": json.dumps(chart_composite),
            "chart_cog": json.dumps(chart_cog),
            "chart_mot": json.dumps(chart_mot),
            "chart_lang": json.dumps(chart_lang),
            "chart_soc": json.dumps(chart_soc),
            "chart_ind": json.dumps(chart_ind),
        }
    )


@router.get("/{eval_id}/delete")
async def evaluation_delete(eval_id: int, request: Request, db: Session = Depends(get_db)):
    user = _get_user(request, db)
    if not user or user.role != "admin":
        return RedirectResponse(url="/login")
    
    evaluation = db.query(Evaluation).filter(Evaluation.id == eval_id).first()
    student_id = None
    if evaluation:
        student_id = evaluation.student_id
        db.delete(evaluation)
        db.commit()
        
    url = "/evaluations/rekap"
    if student_id:
        url += "?student_id=" + str(student_id) + "&msg=Penilaian+kuantitatif+berhasil+dihapus"
    else:
        url += "?msg=Penilaian+kuantitatif+berhasil+dihapus"
    return RedirectResponse(url=url, status_code=302)


# ── Evaluation REST API Endpoints ─────────────────────────────────────────────

from pydantic import BaseModel, Field
from typing import Dict

@router.get("/api/indicators")
async def api_get_indicators(request: Request, db: Session = Depends(get_db)):
    user = _get_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated or not an admin")
    return INDICATORS


class EvaluationCreateAPISchema(BaseModel):
    student_id: int
    date: str
    class_name: Optional[str] = ""
    diagnosa: Optional[str] = ""
    scores: Dict[str, int] = Field(..., description="Map of indicator item IDs to score values (1-4)")


@router.post("/api/add")
async def api_evaluation_add(
    request: Request,
    eval_data: EvaluationCreateAPISchema,
    db: Session = Depends(get_db)
):
    user = _get_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated or not an admin")
        
    result = calculate_evaluation(eval_data.scores)

    try:
        eval_date = datetime.strptime(eval_data.date, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400, detail="Format tanggal salah (harus YYYY-MM-DD)")

    evaluation = Evaluation(
        student_id=eval_data.student_id,
        date=eval_date,
        class_name=eval_data.class_name or None,
        diagnosa=eval_data.diagnosa or None,
        scores=json.dumps(result["scores"]),
        avg_cognitive=result["avg_cognitive"],
        avg_motoric=result["avg_motoric"],
        avg_language=result["avg_language"],
        avg_social=result["avg_social"],
        avg_independence=result["avg_independence"],
        composite_index=result["composite_index"],
        index_percentage=result["index_percentage"],
        predicate=result["predicate"]
    )
    db.add(evaluation)
    
    # Update student profile
    student = db.query(Student).filter(Student.id == eval_data.student_id).first()
    if student:
        if eval_data.class_name:
            student.class_name = eval_data.class_name
        if eval_data.diagnosa:
            student.special_needs = eval_data.diagnosa
            
    db.commit()
    return {"status": "success", "message": "Penilaian kuantitatif BK berhasil disimpan", "id": evaluation.id}


@router.get("/api/rekap")
async def api_evaluation_rekap(request: Request, student_id: Optional[int] = None, db: Session = Depends(get_db)):
    user = _get_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated or not an admin")

    students = db.query(Student).order_by(Student.name).all()
    selected_student_id = student_id
    if not selected_student_id and students:
        selected_student_id = students[0].id
        
    selected_student = None
    history = []
    comparison_trend = []
    
    chart_dates = []
    chart_composite = []
    chart_cog = []
    chart_mot = []
    chart_lang = []
    chart_soc = []
    chart_ind = []
    
    if selected_student_id:
        selected_student = db.query(Student).filter(Student.id == selected_student_id).first()
        history = db.query(Evaluation).filter(Evaluation.student_id == selected_student_id).order_by(Evaluation.date.asc()).all()
        
        for ev in history:
            chart_dates.append(ev.date.strftime("%d %b %Y"))
            chart_composite.append(ev.composite_index)
            chart_cog.append(round(ev.avg_cognitive, 2))
            chart_mot.append(round(ev.avg_motoric, 2))
            chart_lang.append(round(ev.avg_language, 2))
            chart_soc.append(round(ev.avg_social, 2))
            chart_ind.append(round(ev.avg_independence, 2))

        if len(history) >= 2:
            last_ev = history[-1]
            prev_ev = history[-2]
            
            domains = [
                ("Kognitif", last_ev.avg_cognitive, prev_ev.avg_cognitive),
                ("Motorik", last_ev.avg_motoric, prev_ev.avg_motoric),
                ("Bahasa & Komunikasi", last_ev.avg_language, prev_ev.avg_language),
                ("Sosial-Emosional", last_ev.avg_social, prev_ev.avg_social),
                ("Kemandirian", last_ev.avg_independence, prev_ev.avg_independence),
            ]
            
            for name, curr, prev in domains:
                diff = curr - prev
                status = "naik" if diff > 0 else "turun" if diff < 0 else "stabil"
                comparison_trend.append({
                    "name": name,
                    "prev": round(prev, 2),
                    "curr": round(curr, 2),
                    "diff": round(abs(diff), 2),
                    "status": status
                })

    comparison_data = []
    for s in students:
        latest_ev = db.query(Evaluation).filter(Evaluation.student_id == s.id).order_by(Evaluation.date.desc()).first()
        comparison_data.append({
            "student_id": s.id,
            "student_name": s.name,
            "class_name": s.class_name,
            "special_needs": s.special_needs,
            "latest_evaluation": {
                "id": latest_ev.id,
                "date": latest_ev.date.isoformat(),
                "composite_index": latest_ev.composite_index,
                "predicate": latest_ev.predicate,
                "avg_cognitive": latest_ev.avg_cognitive,
                "avg_motoric": latest_ev.avg_motoric,
                "avg_language": latest_ev.avg_language,
                "avg_social": latest_ev.avg_social,
                "avg_independence": latest_ev.avg_independence
            } if latest_ev else None
        })

    history_json = [
        {
            "id": ev.id,
            "date": ev.date.isoformat(),
            "class_name": ev.class_name,
            "diagnosa": ev.diagnosa,
            "avg_cognitive": round(ev.avg_cognitive, 2),
            "avg_motoric": round(ev.avg_motoric, 2),
            "avg_language": round(ev.avg_language, 2),
            "avg_social": round(ev.avg_social, 2),
            "avg_independence": round(ev.avg_independence, 2),
            "composite_index": ev.composite_index,
            "index_percentage": ev.index_percentage,
            "predicate": ev.predicate
        }
        for ev in reversed(history)
    ]

    return {
        "selected_student_id": selected_student_id,
        "selected_student": {
            "id": selected_student.id,
            "name": selected_student.name,
            "class_name": selected_student.class_name,
            "special_needs": selected_student.special_needs
        } if selected_student else None,
        "history": history_json,
        "comparison_trend": comparison_trend,
        "comparison_data": comparison_data,
        "chart_data": {
            "dates": chart_dates,
            "composite": chart_composite,
            "cognitive": chart_cog,
            "motoric": chart_mot,
            "language": chart_lang,
            "social": chart_soc,
            "independence": chart_ind
        }
    }


@router.api_route("/api/delete/{eval_id}", methods=["DELETE", "POST"])
async def api_evaluation_delete(eval_id: int, request: Request, db: Session = Depends(get_db)):
    user = _get_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=401, detail="Not authenticated or not an admin")
        
    evaluation = db.query(Evaluation).filter(Evaluation.id == eval_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Penilaian kuantitatif tidak ditemukan")
        
    db.delete(evaluation)
    db.commit()
    return {"status": "success", "message": "Penilaian kuantitatif berhasil dihapus"}
