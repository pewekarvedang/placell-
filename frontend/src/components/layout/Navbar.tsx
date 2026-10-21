import React from "react";
import { useAuth } from "../../context/AuthContext";
import { LogOut, User as UserIcon, Shield, Sparkles, Building2 } from "lucide-react";
import { Badge } from "../common/Badge";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();

  const getRoleBadgeVariant = (role?: string) => {
    switch (role) {
      case "ADMIN":
        return "purple";
      case "TPO":
        return "primary";
      case "FACULTY":
        return "warning";
      case "STUDENT":
        return "success";
      default:
        return "neutral";
    }
  };

  const getRoleDisplayName = (role?: string) => {
    switch (role) {
      case "ADMIN":
        return "System Admin";
      case "TPO":
        return "Placement Officer";
      case "FACULTY":
        return "Faculty Coordinator";
      case "STUDENT":
        return "Student";
      default:
        return "Guest";
    }
  };

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-30 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
            Placell
          </span>
        </div>
      </div>

      {user && (
        <div className="flex items-center space-x-4">
          <div className="hidden sm:flex items-center space-x-3 text-right">
            <div>
              <p className="text-xs font-semibold text-white">{user.full_name}</p>
              <div className="flex items-center justify-end space-x-1.5 mt-0.5">
                <Badge variant={getRoleBadgeVariant(user.role)} size="sm">
                  {getRoleDisplayName(user.role)}
                </Badge>
                {user.department_code && (
                  <span className="text-[11px] text-slate-400 font-mono">
                    [{user.department_code}]
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="h-7 w-px bg-slate-800"></div>

          <button
            onClick={logout}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-700/60 transition"
            title="Sign out of session"
          >
            <LogOut className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden md:inline">Sign Out</span>
          </button>
        </div>
      )}
    </header>
  );
};
