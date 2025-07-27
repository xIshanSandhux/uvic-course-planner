import React from 'react';
import { useNavigate } from 'react-router-dom';
import SidebarLayout from '../components/SidebarLayout';

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <SidebarLayout>
      <main className="w-full max-w-5xl mx-auto px-4 py-8 overflow-x-hidden text-purple">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Welcome back, Shaafi 👋</h1>
          <p className="text-sm text-gray-600">
            BSc in Computer Science | 28/120 Credits | Est. Grad: Apr 2028
          </p>
        </div>

        {/* 1. Term Timeline */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-2">📅 4-Year Term Timeline</h2>
          <div className="grid grid-cols-4 gap-4 bg-white rounded-lg shadow p-4">
            {[2025, 2026, 2027, 2028].map((year) => (
              <div key={year} className="space-y-2">
                <h3 className="font-semibold">{year}</h3>
                {['Fall', 'Spring', 'Summer'].map((term) => (
                  <div
                    key={term}
                    className="p-2 bg-gray-100 rounded hover:bg-yellow-100 cursor-pointer text-sm"
                  >
                    {term} — Study
                  </div>
                ))}
              </div>
            ))}
          </div>
        </section>

        {/* 2. Progress Tracker */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-2">🎓 Progress Tracker</h2>
          <div className="grid grid-cols-2 gap-4">
            {[
              ['Total Credits', '28 / 120'],
              ['Core Courses', '8 / 24'],
              ['Electives', '2 / 12'],
              ['Math & Science Req', '3 / 6'],
              ['Co-op Terms', '1 / 3'],
            ].map(([label, value]) => (
              <div key={label} className="bg-white rounded shadow p-4">
                <p className="text-sm text-gray-600">{label}</p>
                <p className="text-lg font-bold">{value}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 3. Plan Summary */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-2">📋 Next Term Plan Summary</h2>
          <div className="bg-white rounded shadow p-4 space-y-1 text-sm">
            <p>🗓️ <b>Term:</b> Spring 2026</p>
            <p>📚 <b>Courses:</b> MATH 101, CSC 115, PHYS 102</p>
            <p>🕒 <b>Time Prefs:</b> Morning Only (8AM–12PM)</p>
            <p>🎨 <b>Electives:</b> Yes (BUS 150)</p>
            <p>🧘 <b>Style:</b> Balanced</p>
            <div className="flex gap-3 mt-3">
              <button className="text-sm bg-black text-white px-3 py-1 rounded" onClick={() => navigate('/form/plan')}>Edit Plan</button>
              <button className="text-sm border border-purple text-purple px-3 py-1 rounded">Launch Chat</button>
              <button className="text-sm border border-purple text-purple px-3 py-1 rounded">Export PDF</button>
            </div>
          </div>
        </section>

        {/* 4. Chat History */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-2">💬 Chat History</h2>
          <div className="bg-white rounded shadow divide-y">
            {[
              ['Fall 2025', 'Focused on prereqs + intro CS'],
              ['Spring 2026', 'Elective planning + AI track'],
              ['Summer 2026', 'Co-op application discussion'],
            ].map(([term, summary]) => (
              <div key={term} className="p-4 flex justify-between text-sm hover:bg-gray-50">
                <div>
                  <p className="font-medium">{term}</p>
                  <p className="text-gray-600">{summary}</p>
                </div>
                <button className="text-purple underline text-sm">View Chat</button>
              </div>
            ))}
          </div>
        </section>

        {/* 5. Smart Insights */}
        <section className="mb-16">
          <h2 className="text-xl font-semibold mb-2">🔍 Smart AI Insights</h2>
          <ul className="space-y-2 text-sm bg-white rounded shadow p-4">
            <li>⚠️ You’re 8 credits behind co-op eligibility.</li>
            <li>🧠 AI Suggestion: Add 1 more elective next term.</li>
            <li>🎯 Stay on track by taking 3 courses per term till 2028.</li>
            <li>💡 You are eligible for CSC 226 — want to add it?</li>
          </ul>
        </section>
      </main>
    </SidebarLayout>
  );
}
