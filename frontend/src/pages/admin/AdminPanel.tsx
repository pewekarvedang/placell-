import React, { useEffect, useState } from "react";
import { adminApi } from "../../services/api";
import { User, Skill, AuditLog } from "../../types";
import { Badge } from "../../components/common/Badge";
import {
  ShieldCheck,
  Users,
  Code2,
  ScrollText,
  Plus,
  Clock,
  CheckCircle2,
  AlertCircle,
  Building2
} from "lucide-react";

export const AdminPanel: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"users" | "departments" | "skills" | "audit">("users");
  const [users, setUsers] = useState<User[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  // New Department form
  const [newDeptCode, setNewDeptCode] = useState("");
  const [newDeptName, setNewDeptName] = useState("");
  const [newDeptDesc, setNewDeptDesc] = useState("");
  const [addingDept, setAddingDept] = useState(false);

  // New Skill form
  const [newSkillName, setNewSkillName] = useState("");
  const [newSkillCategory, setNewSkillCategory] = useState("PROGRAMMING");
  const [addingSkill, setAddingSkill] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [uData, dData, sData, aData] = await Promise.all([
          adminApi.getUsers(),
          adminApi.getDepartments(),
          adminApi.getSkills(),
          adminApi.getAuditLogs(100),
        ]);
        setUsers(uData);
        setDepartments(dData);
        setSkills(sData);
        setAuditLogs(aData);
      } catch (err) {
        console.error("Error loading admin data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleCreateDepartment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDeptCode.trim() || !newDeptName.trim()) return;
    setAddingDept(true);
    try {
      const added = await adminApi.addDepartment({
        code: newDeptCode.trim().toUpperCase(),
        name: newDeptName.trim(),
        description: newDeptDesc.trim() || undefined,
      });
      setDepartments([...departments, added]);
      setNewDeptCode("");
      setNewDeptName("");
      setNewDeptDesc("");
      setMessage(`Department "${added.code}" registered successfully.`);
      setTimeout(() => setMessage(null), 3000);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error adding department");
    } finally {
      setAddingDept(false);
    }
  };

  const handleCreateSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSkillName.trim()) return;
    setAddingSkill(true);
    try {
      const added = await adminApi.addSkill({
        name: newSkillName.trim(),
        category: newSkillCategory,
      });
      setSkills([...skills, added]);
      setNewSkillName("");
      setMessage("New skill added to central catalog.");
      setTimeout(() => setMessage(null), 3000);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error adding skill");
    } finally {
      setAddingSkill(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Enterprise Administrative Governance
          </h1>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
            ES Core Module
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Manage system users, central skills dictionary, and inspect immutable audit logging records.
        </p>
      </div>

      {message && (
        <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{message}</span>
        </div>
      )}

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab("users")}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === "users"
              ? "bg-blue-600 text-white"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          <Users className="w-4 h-4" />
          <span>Users &amp; Roles ({users.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("departments")}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === "departments"
              ? "bg-blue-600 text-white"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          <Building2 className="w-4 h-4" />
          <span>Departments ({departments.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("skills")}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === "skills"
              ? "bg-blue-600 text-white"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          <Code2 className="w-4 h-4" />
          <span>Skills Dictionary ({skills.length})</span>
        </button>

        <button
          onClick={() => setActiveTab("audit")}
          className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold transition ${
            activeTab === "audit"
              ? "bg-blue-600 text-white"
              : "text-slate-400 hover:text-white hover:bg-slate-800"
          }`}
        >
          <ScrollText className="w-4 h-4" />
          <span>Audit Trail ({auditLogs.length})</span>
        </button>
      </div>

      {/* Tab 1: Users */}
      {activeTab === "users" && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 uppercase font-semibold text-[10px] tracking-wider border-b border-slate-800">
                <tr>
                  <th className="px-6 py-3.5">User</th>
                  <th className="px-6 py-3.5">Email</th>
                  <th className="px-6 py-3.5">Role</th>
                  <th className="px-6 py-3.5">Department</th>
                  <th className="px-6 py-3.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/40 transition">
                    <td className="px-6 py-4 font-bold text-white">{u.full_name}</td>
                    <td className="px-6 py-4 font-mono text-slate-400">{u.email}</td>
                    <td className="px-6 py-4">
                      <Badge
                        variant={
                          u.role === "ADMIN"
                            ? "purple"
                            : u.role === "TPO"
                            ? "primary"
                            : u.role === "FACULTY"
                            ? "warning"
                            : "success"
                        }
                        size="sm"
                      >
                        {u.role}
                      </Badge>
                    </td>
                    <td className="px-6 py-4 text-slate-400">
                      {u.department_name || "Central / Directorate"}
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        Active
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab: Departments */}
      {activeTab === "departments" && (
        <div className="space-y-6">
          <form
            onSubmit={handleCreateDepartment}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row items-center gap-3"
          >
            <input
              type="text"
              required
              value={newDeptCode}
              onChange={(e) => setNewDeptCode(e.target.value)}
              placeholder="Code (e.g. CSDS, ECE)..."
              className="w-full sm:w-36 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white uppercase focus:outline-none focus:border-blue-500 font-mono"
            />
            <input
              type="text"
              required
              value={newDeptName}
              onChange={(e) => setNewDeptName(e.target.value)}
              placeholder="Full Department Name..."
              className="flex-1 w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
            />
            <input
              type="text"
              value={newDeptDesc}
              onChange={(e) => setNewDeptDesc(e.target.value)}
              placeholder="Description (Optional)..."
              className="flex-1 w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
            />
            <button
              type="submit"
              disabled={addingDept}
              className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs flex items-center justify-center space-x-1.5 transition shrink-0"
            >
              <Plus className="w-4 h-4" />
              <span>Register Department</span>
            </button>
          </form>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            {departments.map((d) => (
              <div
                key={d.id}
                className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="primary" size="md">
                    {d.code}
                  </Badge>
                  <Building2 className="w-4 h-4 text-slate-500" />
                </div>
                <h4 className="text-xs font-bold text-white">{d.name}</h4>
                <p className="text-[11px] text-slate-400 line-clamp-2">
                  {d.description || "Academic computing department registered under institutional placement."}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Skills Taxonomy */}
      {activeTab === "skills" && (
        <div className="space-y-6">
          <form
            onSubmit={handleCreateSkill}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row items-center gap-3"
          >
            <input
              type="text"
              required
              value={newSkillName}
              onChange={(e) => setNewSkillName(e.target.value)}
              placeholder="Skill Name (e.g. LangChain, Snowflake, GraphQL)..."
              className="flex-1 w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
            />
            <select
              value={newSkillCategory}
              onChange={(e) => setNewSkillCategory(e.target.value)}
              className="w-full sm:w-48 px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
            >
              <option value="PROGRAMMING">Programming</option>
              <option value="DATABASE">Database</option>
              <option value="CORE_CS">Core CS</option>
              <option value="FRAMEWORK">Framework</option>
              <option value="CLOUD_DEVOPS">Cloud / DevOps</option>
              <option value="AI_ML">AI / Data Science</option>
              <option value="SOFT_SKILL">Soft Skill</option>
            </select>
            <button
              type="submit"
              disabled={addingSkill}
              className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs flex items-center justify-center space-x-1.5 transition"
            >
              <Plus className="w-4 h-4" />
              <span>Add to Taxonomy</span>
            </button>
          </form>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {skills.map((s) => (
              <div
                key={s.id}
                className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between"
              >
                <p className="text-xs font-bold text-white">{s.name}</p>
                <span className="text-[10px] text-slate-500 font-mono mt-1">
                  {s.category}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: System Audit Trail (ES Requirement) */}
      {activeTab === "audit" && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 text-slate-400 uppercase font-semibold text-[10px] tracking-wider border-b border-slate-800">
                <tr>
                  <th className="px-6 py-3.5">Timestamp</th>
                  <th className="px-6 py-3.5">Action</th>
                  <th className="px-6 py-3.5">Actor (User)</th>
                  <th className="px-6 py-3.5">Target Entity</th>
                  <th className="px-6 py-3.5">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-800/40 transition">
                    <td className="px-6 py-3.5 font-mono text-[11px] text-slate-400 whitespace-nowrap">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="px-6 py-3.5 font-mono font-bold text-blue-400">
                      {log.action}
                    </td>
                    <td className="px-6 py-3.5">
                      <span className="text-white font-medium">{log.user_email || "System"}</span>
                      {log.user_role && (
                        <span className="block text-[10px] text-slate-500">
                          {log.user_role}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-3.5 text-slate-400 font-mono text-[11px]">
                      {log.entity_name}
                    </td>
                    <td className="px-6 py-3.5 text-slate-400 text-xs max-w-xs truncate">
                      {log.details || "N/A"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
