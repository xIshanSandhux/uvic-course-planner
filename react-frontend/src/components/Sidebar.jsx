// components/Sidebar.jsx
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

/* Hamburger Icon */
export function HamburgerIcon() {
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

export default function Sidebar({ open, onClose }) {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    onClose();
    navigate(path);
  };

  return (
    <>
      {/* Sidebar Drawer */}
      <aside
        className={`fixed inset-y-0 right-0 w-64 bg-offwhite text-dark transform ${
          open ? 'translate-x-0' : 'translate-x-full'
        } transition-transform duration-300 ease-in-out shadow-soft z-50`}
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between px-4 py-4 border-b border-yellow-900">
          <h2 className="text-xl font-bold text-dark">Menu</h2>
          <button onClick={onClose} aria-label="Close Menu">
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
      {open && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
          aria-hidden="true"
        />
      )}
    </>
  );
}
