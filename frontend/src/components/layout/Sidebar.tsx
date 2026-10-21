import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import {
  LayoutDashboard,
  UserCheck,
  Target,
  FilePlus,
  Briefcase,
  Building2,
  BarChart3,
  CheckCircle2,
  ShieldCheck,
  ScrollText,
  Sparkles,
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const { role } = useAuth();

  const getNavLinks = () => {
    switch (role) {
      case "STUDENT":
        return [
          { to: "/", label: "Student Workspace", icon: LayoutDashboard },
          { to: "/profile", label: "My Profile & Skills", icon: UserCheck },
          { to: "/skill-gap", label: "Skill-Gap Analyzer", icon: Target, badge: "AI" },
          { to: "/submit-experience", label: "Log Experience", icon: FilePlus },
          { to: "/drives", label: "Placement Drives", icon: Briefcase },
          { to: "/experiences", label: "Interview Archive", icon: ScrollText },
          { to: "/companies", label: "Companies", icon: Building2 },
        ];
      case "TPO":
        return [
          { to: "/", label: "Placement Cell Portal", icon: LayoutDashboard },
          { to: "/moderation", label: "Verification Queue", icon: CheckCircle2, badge: "Review" },
          { to: "/drives", label: "Drives Management", icon: Briefcase },
          { to: "/companies", label: "Corporate Partners", icon: Building2 },
          { to: "/analytics", label: "College Analytics", icon: BarChart3 },
          { to: "/experiences", label: "Student Reviews", icon: ScrollText },
        ];
      case "FACULTY":
        return [
          { to: "/", label: "Faculty Dashboard", icon: LayoutDashboard },
          { to: "/analytics", label: "Department Analytics", icon: BarChart3 },
          { to: "/drives", label: "Placement Drives", icon: Briefcase },
          { to: "/companies", label: "Recruiter Trends", icon: Building2 },
          { to: "/experiences", label: "Student Feedback", icon: ScrollText },
        ];
      case "ADMIN":
        return [
          { to: "/", label: "Admin Console", icon: LayoutDashboard },
          { to: "/admin", label: "User & Master Data", icon: ShieldCheck },
          { to: "/analytics", label: "System Analytics", icon: BarChart3 },
          { to: "/drives", label: "Placement Drives", icon: Briefcase },
          { to: "/companies", label: "Company Registry", icon: Building2 },
          { to: "/experiences", label: "All Experiences", icon: ScrollText },
        ];
      default:
        return [
          { to: "/experiences", label: "Experiences", icon: ScrollText },
          { to: "/companies", label: "Companies", icon: Building2 },
        ];
    }
  };

  const navLinks = getNavLinks();

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 flex flex-col shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="p-4">
        <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2">
          Navigation
        </p>
        <nav className="space-y-1">
          {navLinks.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition ${
                    isActive
                      ? "bg-blue-600/15 text-blue-400 border border-blue-500/30"
                      : "text-slate-300 hover:text-white hover:bg-slate-800/60"
                  }`
                }
              >
                <div className="flex items-center space-x-2.5">
                  <Icon className="w-4 h-4 text-slate-400" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      <div className="mt-auto p-4 border-t border-slate-800/80">
        <div className="p-3 rounded-lg bg-gradient-to-br from-slate-800/40 to-slate-900/80 border border-slate-700/50">
          <div className="flex items-center space-x-2 text-indigo-400 mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span className="text-[11px] font-bold">Academic Demo Ready</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Multi-tier ES authorization &amp; NLP extraction active.
          </p>
        </div>
      </div>
    </aside>
  );
};
