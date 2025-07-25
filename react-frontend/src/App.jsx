import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import FS1PersonalInfo from './pages/FS1PersonalInfo';
import FS2CoursePlan from './pages/FS2CoursePlan';
import FS3PrereqsCompleted from './pages/FS3PrereqsCompleted';
import Chatbot from './pages/Chatbot';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-grow">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/form" element={<FS1PersonalInfo />} />
          <Route path="/form/plan" element={<FS2CoursePlan />} />
          <Route path="/courses" element={<FS3PrereqsCompleted />} />
          <Route path="/chat" element={<Chatbot />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
