// components/Header.jsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import logo from '../assets/logo.png';

function HamburgerIcon() {
  return (
    <svg
      className="h-6 w-6 text-accent"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg
      className="h-6 w-6 text-accent"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

export default function Header() {
  const { isLoggedIn } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNavigate = (path) => {
    setSidebarOpen(false);
    navigate(path);
  };

  // Close on ESC + lock body scroll when open
  useEffect(() => {
    if (!sidebarOpen) return;

    const onKey = (e) => {
      if (e.key === 'Escape') setSidebarOpen(false);
    };
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', onKey);

    return () => {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', onKey);
    };
  }, [sidebarOpen]);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-primary border-b border-yellow-900 shadow-soft">
      <div className="mx-auto flex items-center justify-between px-8 sm:px-6 py-4">
        {/* Logo + Title (matching PublicHeader.jsx) */}
        <div
          role="button"
          tabIndex={0}
          onClick={() => navigate('/')}
          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && navigate('/')}
          className="flex items-center gap-2 cursor-pointer select-none"
          aria-label="Go to homepage"
        >
          <img src={logo} alt="CourseCraft logo" className="h-8 w-8" />
          <h1 className="text-xl font-bold text-purple">CourseCraft</h1>
        </div>

        {/* Right-side Menu */}
        {isLoggedIn && (
          <>
            <button
              onClick={() => setSidebarOpen(true)}
              aria-label="Open Sidebar"
              className="p-1"
            >
              <HamburgerIcon />
            </button>

            {/* Sidebar Drawer */}
            {sidebarOpen && (
              <>
                <aside
                  className="fixed inset-y-0 right-0 w-64 bg-offwhite text-dark shadow-md z-50"
                  role="dialog"
                  aria-modal="true"
                >
                  <div className="flex items-center justify-between px-4 py-4 border-b">
                    <h2 className="text-xl font-bold text-purple">Menu</h2>
                    <button
                      onClick={() => setSidebarOpen(false)}
                      aria-label="Close Menu"
                      className="p-1"
                    >
                      <CloseIcon />
                    </button>
                  </div>
                  <nav className="mt-2">
                    <ul className="divide-y divide-gray-200">
                      {[
                        { label: 'Home', path: '/' },
                        { label: 'Dashboard', path: '/dashboard' },
                        { label: 'Profile Form', path: '/form' },
                        { label: 'Course Plan', path: '/form/plan' }, // <-- fixed path
                        { label: 'Prerequisite Courses', path: '/courses' },
                        { label: 'Chatbot AI', path: '/chat' },
                      ].map(({ label, path }) => (
                        <li key={path}>
                          <button
                            onClick={() => handleNavigate(path)}
                            className="w-full text-left px-4 py-3 text-base font-medium hover:bg-gray-100"
                          >
                            {label}
                          </button>
                        </li>
                      ))}
                    </ul>
                  </nav>
                </aside>

                {/* Overlay */}
                <div
                  className="fixed inset-0 bg-black/50 z-40"
                  onClick={() => setSidebarOpen(false)}
                  aria-hidden="true"
                />
              </>
            )}
          </>
        )}
      </div>
    </header>
  );
}
