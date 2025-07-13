import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import Landing from './pages/Landing';

import FS1PersonalInfo from './pages/FS1PersonalInfo.jsx';
import FS2CoursePlan from './pages/FS2CoursePlan';
import FS3PrereqsCompleted from './pages/FS3PrereqsCompleted';

import Chatbot from './pages/Chatbot';

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/form" element={<FS1PersonalInfo />} />
      <Route path="/form/plan" element={<FS2CoursePlan />} />
      <Route path="/courses" element={<FS3PrereqsCompleted />} />
      <Route path="/chat" element={<Chatbot />} />
    </Routes>
  </BrowserRouter>
);
