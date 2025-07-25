import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Footer from './Footer';

function HamburgerIcon() {
  return (
    <svg className="h-8 w-8 text-accent hover:text-cyan" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg className="h-6 w-6 text-accent hover:text-cyan" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

export default function SidebarLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    setSidebarOpen(false);
    navigate(path);
  };

  return (
    <div className="flex flex-col min-h-screen w-screen bg-offwhite text-purple font-sans">

      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 w-64 bg-offwhite text-dark transform ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } transition-transform duration-300 ease-in-out shadow-soft z-30`}>
        <div className="flex items-center justify-between px-4 py-4 border-b border-yellow-300">
          <h2 className="text-xl font-bold text-dark">Menu</h2>
          <button onClick={() => setSidebarOpen(false)} aria-label="Close Menu">
            <CloseIcon />
          </button>
        </div>
        <nav className="mt-6">
          <ul className="space-y-1">
            {[ 
              { label: 'Home', path: '/' },
              { label: 'Dashboard', path: '/dashboard' },
              { label: 'Profile Form', path: '/form' },
              { label: 'Course Plan', path: '/form/plan' },
              { label: 'Prerequisite Courses', path: '/courses' },
              { label: 'Chatbot AI', path: '/chat' },
            ].map(({ label, path }) => (
              <li key={path}>
                <button
                  onClick={() => handleNavigate(path)}
                  className="block w-full text-left px-4 py-3 bg-offwhite text-dark hover:bg-accent hover:text-white transition-colors rounded"
                >
                  {label}
                </button>
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

      {/* Page content */}
      <div className="flex-grow flex flex-col">
        <header className="p-4 z-10 bg-transparent">
          <button onClick={() => setSidebarOpen(true)} aria-label="Open Menu">
            <HamburgerIcon />
          </button>
        </header>

        <main className="flex-grow">{children}</main>

        <Footer />
      </div>
    </div>
  );
}
