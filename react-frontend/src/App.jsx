import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import FS1PersonalInfo from './pages/FS1PersonalInfo';
import FS2CoursePlan from './pages/FS2CoursePlan';
import FS3PrereqsCompleted from './pages/FS3PrereqsCompleted';
import Chatbot from './pages/Chatbot';
import AppShell from './components/AppShell';

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <AppShell publicHeader>
            <Landing />
          </AppShell>
        }
      />
      <Route
        path="/dashboard"
        element={
          <AppShell>
            <Dashboard />
          </AppShell>
        }
      />
      <Route
        path="/form"
        element={
          <AppShell>
            <FS1PersonalInfo />
          </AppShell>
        }
      />
      <Route
        path="/form/plan"
        element={
          <AppShell>
            <FS2CoursePlan />
          </AppShell>
        }
      />
      <Route
        path="/courses"
        element={
          <AppShell>
            <FS3PrereqsCompleted />
          </AppShell>
        }
      />
      <Route
        path="/chat"
        element={
          <AppShell>
            <Chatbot />
          </AppShell>
        }
      />
    </Routes>
  );
}

export default App;
