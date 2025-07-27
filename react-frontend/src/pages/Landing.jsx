import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import SidebarLayout from '../components/SidebarLayout'; // adjust import path as needed

export default function LandingPage() {
  const [activeTab, setActiveTab] = useState('login');
  const navigate = useNavigate();

  const handleStartPlanning = () => {
    Cookies.set('guest_session', 'true', { expires: 1 / 24 }); // 1 hour
    navigate('/form');
  };

  const handleAuthSubmit = () => {
    if (activeTab === 'signup') {
      // Perform sign-up logic here
      navigate('/form'); // to FS1PersonalInfo
    } else {
      // Perform login logic here
      navigate('/dashboard');
    }
  };

  return (
    <SidebarLayout>
      <div className="w-full max-w-2xl mx-auto mt-10 px-6 text-center">
        {/* Hero Card */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-md p-6 mb-10">
          <h2 className="text-3xl font-extrabold text-[#1a237e] mb-4">
            Plan Your UVic Courses with Ease
          </h2>
          <p className="text-gray-700 mb-6 font-medium">
            An AI-powered assistant that helps you
          </p>

          <ul className="text-[#1a237e] font-medium space-y-2 mb-6 list-disc list-inside mx-auto text-center w-fit">
            <li>Enter your academic info</li>
            <li>Get tailored course suggestions</li>
            <li>Avoid scheduling conflicts</li>
            <li>Export timetables effortlessly</li>
          </ul>

          {/* Start Planning Button */}
          <button
            onClick={handleStartPlanning}
            className="mt-2 bg-orange-500 text-white font-semibold py-2 px-6 rounded-full shadow hover:bg-orange-600 transition"
          >
            Start Planning
          </button>
        </div>

        {/* Auth Card */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-md p-6">
          <div className="flex justify-center mb-4 space-x-6 text-lg font-medium">
            <span
              className={`cursor-pointer ${
                activeTab === 'login'
                  ? 'text-yellow-600 border-b-2 border-yellow-500'
                  : 'text-gray-500 hover:text-black'
              }`}
              onClick={() => setActiveTab('login')}
            >
              Login
            </span>
            <span
              className={`cursor-pointer ${
                activeTab === 'signup'
                  ? 'text-yellow-600 border-b-2 border-yellow-500'
                  : 'text-gray-500 hover:text-black'
              }`}
              onClick={() => setActiveTab('signup')}
            >
              Sign Up
            </span>
          </div>

          <input
            type="email"
            placeholder="Email"
            className="w-full mb-3 px-4 py-2 border border-gray-300 rounded bg-white text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#1a237e]"
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full mb-4 px-4 py-2 border border-gray-300 rounded bg-white text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#1a237e]"
          />

          <button
            className="w-full bg-[#1a237e] text-white py-2 rounded hover:bg-[#283593] font-semibold"
            onClick={handleAuthSubmit}
          >
            {activeTab === 'login' ? 'Login' : 'Sign Up'}
          </button>
        </div>
      </div>
    </SidebarLayout>
  );
}
