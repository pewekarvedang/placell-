import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { Navbar } from "./components/layout/Navbar";
import { Sidebar } from "./components/layout/Sidebar";

// Pages
import { Login } from "./pages/auth/Login";
import { StudentDashboard } from "./pages/student/StudentDashboard";
import { ProfileView } from "./pages/student/ProfileView";
import { SkillGapView } from "./pages/student/SkillGapView";
import { SubmitExperience } from "./pages/student/SubmitExperience";
import { TPODashboard } from "./pages/tpo/TPODashboard";
import { ModerationQueue } from "./pages/tpo/ModerationQueue";
import { AnalyticsDashboard } from "./pages/analytics/AnalyticsDashboard";
import { ExperiencesList } from "./pages/shared/ExperiencesList";
import { CompaniesDirectory } from "./pages/shared/CompaniesDirectory";
import { DrivesCatalog } from "./pages/shared/DrivesCatalog";
import { AdminPanel } from "./pages/admin/AdminPanel";

// Protected Layout Route wrapper
const ProtectedLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 bg-slate-950/40 min-w-0 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

// Role-based Root Route Router
const RoleDashboardRouter: React.FC = () => {
  const { role } = useAuth();

  switch (role) {
    case "STUDENT":
      return <StudentDashboard />;
    case "TPO":
      return <TPODashboard />;
    case "FACULTY":
      return <AnalyticsDashboard />;
    case "ADMIN":
      return <AdminPanel />;
    default:
      return <StudentDashboard />;
  }
};

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<Login />} />

          {/* Protected Enterprise Routes */}
          <Route
            path="/"
            element={
              <ProtectedLayout>
                <RoleDashboardRouter />
              </ProtectedLayout>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedLayout>
                <ProfileView />
              </ProtectedLayout>
            }
          />
          <Route
            path="/skill-gap"
            element={
              <ProtectedLayout>
                <SkillGapView />
              </ProtectedLayout>
            }
          />
          <Route
            path="/submit-experience"
            element={
              <ProtectedLayout>
                <SubmitExperience />
              </ProtectedLayout>
            }
          />
          <Route
            path="/moderation"
            element={
              <ProtectedLayout>
                <ModerationQueue />
              </ProtectedLayout>
            }
          />
          <Route
            path="/analytics"
            element={
              <ProtectedLayout>
                <AnalyticsDashboard />
              </ProtectedLayout>
            }
          />
          <Route
            path="/experiences"
            element={
              <ProtectedLayout>
                <ExperiencesList />
              </ProtectedLayout>
            }
          />
          <Route
            path="/companies"
            element={
              <ProtectedLayout>
                <CompaniesDirectory />
              </ProtectedLayout>
            }
          />
          <Route
            path="/drives"
            element={
              <ProtectedLayout>
                <DrivesCatalog />
              </ProtectedLayout>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedLayout>
                <AdminPanel />
              </ProtectedLayout>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
