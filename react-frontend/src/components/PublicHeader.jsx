// components/PublicHeader.jsx
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';

export default function PublicHeader({ fixed = true }) {
  const navigate = useNavigate();

  return (
    <header
      className={`${fixed ? 'fixed top-0 left-0 right-0 z-50' : ''} bg-primary border-b border-yellow-900 shadow-soft`}
    >
      <div className="mx-auto flex items-center justify-between px-8 sm:px-6 py-4">
        {/* Logo + Title */}
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

        {/* Right Side Placeholder (empty, but keeps layout consistent with Header) */}
        <div className="w-6" aria-hidden="true" />
      </div>
    </header>
  );
}
