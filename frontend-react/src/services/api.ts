import type { Pengguna, Siswa, PerkembanganHarian, Raport, InputPenilaian, GaleriKegiatan, DataDashboard } from '../types';

// Helper to parse HTML string if fallback is needed
function parseHTML(html: string): Document {
  const parser = new DOMParser();
  return parser.parseFromString(html, 'text/html');
}

// Central fetch wrapper that guarantees credentials (cookies) and Bearer token are ALWAYS sent
async function authFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const token = localStorage.getItem('rapor_tk_token');
  const headers = new Headers(options.headers || {});
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  const finalOptions: RequestInit = {
    ...options,
    headers,
    credentials: 'include', // <-- Ensures access_token cookie is always transmitted!
  };
  return fetch(url, finalOptions);
}

// Decode stored user from localStorage or cookie
export function getStoredUser(): { id: number; name: string; email: string; role: 'admin' | 'pendamping' } | null {
  try {
    const local = localStorage.getItem('rapor_tk_user');
    if (local) {
      const parsed = JSON.parse(local);
      if (parsed && parsed.id && parsed.email) {
        return parsed;
      }
    }
  } catch (e) {}

  const token = localStorage.getItem('rapor_tk_token') || (() => {
    const match = document.cookie.match(new RegExp('(^| )access_token=([^;]+)'));
    return match ? match[2] : null;
  })();

  if (!token) return null;
  try {
    const payloadBase64 = token.split('.')[1];
    const decoded = JSON.parse(atob(payloadBase64));
    if (!decoded || !decoded.sub) return null;
    return {
      id: Number(decoded.id || decoded.sub),
      name: decoded.name || '',
      email: decoded.email || '',
      role: decoded.role as 'admin' | 'pendamping',
    };
  } catch (e) {
    return null;
  }
}

export const api = {
  // ── AUTH ────────────────────────────────────────────────────────
  async login(email: string, pin: string) {
    try {
      const res = await authFetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.trim(), password: pin.trim() }),
      });

      const data = await res.json().catch(() => null);

      if (res.ok && data && data.status === 'success' && data.user) {
        if (data.token) {
          localStorage.setItem('rapor_tk_token', data.token);
        }
        localStorage.setItem('rapor_tk_user', JSON.stringify(data.user));
        return { success: true, user: data.user };
      }

      if (data && data.detail) {
        return { success: false, error: data.detail };
      }
    } catch (e: any) {
      return { success: false, error: e.message || 'Tidak dapat terhubung ke server backend.' };
    }

    return { success: false, error: 'Email atau PIN salah.' };
  },

  async logout() {
    localStorage.removeItem('rapor_tk_user');
    localStorage.removeItem('rapor_tk_token');
    try {
      await authFetch('/api/auth/logout', { method: 'POST' });
    } catch (e) {}
  },

  async checkAuth() {
    try {
      const res = await authFetch('/api/auth/me');
      if (res.ok) {
        const user = await res.json();
        localStorage.setItem('rapor_tk_user', JSON.stringify(user));
        return user;
      }
      if (res.status === 401) {
        localStorage.removeItem('rapor_tk_user');
        localStorage.removeItem('rapor_tk_token');
        return null;
      }
    } catch (e) {}

    // Jika token lokal masih valid di JWT decode dan server tidak menolak 401
    const stored = getStoredUser();
    if (stored && stored.id && stored.email && localStorage.getItem('rapor_tk_token')) {
      return stored;
    }

    localStorage.removeItem('rapor_tk_user');
    localStorage.removeItem('rapor_tk_token');
    return null;
  },

  // ── DASHBOARD ──────────────────────────────────────────────────
  async getDashboard() {
    const res = await authFetch('/api/dashboard');
    if (!res.ok) {
      if (res.status === 401) {
        localStorage.removeItem('rapor_tk_user');
        localStorage.removeItem('rapor_tk_token');
        throw new Error('Sesi login telah berakhir. Silakan login kembali.');
      }
      throw new Error(`Gagal memuat data dashboard (status ${res.status})`);
    }

    const data = await res.json();
    return {
      total_students: data.total_students ?? 0,
      total_reports_today: data.total_reports_today ?? 0,
      total_assessments: data.total_assessments ?? 0,
      total_graded_students: data.total_graded_students ?? 0,
      total_gallery_items: data.total_gallery_items ?? 0,
      recent_reports: (data.recent_reports || []).map((r: any) => ({
        id: r.id,
        student_name: r.student_name || 'Siswa',
        date: r.date || '',
        notes: r.notes || '',
      })),
      chart_data: {
        bar: {
          labels: data.chart_data?.bar?.labels || [],
          data: data.chart_data?.bar?.data || [],
        },
        line: {
          labels: data.chart_data?.line?.labels || [],
          data: data.chart_data?.line?.data || [],
        },
      },
    };
  },

  // ── STUDENTS ────────────────────────────────────────────────────
  async getStudents(q: string = '') {
    try {
      const url = q ? `/students/api/list?q=${encodeURIComponent(q)}` : '/students/api/list';
      const res = await authFetch(url);
      if (res.ok) {
        return await res.json();
      }
      if (res.status === 401) {
        localStorage.removeItem('rapor_tk_user');
        localStorage.removeItem('rapor_tk_token');
      }
    } catch (e) {}
    return [];
  },

  async getStudent(id: number) {
    try {
      const res = await authFetch(`/students/api/detail/${id}`);
      if (res.ok) {
        const data = await res.json();
        return data.student || data;
      }
      if (res.status === 401) {
        localStorage.removeItem('rapor_tk_user');
        localStorage.removeItem('rapor_tk_token');
      }
    } catch (e) {}
    return null;
  },

  async getTeachers(): Promise<{ id: number; name: string; email: string }[]> {
    try {
      const res = await authFetch('/students/api/teachers');
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {}

    try {
      const res = await authFetch('/api/users');
      if (res.ok) {
        const users = await res.json();
        return users.filter((u: any) => u.role === 'pendamping');
      }
    } catch (e) {}

    return [];
  },

  async addStudent(data: { name: string; birth_date: string; class_name: string; special_needs: string; teacher_id?: number }) {
    // 1. Try REST API
    try {
      const res = await authFetch('/students/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) return true;
    } catch (e) {}

    // 2. Fallback to Form URL-Encoded (backend-fix pure)
    const params = new URLSearchParams();
    params.append('name', data.name);
    params.append('birth_date', data.birth_date);
    params.append('class_name', data.class_name || '');
    params.append('special_needs', data.special_needs || '');
    if (data.teacher_id) params.append('teacher_id', String(data.teacher_id));

    const res = await authFetch('/students/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async editStudent(id: number, data: { name: string; birth_date: string; class_name: string; special_needs: string; teacher_id?: number }) {
    try {
      const res = await authFetch(`/students/api/edit/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    params.append('name', data.name);
    params.append('birth_date', data.birth_date);
    params.append('class_name', data.class_name || '');
    params.append('special_needs', data.special_needs || '');
    if (data.teacher_id) params.append('teacher_id', String(data.teacher_id));

    const res = await authFetch(`/students/${id}/edit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async deleteStudent(id: number) {
    try {
      const res = await authFetch(`/students/api/delete/${id}`, { method: 'POST' });
      if (res.ok) return true;
    } catch (e) {}
    const res = await authFetch(`/students/${id}/delete`);
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  // ── DAILY REPORTS ───────────────────────────────────────────────
  async getDailyReports(studentId?: number) {
    try {
      const url = studentId ? `/daily-reports/api/list?student_id=${studentId}` : '/daily-reports/api/list';
      const res = await authFetch(url);
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {}

    const url = studentId ? `/daily-reports?student_id=${studentId}` : '/daily-reports';
    const res = await authFetch(url);
    const html = await res.text();
    const doc = parseHTML(html);

    const reports: any[] = [];
    doc.querySelectorAll('.grid > div.card, .space-y-4 > div.card, .card').forEach(card => {
      const titleEl = card.querySelector('.card-title, h3, .font-bold');
      const studentName = titleEl?.textContent?.trim() || '';
      const dateEl = card.querySelector('.badge-ghost, .text-slate-400');
      const date = dateEl?.textContent?.trim() || '';
      const notes = card.querySelector('p')?.textContent?.trim() || '';
      const editLink = card.querySelector('a[href^="/daily-reports/"]')?.getAttribute('href');
      const idMatch = editLink?.match(/\/daily-reports\/(\d+)/);
      const id = idMatch ? Number(idMatch[1]) : 0;

      if (id) {
        reports.push({
          id,
          student_id: studentId || 0,
          student_name: studentName,
          date,
          notes,
          behavior: '',
          social_interaction: '',
        });
      }
    });
    return reports;
  },

  async getDailyReport(id: number) {
    try {
      const reports = await this.getDailyReports();
      const found = reports.find((r: any) => r.id === id);
      if (found) {
        return {
          id: found.id,
          student_id: found.student_id,
          report_date: found.date,
          notes: found.notes,
          behavior: found.behavior,
          social_interaction: found.social_interaction,
        };
      }
    } catch (e) {}

    const res = await authFetch(`/daily-reports/${id}/edit`);
    const html = await res.text();
    const doc = parseHTML(html);

    const studentSelect = doc.querySelector('select#student_id') as HTMLSelectElement;
    const studentId = Number(studentSelect?.value) || 0;
    const reportDate = (doc.querySelector('input#report_date') as HTMLInputElement)?.value || '';
    const notes = (doc.querySelector('textarea#notes') as HTMLTextAreaElement)?.value || '';
    const behavior = (doc.querySelector('textarea#behavior') as HTMLTextAreaElement)?.value || '';
    const socialInteraction = (doc.querySelector('textarea#social_interaction') as HTMLTextAreaElement)?.value || '';

    return {
      id,
      student_id: studentId,
      report_date: reportDate,
      notes,
      behavior,
      social_interaction: socialInteraction,
    };
  },

  async addDailyReport(data: { student_id: number; report_date: string; notes: string; behavior: string; social_interaction: string }) {
    try {
      const res = await authFetch('/daily-reports/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: data.student_id,
          date: data.report_date,
          notes: data.notes,
          behavior: data.behavior,
          social_interaction: data.social_interaction,
        }),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    params.append('student_id', String(data.student_id));
    params.append('report_date', data.report_date);
    params.append('notes', data.notes || '');
    params.append('behavior', data.behavior || '');
    params.append('social_interaction', data.social_interaction || '');

    const res = await authFetch('/daily-reports/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async editDailyReport(id: number, data: { student_id: number; report_date: string; notes: string; behavior: string; social_interaction: string }) {
    try {
      const res = await authFetch(`/daily-reports/api/edit/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: data.student_id,
          date: data.report_date,
          notes: data.notes,
          behavior: data.behavior,
          social_interaction: data.social_interaction,
        }),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    params.append('student_id', String(data.student_id));
    params.append('report_date', data.report_date);
    params.append('notes', data.notes || '');
    params.append('behavior', data.behavior || '');
    params.append('social_interaction', data.social_interaction || '');

    const res = await authFetch(`/daily-reports/${id}/edit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async deleteDailyReport(id: number) {
    try {
      const res = await authFetch(`/daily-reports/api/delete/${id}`, { method: 'POST' });
      if (res.ok) return true;
    } catch (e) {}
    const res = await authFetch(`/daily-reports/${id}/delete`);
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  // ── ASSESSMENTS ─────────────────────────────────────────────────
  async getAssessments(studentId?: number) {
    try {
      const url = studentId ? `/assessments/api/list?student_id=${studentId}` : '/assessments/api/list';
      const res = await authFetch(url);
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {}

    const url = studentId ? `/assessments?student_id=${studentId}` : '/assessments';
    const res = await authFetch(url);
    const html = await res.text();
    const doc = parseHTML(html);

    const assessments: any[] = [];
    doc.querySelectorAll('.grid > div.card, .space-y-4 > div.card').forEach(card => {
      const studentName = card.querySelector('.font-bold')?.textContent?.trim() || '';
      const period = card.querySelector('.badge-primary')?.textContent?.trim() || '';
      const summary = card.querySelector('p')?.textContent?.trim() || '';
      const editLink = card.querySelector('a[href^="/assessments/"]')?.getAttribute('href');
      const idMatch = editLink?.match(/\/assessments\/(\d+)/);
      const id = idMatch ? Number(idMatch[1]) : 0;

      if (id) {
        assessments.push({
          id,
          student_id: studentId || 0,
          student_name: studentName,
          period,
          summary,
        });
      }
    });
    return assessments;
  },

  async addAssessment(data: any) {
    try {
      const res = await authFetch('/assessments/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    for (const key in data) {
      if (data[key] !== undefined && data[key] !== null) {
        params.append(key, String(data[key]));
      }
    }
    const res = await authFetch('/assessments/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async editAssessment(id: number, data: any) {
    try {
      const res = await authFetch(`/assessments/api/edit/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    for (const key in data) {
      if (data[key] !== undefined && data[key] !== null) {
        params.append(key, String(data[key]));
      }
    }
    const res = await authFetch(`/assessments/${id}/edit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async deleteAssessment(id: number) {
    try {
      const res = await authFetch(`/assessments/api/delete/${id}`, { method: 'POST' });
      if (res.ok) return true;
    } catch (e) {}
    const res = await authFetch(`/assessments/${id}/delete`);
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  // ── GALLERY ─────────────────────────────────────────────────────
  async getGallery(studentId?: number) {
    try {
      const url = studentId ? `/gallery/api/list?student_id=${studentId}` : '/gallery/api/list';
      const res = await authFetch(url);
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {}

    const url = studentId ? `/gallery?student_id=${studentId}` : '/gallery';
    const res = await authFetch(url);
    const html = await res.text();
    const doc = parseHTML(html);

    const items: any[] = [];
    doc.querySelectorAll('.grid > div.card, .grid > div').forEach(card => {
      const img = card.querySelector('img')?.getAttribute('src') || '';
      const studentName = card.querySelector('.font-bold, .font-semibold')?.textContent?.trim() || '';
      const desc = card.querySelector('p')?.textContent?.trim() || '';
      const delLink = card.querySelector('a[href^="/gallery/"]')?.getAttribute('href');
      const idMatch = delLink?.match(/\/gallery\/(\d+)\/delete/);
      const id = idMatch ? Number(idMatch[1]) : 0;

      if (id && img) {
        items.push({
          id,
          student_id: studentId || 0,
          student_name: studentName,
          image_path: img,
          description: desc,
          date: '',
        });
      }
    });
    return items;
  },

  async uploadGallery(formData: FormData) {
    try {
      const res = await authFetch('/gallery/api/upload', {
        method: 'POST',
        body: formData,
      });
      if (res.ok) return true;
    } catch (e) {}

    const res = await authFetch('/gallery/upload', {
      method: 'POST',
      body: formData,
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async deleteGallery(id: number) {
    try {
      const res = await authFetch(`/gallery/api/delete/${id}`, { method: 'POST' });
      if (res.ok) return true;
    } catch (e) {}
    const res = await authFetch(`/gallery/${id}/delete`);
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  // ── EVALUATIONS (BK) ────────────────────────────────────────────
  async getEvaluationRekap() {
    try {
      const res = await authFetch('/evaluations/api/rekap');
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {}
    return [];
  },

  async addEvaluation(formData: URLSearchParams) {
    try {
      const res = await authFetch('/evaluations/api/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      });
      if (res.ok) return true;
    } catch (e) {}

    const res = await authFetch('/evaluations/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async deleteEvaluation(id: number) {
    try {
      const res = await authFetch(`/evaluations/api/delete/${id}`, { method: 'POST' });
      if (res.ok) return true;
    } catch (e) {}
    const res = await authFetch(`/evaluations/${id}/delete`);
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  // ── USERS ───────────────────────────────────────────────────────
  async getUsers() {
    try {
      const res = await authFetch('/api/users');
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {}

    const res = await authFetch('/users');
    const html = await res.text();
    const doc = parseHTML(html);

    const users: any[] = [];
    doc.querySelectorAll('table tbody tr').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length < 4) return;
      const name = cells[1]?.querySelector('.font-bold')?.textContent?.trim() || '';
      const email = cells[2]?.textContent?.trim() || '';
      const role = cells[3]?.textContent?.trim().toLowerCase().includes('admin') ? 'admin' : 'pendamping';
      const delLink = cells[4]?.querySelector('a[href^="/users/"]')?.getAttribute('href');
      const idMatch = delLink?.match(/\/users\/(\d+)\/delete/);
      const id = idMatch ? Number(idMatch[1]) : 0;

      if (id && name) {
        users.push({ id, name, email, role });
      }
    });
    return users;
  },

  async addUser(data: { name: string; email: string; password?: string; role: string }) {
    // 1. Try REST API
    try {
      const res = await authFetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) return true;
    } catch (e) {}

    // 2. Fallback to Form URL-Encoded (backend-fix pure)
    const params = new URLSearchParams();
    params.append('name', data.name);
    params.append('email', data.email);
    if (data.password) params.append('password', data.password);
    params.append('role', data.role);

    const res = await authFetch('/users/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async editUser(id: number, data: { name: string; email: string; role: string }) {
    try {
      const res = await authFetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    params.append('name', data.name);
    params.append('email', data.email);
    params.append('role', data.role);

    const res = await authFetch(`/users/${id}/edit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async resetPassword(id: number, password: string) {
    try {
      const res = await authFetch(`/api/users/${id}/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });
      if (res.ok) return true;
    } catch (e) {}

    const params = new URLSearchParams();
    params.append('password', password);

    const res = await authFetch(`/users/${id}/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: params.toString(),
    });
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  async deleteUser(id: number) {
    try {
      const res = await authFetch(`/api/users/${id}`, { method: 'DELETE' });
      if (res.ok) return true;
    } catch (e) {}
    const res = await authFetch(`/users/${id}/delete`);
    return res.ok || res.status === 302 || res.type === 'opaqueredirect';
  },

  // ── REPORTS ─────────────────────────────────────────────────────
  async getReportsList() {
    try {
      const students = await this.getStudents();
      return students.map((s: any) => ({
        student: s,
        assessments_count: 1,
      }));
    } catch (e) {}

    const res = await authFetch('/reports');
    const html = await res.text();
    const doc = parseHTML(html);

    const list: any[] = [];
    doc.querySelectorAll('table tbody tr').forEach(row => {
      const cells = row.querySelectorAll('td');
      if (cells.length < 5) return;
      const name = cells[0]?.querySelector('.font-bold')?.textContent?.trim() || '';
      const specialNeeds = cells[0]?.querySelector('.text-xs')?.textContent?.trim() || '';
      const age = parseInt(cells[1]?.textContent?.trim() || '0') || 0;
      const className = cells[2]?.textContent?.trim() || '';
      const isReady = cells[3]?.textContent?.includes('Siap Cetak') || false;
      const link = cells[4]?.querySelector('a')?.getAttribute('href') || '';
      const idMatch = link.match(/\/reports\/(\d+)/);
      const id = idMatch ? Number(idMatch[1]) : 0;

      if (id && name) {
        list.push({
          student: { id, name, age, class_name: className, special_needs: specialNeeds },
          assessments_count: isReady ? 1 : 0,
        });
      }
    });
    return list;
  },
};

export const apiRaport = api;
