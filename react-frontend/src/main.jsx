import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import Landing from './pages/Landing';
import UserForm from './pages/UserForm';
import CourseSelect from './pages/CourseSelect';
import Chatbot from './pages/Chatbot';

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/form" element={<UserForm />} />
      <Route path="/courses" element={<CourseSelect />} />
      <Route path="/chat" element={<Chatbot />} />
    </Routes>
  </BrowserRouter>
);
