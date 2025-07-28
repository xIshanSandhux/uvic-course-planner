import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Footer from './Footer';
import logo from '../assets/logo.png';

/* Reusable Icon Wrapper */
function IconWrapper({ children }) {
  return (
    <div className="p-1.5 bg-black rounded-md flex items-center justify-center">
      {children}
    </div>
  );
}

/* Hamburger Icon */
function HamburgerIcon() {
  return (
    <svg
      className="h-6 w-6 text-accent hover:text-cyan"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}

/* Close Icon */
function CloseIcon() {
  return (
    <svg
      className="h-6 w-6 text-accent hover:text-cyan"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
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
    <div className="flex flex-col min-h-screen w-screen bg-offwhite text-purple font-sans overflow-x-hidden">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 right-0 w-64 bg-offwhite text-dark transform ${
          sidebarOpen ? 'translate-x-0' : 'translate-x-full'
        } transition-transform duration-300 ease-in-out shadow-soft z-30`}
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between px-4 py-4 border-b border-yellow-900">
          <h2 className="text-xl font-bold text-dark">Menu</h2>
          <button onClick={() => setSidebarOpen(false)} aria-label="Close Menu">
              <CloseIcon />
          </button>
        </div>

        {/* Navigation */}
        <nav className="mt-2">
          <ul className="divide-y divide-gray-200">
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
                  className="w-full text-left px-4 py-3 text-base font-medium bg-offwhite text-dark hover:bg-accent hover:text-white transition-colors"
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

      {/* Main Content Area */}
      <div className="flex-grow flex flex-col">
        {/* Header */}
        <header className="flex justify-between items-center px-8 py-4 sm:px-6 bg-primary border-b border-yellow-900 z-10">
          <div
            onClick={() => navigate('/')}
            className="flex items-center gap-2 cursor-pointer"
          >
            <img src={logo} alt="CourseCraft Logo" className="h-8 w-8 object-contain" />
            <span className="text-xl sm:text-2xl font-extrabold text-purple">CourseCraft</span>
          </div>
          <button onClick={() => setSidebarOpen(true)} aria-label="Open Menu">
              <HamburgerIcon />
          </button>
        </header>

        <main className="flex-grow pb-8">{children}</main>
        <Footer />
      </div>
    </div>
  );
}
