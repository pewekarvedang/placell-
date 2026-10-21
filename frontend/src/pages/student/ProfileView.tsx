import React, { useEffect, useState } from "react";
import { studentApi, adminApi } from "../../services/api";
import { StudentProfile, Skill } from "../../types";
import { Badge } from "../../components/common/Badge";
import {
  UserCheck,
  Code2,
  GraduationCap,
  Briefcase,
  Award,
  Save,
  Plus,
  Trash2,
  CheckCircle2,
  AlertCircle
} from "lucide-react";

export const ProfileView: React.FC = () => {
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [availableSkills, setAvailableSkills] = useState<Skill[]>([]);
  const [selectedSkillId, setSelectedSkillId] = useState("");
  const [proficiency, setProficiency] = useState("Intermediate");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Form editable states
  const [cgpa, setCgpa] = useState<number>(7.5);
  const [projectsCount, setProjectsCount] = useState<number>(2);
  const [internshipsCount, setInternshipsCount] = useState<number>(0);
  const [certificationsCount, setCertificationsCount] = useState<number>(1);
  const [preferredRole, setPreferredRole] = useState("Software Development Engineer (SDE-1)");
  const [bio, setBio] = useState("");

  useEffect(() => {
    const fetchProfileAndSkills = async () => {
      try {
        const [profData, skillsData] = await Promise.all([
          studentApi.getProfile(),
          adminApi.getSkills(),
        ]);
        setProfile(profData);
        setCgpa(profData.cgpa);
        setProjectsCount(profData.projects_count);
        setInternshipsCount(profData.internships_count);
        setCertificationsCount(profData.certifications_count);
        setPreferredRole(profData.preferred_role_title);
        setBio(profData.bio || "");
        setAvailableSkills(skillsData);
        if (skillsData.length > 0) {
          setSelectedSkillId(skillsData[0].id);
        }
      } catch (err) {
        console.error("Error fetching profile:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfileAndSkills();
  }, []);

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    try {
      const updated = await studentApi.updateProfile({
        cgpa: Number(cgpa),
        projects_count: Number(projectsCount),
        internships_count: Number(internshipsCount),
        certifications_count: Number(certificationsCount),
        preferred_role_title: preferredRole,
        bio: bio,
      });
      setProfile(updated);
      setMessage({ type: "success", text: "Profile records updated successfully!" });
    } catch (err: any) {
      setMessage({ type: "error", text: err.response?.data?.detail || "Failed to update profile." });
    } finally {
      setSaving(false);
    }
  };

  const handleAddSkill = async () => {
    if (!selectedSkillId) return;
    try {
      const updated = await studentApi.addSkill(selectedSkillId, proficiency);
      setProfile(updated);
      setMessage({ type: "success", text: "Skill added to your inventory!" });
    } catch (err: any) {
      setMessage({ type: "error", text: err.response?.data?.detail || "Could not add skill." });
    }
  };

  const handleRemoveSkill = async (skillId: string) => {
    try {
      const updated = await studentApi.removeSkill(skillId);
      setProfile(updated);
      setMessage({ type: "success", text: "Skill removed from your profile." });
    } catch (err: any) {
      setMessage({ type: "error", text: "Could not remove skill." });
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // Filter out skills the student already possesses
  const possessedSkillIds = new Set(profile?.skills.map((s) => s.skill_id));
  const unselectedSkills = availableSkills.filter((s) => !possessedSkillIds.has(s.id));

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">
          Student Profile &amp; Academic Portfolio
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Maintain your institutional records, academic credentials, and skills inventory.
        </p>
      </div>

      {message && (
        <div
          className={`p-4 rounded-xl flex items-center space-x-2 text-xs font-medium border ${
            message.type === "success"
              ? "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
              : "bg-rose-500/10 text-rose-300 border-rose-500/20"
          }`}
        >
          {message.type === "success" ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          )}
          <span>{message.text}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Academic Credentials Form */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center space-x-2.5 pb-4 border-b border-slate-800 mb-6">
            <UserCheck className="w-5 h-5 text-blue-400" />
            <h2 className="text-sm font-bold text-white">Academic &amp; Role Information</h2>
          </div>

          <form onSubmit={handleProfileSave} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  disabled
                  value={profile?.full_name || ""}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/50 border border-slate-800/80 text-xs text-slate-400 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">
                  Student Roll Number
                </label>
                <input
                  type="text"
                  disabled
                  value={profile?.roll_number || ""}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/50 border border-slate-800/80 text-xs text-slate-400 font-mono cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">
                  Department
                </label>
                <input
                  type="text"
                  disabled
                  value={`${profile?.department_name} (${profile?.department_code})`}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/50 border border-slate-800/80 text-xs text-slate-400 cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">
                  Graduation Year
                </label>
                <input
                  type="text"
                  disabled
                  value={profile?.graduation_year || 2026}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/50 border border-slate-800/80 text-xs text-slate-400 cursor-not-allowed"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Cumulative CGPA (0 - 10 scale)
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="10"
                  required
                  value={cgpa}
                  onChange={(e) => setCgpa(parseFloat(e.target.value) || 0)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Target / Preferred Job Role
                </label>
                <input
                  type="text"
                  required
                  value={preferredRole}
                  onChange={(e) => setPreferredRole(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  placeholder="e.g. Software Development Engineer"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Projects Completed
                </label>
                <input
                  type="number"
                  min="0"
                  value={projectsCount}
                  onChange={(e) => setProjectsCount(parseInt(e.target.value) || 0)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Internships Count
                </label>
                <input
                  type="number"
                  min="0"
                  value={internshipsCount}
                  onChange={(e) => setInternshipsCount(parseInt(e.target.value) || 0)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Certifications Count
                </label>
                <input
                  type="number"
                  min="0"
                  value={certificationsCount}
                  onChange={(e) => setCertificationsCount(parseInt(e.target.value) || 0)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 font-mono"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Bio / Technical Summary
                </label>
                <textarea
                  rows={3}
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none leading-relaxed"
                  placeholder="Summarize your engineering interests and portfolio..."
                />
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={saving}
                className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs flex items-center space-x-2 shadow-lg shadow-blue-600/25 transition disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span>{saving ? "Saving Changes..." : "Save Academic Profile"}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Right Column: Skills Management */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2.5 pb-4 border-b border-slate-800 mb-4">
              <Code2 className="w-5 h-5 text-indigo-400" />
              <h2 className="text-sm font-bold text-white">Skills Inventory</h2>
            </div>

            {/* Add Skill Form */}
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3 mb-5">
              <p className="text-xs font-semibold text-slate-300">Add Skill from Taxonomy</p>

              <div>
                <select
                  value={selectedSkillId}
                  onChange={(e) => setSelectedSkillId(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                >
                  {unselectedSkills.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name} ({s.category})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <select
                  value={proficiency}
                  onChange={(e) => setProficiency(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                >
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Advanced">Advanced</option>
                </select>
              </div>

              <button
                type="button"
                onClick={handleAddSkill}
                disabled={!selectedSkillId}
                className="w-full py-2 px-3 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white flex items-center justify-center space-x-1.5 transition disabled:opacity-50"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Add Skill</span>
              </button>
            </div>

            {/* Current Skills List */}
            <p className="text-xs font-semibold text-slate-400 mb-2">
              Possessed Skills ({profile?.skills.length || 0})
            </p>

            <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
              {profile?.skills && profile.skills.length > 0 ? (
                profile.skills.map((s) => (
                  <div
                    key={s.skill_id}
                    className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between"
                  >
                    <div>
                      <p className="text-xs font-bold text-white">{s.skill_name}</p>
                      <p className="text-[10px] text-slate-400 font-mono">
                        {s.category} &bull; {s.proficiency_level}
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleRemoveSkill(s.skill_id)}
                      className="p-1 rounded text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition"
                      title="Remove skill"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))
              ) : (
                <p className="text-xs text-slate-400 italic">No skills listed yet.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
