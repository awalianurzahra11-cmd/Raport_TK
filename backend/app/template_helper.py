import os
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REACT_INDEX = os.path.join(BASE_DIR, "frontend-react", "dist", "index.html")

class SafeTemplates:
    def __init__(self, directory=None):
        self.directory = directory
        self.jinja = None
        if directory and os.path.exists(directory):
            try:
                self.jinja = Jinja2Templates(directory=directory)
            except Exception:
                self.jinja = None

    def TemplateResponse(self, request, name, context=None, **kwargs):
        if self.jinja and os.path.exists(os.path.join(self.directory, name)):
            try:
                return self.jinja.TemplateResponse(request, name, context, **kwargs)
            except Exception:
                pass

        if os.path.exists(REACT_INDEX):
            return FileResponse(REACT_INDEX)

        error = (context or {}).get("error")
        if error:
            return RedirectResponse(f"/login?error={error}", status_code=302)

        return HTMLResponse("<!doctype html><html><head><meta charset='utf-8'></head><body><div id='root'></div></body></html>")
