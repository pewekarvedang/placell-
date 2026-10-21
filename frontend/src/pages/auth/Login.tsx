import React, { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Sparkles, Shield, GraduationCap, Briefcase, Award, ArrowRight, Lock, Mail, AlertCircle } from "lucide-react";

export const Login: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("student@college.edu");
  const [password, setPassword] = useState("Pass@123");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login({ email, password });
      navigate("/");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Authentication failed. Please verify credentials.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const setDemoCredentials = (roleEmail: string) => {
    setEmail(roleEmail);
    setPassword("Pass@123");
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center z-10">
        <div className="mx-auto w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-xl shadow-blue-500/25">
          <Sparkles className="w-6 h-6 text-white" />
        </div>
        <h2 className="mt-4 text-3xl font-extrabold tracking-tight text-white">
          Placell
        </h2>
        <p className="mt-1 text-xs text-slate-400 font-medium">
          AI-Powered Student Placement Experience &amp; Career Analytics System
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md z-10 px-4 sm:px-0">
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-2xl backdrop-blur-xl">
          {error && (
            <div className="mb-5 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-start space-x-2.5 text-xs text-rose-300">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Institutional Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
                  placeholder="name@college.edu"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full mt-2 py-2.5 px-4 rounded-xl font-semibold text-sm bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/25 flex items-center justify-center space-x-2 transition disabled:opacity-50"
            >
              <span>{isSubmitting ? "Authenticating..." : "Sign In to Workspace"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Role Switcher for Viva Presentation */}
          <div className="mt-8 pt-6 border-t border-slate-800">
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 text-center mb-3">
              One-Click Viva Demo Roles
            </p>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setDemoCredentials("student@college.edu")}
                className="p-2.5 rounded-lg border border-slate-800 bg-slate-950/60 hover:bg-slate-800 hover:border-slate-700 text-left transition flex items-center space-x-2"
              >
                <div className="p-1 rounded bg-emerald-500/10 text-emerald-400">
                  <GraduationCap className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-white">Student</p>
                  <p className="text-[10px] text-slate-400">Vedang Pewekar</p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setDemoCredentials("tpo@college.edu")}
                className="p-2.5 rounded-lg border border-slate-800 bg-slate-950/60 hover:bg-slate-800 hover:border-slate-700 text-left transition flex items-center space-x-2"
              >
                <div className="p-1 rounded bg-blue-500/10 text-blue-400">
                  <Briefcase className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-white">Placement Officer</p>
                  <p className="text-[10px] text-slate-400">Prof. Anita</p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setDemoCredentials("faculty.cse@college.edu")}
                className="p-2.5 rounded-lg border border-slate-800 bg-slate-950/60 hover:bg-slate-800 hover:border-slate-700 text-left transition flex items-center space-x-2"
              >
                <div className="p-1 rounded bg-amber-500/10 text-amber-400">
                  <Award className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-white">Faculty Coord.</p>
                  <p className="text-[10px] text-slate-400">Dr. Rajesh</p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setDemoCredentials("admin@college.edu")}
                className="p-2.5 rounded-lg border border-slate-800 bg-slate-950/60 hover:bg-slate-800 hover:border-slate-700 text-left transition flex items-center space-x-2"
              >
                <div className="p-1 rounded bg-purple-500/10 text-purple-400">
                  <Shield className="w-3.5 h-3.5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-white">System Admin</p>
                  <p className="text-[10px] text-slate-400">Full Access</p>
                </div>
              </button>
            </div>
            <p className="mt-3 text-center text-[10px] text-slate-400 font-mono">
              Default password: Pass@123
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
