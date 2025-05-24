import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function HamburgerIcon() {
  return (
    <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

export default function LandingPage() {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen w-screen bg-gradient-to-b from-blue-600 to-blue-900 text-white">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 w-64 bg-blue-950 text-white transform ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-transform duration-300 ease-in-out shadow-lg z-30`}
        role="navigation"
      >
        <div className="flex items-center justify-between px-4 py-4 border-b border-blue-800">
          <h2 className="text-xl font-bold">Menu</h2>
          <button onClick={() => setSidebarOpen(false)} aria-label="Close Menu">
            <CloseIcon />
          </button>
        </div>
        <nav className="mt-6">
          <ul className="space-y-1">
            {[
              { label: 'Home', path: '/' },
              { label: 'Profile Form', path: '/form' },
              { label: 'Course List', path: '/courses' },
              { label: 'Chatbot AI', path: '/chat' },
            ].map(({ label, path }) => (
              <li key={path}>
                <Link
                  to={path}
                  className="block px-4 py-3 hover:bg-blue-800 transition rounded"
                  onClick={() => setSidebarOpen(false)}
                >
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-20"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Main content */}
      <div className="flex-grow flex flex-col">
        {/* Top Bar */}
        <header className="p-4 bg-transparent">
          <button onClick={() => setSidebarOpen(true)} aria-label="Open Menu">
            <HamburgerIcon />
          </button>
        </header>

        {/* Hero Section */}
        <main className="flex-grow flex flex-col justify-center items-center px-6 text-center">
          <section className="backdrop-blur-lg bg-white bg-opacity-10 rounded-2xl p-10 max-w-2xl shadow-lg">
            <h1 className="text-5xl font-extrabold text-white mb-4">
              Plan Your UVic Courses with Ease
            </h1>
            <p className="text-lg text-gray-200 mb-6">
              An AI-powered assistant that helps you:
            </p>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left text-yellow-300 list-disc list-inside mb-8">
              <li>Pick your courses smartly</li>
              <li>Avoid scheduling conflicts</li>
              <li>Get tailored suggestions</li>
              <li>Export timetables effortlessly</li>
            </ul>
            <button
              onClick={() => navigate('/form')}
              className="px-8 py-3 bg-yellow-400 text-blue-950 font-semibold rounded-full hover:bg-yellow-300 transition"
            >
              Start Planning
            </button>
          </section>
        </main>

        {/* Footer */}
        <footer className="bg-blue-950 text-gray-300 py-4 text-center text-sm">
          © {new Date().getFullYear()} UVic Course Planner
        </footer>
      </div>
    </div>
    
  );
}