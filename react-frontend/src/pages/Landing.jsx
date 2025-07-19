import React from 'react';
import { useNavigate } from 'react-router-dom';
import SidebarLayout from '../components/SidebarLayout';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <SidebarLayout>
      <div className="flex-grow flex flex-col">
        <header className="p-4 bg-transparent">
          <button onClick={() => navigate('/form')} aria-label="Start Planning">
            {/* Optional: keep the icon or text here if needed */}
          </button>
        </header>

        {/* Hero Section */}
        <main className="flex-grow flex flex-col justify-center items-center px-6 text-center">
          <section className="bg-white rounded-2xl p-10 max-w-2xl shadow-soft">
            <h1 className="text-4xl pb-4 font-extrabold mb-4 text-purple">
              Plan Your UVic Courses with Ease
            </h1>
            <p className="text-lg text-black font-medium mb-6">
              An AI-powered assistant that helps you:
            </p>
            <ul className="grid grid-cols-1 sm:grid-cols-1 gap-4 text-center text-purple/70 font-small list-disc list-inside mb-8">
              <li>Enter your academic info</li>
              <li>Get tailored course suggestions</li>
              <li>Avoid scheduling conflicts</li>
              <li>Export timetables effortlessly</li>
            </ul>
            <button
              onClick={() => navigate('/form')}
              className="px-8 py-3 bg-accent shadow-soft text-white font-semibold rounded-full hover:text-black hover:bg-cyan transition"
            >
              Start Planning
            </button>
          </section>
        </main>
      </div>
    </SidebarLayout>
  );
}
