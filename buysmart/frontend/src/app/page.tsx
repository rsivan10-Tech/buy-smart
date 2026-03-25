'use client';

import React, { useEffect, useState } from 'react';
import { useProjectStore } from '@/store/useProjectStore';

type WelcomeResponse = {
  message: string;
};

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export default function Home() {
  const { projects, setProjects, addProject, loading, setLoading, error, setError } = useProjectStore();
  const [welcomeText, setWelcomeText] = useState('');

  useEffect(() => {
    async function loadProjects() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${BACKEND_URL}/projects`);
        if (!res.ok) throw new Error(`API error ${res.status}`);
        const data = await res.json();
        setProjects(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    }

    async function loadWelcome() {
      try {
        const res = await fetch(`${BACKEND_URL}/api/welcome`);
        if (!res.ok) return;
        const data: WelcomeResponse = await res.json();
        setWelcomeText(data.message);
      } catch {
        setWelcomeText('Could not reach backend');
      }
    }

    loadWelcome();
    loadProjects();
  }, [setProjects, setLoading, setError]);

  const createProject = async () => {
    try {
      const payload = { name: 'דירת דוגמה', city: 'תל אביב', area_sqm: 72.5, price_ils: 2500000 };
      const res = await fetch(`${BACKEND_URL}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`failed to save project (${res.status})`);
      const project = await res.json();
      addProject(project);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 text-right" dir="rtl">
      <main className="mx-auto w-full max-w-4xl rounded-3xl border border-gray-200 bg-white p-10 shadow-lg">
        <h1 className="text-4xl font-black tracking-tight text-slate-900">בואו לחסוך בבחירת דירה על הנייר עם Buy Smart</h1>
        <p className="mt-4 text-lg text-slate-700">{welcomeText || 'טוען...'}</p>

        <button
          type="button"
          className="mt-6 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          onClick={createProject}
        >
          צור פרויקט חדש לדגומה
        </button>

        {loading && <p className="mt-4 text-sm text-slate-500">טוען פרויקטים מהשרת...</p>}
        {error && <p className="mt-4 text-sm text-red-600">שגיאה: {error}</p>}

        <div className="mt-6">
          <h2 className="text-2xl font-semibold">פרויקטים קיימים</h2>
          {projects.length === 0 ? (
            <p className="mt-2 text-sm text-slate-600">אין פרויקטים להצגה</p>
          ) : (
            <ul className="mt-3 space-y-2">
              {projects.map((proj) => (
                <li key={proj.id} className="rounded border p-3 text-right">
                  <strong>{proj.name}</strong> - {proj.city} - {proj.area_sqm} מ"ר - {proj.price_ils} ש"ח
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}
