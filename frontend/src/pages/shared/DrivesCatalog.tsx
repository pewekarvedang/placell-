import React, { useEffect, useState } from "react";
import { driveApi, studentApi, companyApi } from "../../services/api";
import { PlacementDrive, StudentProfile, Company } from "../../types";
import { Badge } from "../../components/common/Badge";
import { useAuth } from "../../context/AuthContext";
import {
  Briefcase,
  Building2,
  Calendar,
  DollarSign,
  GraduationCap,
  Users,
  CheckCircle2,
  AlertCircle,
  Plus,
  X,
  UserCheck,
  Check,
  Ban
} from "lucide-react";

export const DrivesCatalog: React.FC = () => {
  const { role } = useAuth();
  const [drives, setDrives] = useState<PlacementDrive[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [applyingId, setApplyingId] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // New Drive Modal State (TPO / Admin)
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [selectedCompanyId, setSelectedCompanyId] = useState("");
  const [companyRoles, setCompanyRoles] = useState<any[]>([]);
  const [selectedRoleId, setSelectedRoleId] = useState("");
  const [driveTitle, setDriveTitle] = useState("");
  const [driveDate, setDriveDate] = useState(new Date(Date.now() + 7 * 86400000).toISOString().split("T")[0]);
  const [driveStatus, setDriveStatus] = useState("UPCOMING");
  const [eligibilityCgpa, setEligibilityCgpa] = useState(6.5);
  const [ctcOffered, setCtcOffered] = useState(8.0);
  const [roundsDesc, setRoundsDesc] = useState("Round 1: Online Assessment (Coding & MCQs), Round 2: Technical Interview, Round 3: HR Discussion");
  const [scheduling, setScheduling] = useState(false);

  // Applicants Modal State
  const [showApplicantsModal, setShowApplicantsModal] = useState(false);
  const [activeDriveTitle, setActiveDriveTitle] = useState("");
  const [applicants, setApplicants] = useState<any[]>([]);
  const [loadingApplicants, setLoadingApplicants] = useState(false);
  const [updatingAppId, setUpdatingAppId] = useState<string | null>(null);

  const fetchDrives = async () => {
    try {
      const drivesData = await driveApi.getDrives();
      setDrives(drivesData);
    } catch (err) {
      console.error("Error loading drives:", err);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [drivesData, compsData] = await Promise.all([
          driveApi.getDrives(),
          companyApi.getCompanies(),
        ]);
        setDrives(drivesData);
        setCompanies(compsData);
        if (compsData.length > 0) {
          setSelectedCompanyId(compsData[0].id);
        }

        if (role === "STUDENT") {
          try {
            const p = await studentApi.getProfile();
            setProfile(p);
          } catch {
            // non-student profile lookup ignored
          }
        }
      } catch (err) {
        console.error("Error loading drives catalog:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [role]);

  // When selected company changes in schedule modal, load roles
  useEffect(() => {
    if (!selectedCompanyId) return;
    const fetchRoles = async () => {
      try {
        const roles = await companyApi.getRoles(selectedCompanyId);
        setCompanyRoles(roles);
        if (roles.length > 0) {
          setSelectedRoleId(roles[0].id);
          setDriveTitle(`${roles[0].title} Campus Drive`);
        } else {
          setSelectedRoleId("");
          setDriveTitle("Software Development Engineer Campus Drive");
        }
      } catch {
        setCompanyRoles([]);
      }
    };
    fetchRoles();
  }, [selectedCompanyId]);

  const handleApply = async (driveId: string) => {
    setApplyingId(driveId);
    setMessage(null);
    try {
      await driveApi.apply(driveId);
      setMessage({ type: "success", text: "Successfully registered application for this drive!" });
      fetchDrives();
    } catch (err: any) {
      setMessage({ type: "error", text: err.response?.data?.detail || "Could not apply for drive." });
    } finally {
      setApplyingId(null);
    }
  };

  const handleScheduleDrive = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCompanyId) return;
    setScheduling(true);
    try {
      // Find role or fall back
      let roleId = selectedRoleId;
      if (!roleId && companyRoles.length > 0) {
        roleId = companyRoles[0].id;
      }
      // If company has no job role, fallback to any or first company's role
      if (!roleId) {
        alert("This company does not have an active job role configured yet. Please configure a job role first.");
        setScheduling(false);
        return;
      }

      await driveApi.createDrive({
        company_id: selectedCompanyId,
        job_role_id: roleId,
        title: driveTitle.trim(),
        drive_date: driveDate,
        status: driveStatus,
        eligibility_cgpa: Number(eligibilityCgpa),
        ctc_offered_lpa: Number(ctcOffered),
        rounds_description: roundsDesc.trim(),
      });

      setMessage({ type: "success", text: `Campus drive "${driveTitle}" scheduled successfully!` });
      setShowScheduleModal(false);
      fetchDrives();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error scheduling placement drive.");
    } finally {
      setScheduling(false);
    }
  };

  const openApplicantsModal = async (drive: PlacementDrive) => {
    setActiveDriveTitle(drive.title);
    setShowApplicantsModal(true);
    setLoadingApplicants(true);
    try {
      const data = await driveApi.getApplications(drive.id);
      setApplicants(data);
    } catch (err) {
      alert("Error fetching applicants for this drive.");
    } finally {
      setLoadingApplicants(false);
    }
  };

  const handleStatusUpdate = async (applicationId: string, newStatus: string) => {
    setUpdatingAppId(applicationId);
    try {
      await driveApi.updateApplicationStatus(applicationId, newStatus);
      setApplicants((prev) =>
        prev.map((a) => (a.id === applicationId ? { ...a, status: newStatus } : a))
      );
      fetchDrives();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to update status.");
    } finally {
      setUpdatingAppId(null);
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Campus Placement Drives Catalog
            </h1>
            <Badge variant="primary" size="sm">
              {drives.length} Drives
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Explore upcoming and active recruiter drives, check eligibility thresholds, and register your application.
          </p>
        </div>

        {(role === "TPO" || role === "ADMIN") && (
          <button
            type="button"
            onClick={() => setShowScheduleModal(true)}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white flex items-center space-x-2 transition shadow-lg shadow-blue-600/25 shrink-0 self-start sm:self-auto"
          >
            <Plus className="w-4 h-4" />
            <span>Schedule New Drive</span>
          </button>
        )}
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

      {loading ? (
        <div className="p-12 flex justify-center">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {drives.map((d) => {
            const isEligible = profile ? profile.cgpa >= d.eligibility_cgpa : true;
            return (
              <div
                key={d.id}
                className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm hover:border-slate-700/80 transition flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="space-y-2">
                  <div className="flex items-center space-x-2.5">
                    <h3 className="text-sm font-bold text-white">{d.company_name}</h3>
                    <Badge
                      variant={
                        d.status === "ACTIVE"
                          ? "success"
                          : d.status === "UPCOMING"
                          ? "primary"
                          : "neutral"
                      }
                      size="sm"
                    >
                      {d.status}
                    </Badge>
                  </div>

                  <p className="text-xs font-medium text-slate-300">{d.title}</p>
                  <p className="text-[11px] text-slate-400">{d.rounds_description}</p>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-1 font-mono">
                    <span className="flex items-center space-x-1">
                      <Calendar className="w-3.5 h-3.5 text-slate-500" />
                      <span>{d.drive_date}</span>
                    </span>
                    <span className="flex items-center space-x-1">
                      <GraduationCap className="w-3.5 h-3.5 text-slate-500" />
                      <span>Min CGPA: <strong className="text-white">{d.eligibility_cgpa}</strong></span>
                    </span>
                    <span className="flex items-center space-x-1">
                      <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
                      <span>CTC: <strong className="text-emerald-400">{d.ctc_offered_lpa} LPA</strong></span>
                    </span>
                  </div>
                </div>

                <div className="flex flex-col sm:items-end justify-between shrink-0 space-y-3">
                  <div className="text-right text-xs">
                    <span className="font-mono font-bold text-blue-400">
                      {d.applicants_count} Applied
                    </span>
                    <span className="block text-[10px] text-slate-500">
                      {d.selected_count} Selected
                    </span>
                  </div>

                  <div className="flex items-center space-x-2">
                    {(role === "TPO" || role === "ADMIN" || role === "FACULTY") && (
                      <button
                        type="button"
                        onClick={() => openApplicantsModal(d)}
                        className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center space-x-1.5"
                      >
                        <Users className="w-3.5 h-3.5 text-blue-400" />
                        <span>Applicants ({d.applicants_count})</span>
                      </button>
                    )}

                    {role === "STUDENT" && (
                      <button
                        type="button"
                        onClick={() => handleApply(d.id)}
                        disabled={!isEligible || applyingId === d.id || d.status === "COMPLETED"}
                        className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
                          d.status === "COMPLETED"
                            ? "bg-slate-800 text-slate-500 cursor-not-allowed"
                            : !isEligible
                            ? "bg-rose-500/10 text-rose-400 border border-rose-500/20 cursor-not-allowed"
                            : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/20"
                        }`}
                      >
                        {applyingId === d.id
                          ? "Registering..."
                          : d.status === "COMPLETED"
                          ? "Drive Concluded"
                          : !isEligible
                          ? `Ineligible (CGPA < ${d.eligibility_cgpa})`
                          : "Apply for Drive"}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal for Scheduling a New Drive (TPO / Admin) */}
      {showScheduleModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowScheduleModal(false)}
              className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center space-x-2.5 mb-5">
              <div className="p-2 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <Calendar className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Schedule Campus Placement Drive</h3>
                <p className="text-xs text-slate-400">Configure drive date, eligibility criteria, and rounds structure.</p>
              </div>
            </div>

            <form onSubmit={handleScheduleDrive} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Company Partner *</label>
                <select
                  value={selectedCompanyId}
                  onChange={(e) => setSelectedCompanyId(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                >
                  {companies.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.industry})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Target Job Role *</label>
                {companyRoles.length > 0 ? (
                  <select
                    value={selectedRoleId}
                    onChange={(e) => {
                      setSelectedRoleId(e.target.value);
                      const r = companyRoles.find((x) => x.id === e.target.value);
                      if (r) setDriveTitle(`${r.title} Campus Drive`);
                    }}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                  >
                    {companyRoles.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.title} (Min CGPA: {r.min_cgpa})
                      </option>
                    ))}
                  </select>
                ) : (
                  <p className="text-xs text-amber-400 italic">
                    Loading or no explicit role found. Defaulting to general campus drive.
                  </p>
                )}
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Drive Title *</label>
                <input
                  type="text"
                  required
                  value={driveTitle}
                  onChange={(e) => setDriveTitle(e.target.value)}
                  placeholder="e.g. SDE-1 Recruitment Drive 2026"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Drive Date *</label>
                  <input
                    type="date"
                    required
                    value={driveDate}
                    onChange={(e) => setDriveDate(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Drive Status</label>
                  <select
                    value={driveStatus}
                    onChange={(e) => setDriveStatus(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="UPCOMING">Upcoming</option>
                    <option value="ACTIVE">Active</option>
                    <option value="COMPLETED">Completed</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Min CGPA Cutoff</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="10"
                    value={eligibilityCgpa}
                    onChange={(e) => setEligibilityCgpa(parseFloat(e.target.value) || 0)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Offered CTC (LPA)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="1"
                    value={ctcOffered}
                    onChange={(e) => setCtcOffered(parseFloat(e.target.value) || 0)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Interview Rounds Structure</label>
                <textarea
                  rows={2}
                  value={roundsDesc}
                  onChange={(e) => setRoundsDesc(e.target.value)}
                  placeholder="Outline the sequence of evaluation rounds..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 resize-none"
                />
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowScheduleModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={scheduling}
                  className="px-5 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white transition flex items-center space-x-1.5 shadow-lg shadow-blue-600/25"
                >
                  {scheduling ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <>
                      <Calendar className="w-4 h-4" />
                      <span>Schedule Drive</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal for Viewing & Moderating Drive Applicants (TPO / Faculty / Admin) */}
      {showApplicantsModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowApplicantsModal(false)}
              className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center space-x-2.5 mb-5">
              <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <Users className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Registered Applicants</h3>
                <p className="text-xs text-slate-400">{activeDriveTitle}</p>
              </div>
            </div>

            {loadingApplicants ? (
              <div className="py-12 flex justify-center">
                <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : applicants.length === 0 ? (
              <div className="py-12 text-center text-slate-400 space-y-2">
                <Users className="w-8 h-8 text-slate-600 mx-auto" />
                <p className="text-xs">No students have applied to this drive yet.</p>
              </div>
            ) : (
              <div className="divide-y divide-slate-800/80">
                {applicants.map((a) => (
                  <div key={a.id} className="py-3.5 flex items-center justify-between gap-3">
                    <div>
                      <p className="text-xs font-bold text-white">{a.student_name}</p>
                      <div className="flex items-center space-x-2 text-[11px] text-slate-400 font-mono mt-0.5">
                        <span>Roll: {a.student_roll_number}</span>
                        <span>&bull;</span>
                        <span>CGPA: <strong className="text-slate-200">{a.student_cgpa}</strong></span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <Badge
                        variant={
                          a.status === "SELECTED"
                            ? "success"
                            : a.status === "SHORTLISTED"
                            ? "primary"
                            : a.status === "REJECTED"
                            ? "danger"
                            : "neutral"
                        }
                        size="sm"
                      >
                        {a.status}
                      </Badge>

                      {(role === "TPO" || role === "ADMIN") && (
                        <div className="flex items-center space-x-1.5">
                          {a.status !== "SELECTED" && (
                            <button
                              type="button"
                              disabled={updatingAppId === a.id}
                              onClick={() => handleStatusUpdate(a.id, "SELECTED")}
                              className="px-2 py-1 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/20 transition flex items-center space-x-1"
                              title="Mark Selected"
                            >
                              <Check className="w-3 h-3" />
                              <span>Select</span>
                            </button>
                          )}
                          {a.status !== "SHORTLISTED" && a.status !== "SELECTED" && (
                            <button
                              type="button"
                              disabled={updatingAppId === a.id}
                              onClick={() => handleStatusUpdate(a.id, "SHORTLISTED")}
                              className="px-2 py-1 rounded text-[11px] font-semibold bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20 transition"
                            >
                              Shortlist
                            </button>
                          )}
                          {a.status !== "REJECTED" && (
                            <button
                              type="button"
                              disabled={updatingAppId === a.id}
                              onClick={() => handleStatusUpdate(a.id, "REJECTED")}
                              className="px-2 py-1 rounded text-[11px] font-semibold bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 border border-rose-500/20 transition flex items-center space-x-1"
                              title="Mark Rejected"
                            >
                              <Ban className="w-3 h-3" />
                              <span>Reject</span>
                            </button>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};