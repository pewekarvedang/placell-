import React, { useEffect, useState } from "react";
import { companyApi } from "../../services/api";
import { Company } from "../../types";
import { Badge } from "../../components/common/Badge";
import { useAuth } from "../../context/AuthContext";
import {
  Building2,
  Search,
  Star,
  MapPin,
  TrendingUp,
  BrainCircuit,
  BarChart3,
  X,
  ExternalLink,
  Plus,
  CheckCircle2
} from "lucide-react";

export const CompaniesDirectory: React.FC = () => {
  const { role } = useAuth();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [selectedCompAnalytics, setSelectedCompAnalytics] = useState<any | null>(null);
  const [modalLoading, setModalLoading] = useState(false);

  // Registration Modal State for TPO / Admin
  const [showAddModal, setShowAddModal] = useState(false);
  const [newName, setNewName] = useState("");
  const [newIndustry, setNewIndustry] = useState("Software & Cloud");
  const [newType, setNewType] = useState("Product");
  const [newCtcMin, setNewCtcMin] = useState(6.0);
  const [newCtcMax, setNewCtcMax] = useState(18.0);
  const [newLocation, setNewLocation] = useState("Bengaluru / Hyderabad");
  const [newWebsite, setNewWebsite] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [creating, setCreating] = useState(false);
  const [successBanner, setSuccessBanner] = useState<string | null>(null);

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const data = await companyApi.getCompanies();
        setCompanies(data);
      } catch (err) {
        console.error("Error loading companies:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchCompanies();
  }, []);

  const openAnalyticsModal = async (companyId: string) => {
    setModalLoading(true);
    setSelectedCompAnalytics(null);
    try {
      const data = await companyApi.getAnalytics(companyId);
      setSelectedCompAnalytics(data);
    } catch (err) {
      alert("Error loading company analytics");
    } finally {
      setModalLoading(false);
    }
  };

  const handleCreateCompany = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    setCreating(true);
    try {
      const created = await companyApi.createCompany({
        name: newName.trim(),
        industry: newIndustry.trim(),
        company_type: newType,
        ctc_min_lpa: Number(newCtcMin),
        ctc_max_lpa: Number(newCtcMax),
        location: newLocation.trim(),
        website: newWebsite.trim() || undefined,
        description: newDescription.trim() || undefined,
      });
      setCompanies([created, ...companies]);
      setShowAddModal(false);
      setNewName("");
      setNewDescription("");
      setSuccessBanner(`Successfully registered "${created.name}" as an active recruiting partner!`);
      setTimeout(() => setSuccessBanner(null), 4000);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to register company.");
    } finally {
      setCreating(false);
    }
  };

  const filtered = companies.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.industry.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Corporate Recruiting Partners Directory
            </h1>
            <Badge variant="primary" size="sm">
              {companies.length} Registered Recruiters
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Explore recruiting organizations, compensation brackets, interview difficulty metrics, and skill demand benchmarks.
          </p>
        </div>

        {(role === "TPO" || role === "ADMIN") && (
          <button
            type="button"
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white flex items-center space-x-2 transition shadow-lg shadow-blue-600/25 shrink-0 self-start sm:self-auto"
          >
            <Plus className="w-4 h-4" />
            <span>Register New Company</span>
          </button>
        )}
      </div>

      {successBanner && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{successBanner}</span>
        </div>
      )}

      {/* Search */}
      <div className="relative max-w-md">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
          <Search className="w-4 h-4" />
        </div>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter by company name or industry..."
          className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Grid */}
      {loading ? (
        <div className="p-12 flex justify-center">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((c) => (
            <div
              key={c.id}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600/20 to-indigo-600/20 text-blue-400 border border-blue-500/20 flex items-center justify-center font-bold text-sm">
                      <Building2 className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-white">{c.name}</h3>
                      <p className="text-[11px] text-slate-400">{c.industry}</p>
                    </div>
                  </div>
                  <Badge variant={c.company_type === "Product" ? "purple" : "neutral"} size="sm">
                    {c.company_type}
                  </Badge>
                </div>

                <p className="mt-3 text-xs text-slate-400 line-clamp-2 leading-relaxed">
                  {c.description || "Leading recruitment partner conducting regular campus placement drives."}
                </p>

                <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-1.5 text-xs text-slate-400">
                  <div className="flex items-center justify-between">
                    <span>CTC Compensation:</span>
                    <strong className="text-white font-mono">
                      {c.ctc_min_lpa} - {c.ctc_max_lpa} LPA
                    </strong>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Location:</span>
                    <span className="text-slate-300 truncate max-w-[150px]">{c.location || "Pan-India"}</span>
                  </div>
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 font-mono">
                  {c.roles_count} Open Roles &bull; {c.experiences_count} Reviews
                </span>
                <button
                  type="button"
                  onClick={() => openAnalyticsModal(c.id)}
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600/10 hover:bg-blue-600/20 text-blue-400 border border-blue-500/20 transition flex items-center space-x-1"
                >
                  <BarChart3 className="w-3.5 h-3.5" />
                  <span>Company Intel</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal for Deep-Dive Company Intelligence */}
      {(selectedCompAnalytics || modalLoading) && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setSelectedCompAnalytics(null)}
              className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>

            {modalLoading ? (
              <div className="py-12 flex justify-center">
                <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : selectedCompAnalytics && (
              <div className="space-y-6">
                <div>
                  <div className="flex items-center space-x-2">
                    <h2 className="text-lg font-extrabold text-white">
                      {selectedCompAnalytics.company_name}
                    </h2>
                    <Badge variant="primary" size="sm">
                      {selectedCompAnalytics.industry}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    ASTMA Intelligence Report generated from {selectedCompAnalytics.total_experiences} verified student evaluations.
                  </p>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                    <span className="text-[10px] uppercase text-slate-400 font-bold">Avg Rating</span>
                    <p className="text-lg font-bold text-amber-400 mt-0.5">
                      {selectedCompAnalytics.average_overall_rating} / 5
                    </p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                    <span className="text-[10px] uppercase text-slate-400 font-bold">Difficulty</span>
                    <p className="text-lg font-bold text-rose-400 mt-0.5">
                      {selectedCompAnalytics.average_difficulty_rating} / 5
                    </p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-center">
                    <span className="text-[10px] uppercase text-slate-400 font-bold">Sentiment</span>
                    <p className="text-lg font-bold text-emerald-400 mt-0.5">
                      {selectedCompAnalytics.positive_sentiment_percent}% Pos
                    </p>
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                    Top Skills Demanded in Interviews
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedCompAnalytics.top_demanded_skills.map((s: any) => (
                      <span
                        key={s.skill}
                        className="px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-950 border border-slate-800 text-slate-200"
                      >
                        {s.skill} ({s.count} mentions)
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                    Frequently Tested Interview Topics
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedCompAnalytics.frequent_interview_topics.map((t: string) => (
                      <Badge key={t} variant="purple" size="sm">
                        {t}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Modal for Registering New Company (TPO / Admin) */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowAddModal(false)}
              className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center space-x-2.5 mb-5">
              <div className="p-2 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Register Recruiting Organization</h3>
                <p className="text-xs text-slate-400">Add a corporate partner to the institutional placement portal.</p>
              </div>
            </div>

            <form onSubmit={handleCreateCompany} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Company Name *</label>
                <input
                  type="text"
                  required
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  placeholder="e.g. NVIDIA Corporation, Atlassian, Morgan Stanley"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Industry Sector *</label>
                  <input
                    type="text"
                    required
                    value={newIndustry}
                    onChange={(e) => setNewIndustry(e.target.value)}
                    placeholder="e.g. AI & GPUs, Fintech, SaaS"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Company Type</label>
                  <select
                    value={newType}
                    onChange={(e) => setNewType(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="Product">Product</option>
                    <option value="Service">Service</option>
                    <option value="Startup">Startup</option>
                    <option value="Consulting">Consulting</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Min CTC (LPA)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="1"
                    value={newCtcMin}
                    onChange={(e) => setNewCtcMin(parseFloat(e.target.value) || 0)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Max CTC (LPA)</label>
                  <input
                    type="number"
                    step="0.5"
                    min="1"
                    value={newCtcMax}
                    onChange={(e) => setNewCtcMax(parseFloat(e.target.value) || 0)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Work Location</label>
                <input
                  type="text"
                  value={newLocation}
                  onChange={(e) => setNewLocation(e.target.value)}
                  placeholder="e.g. Bengaluru / Pune / Remote"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Official Career Website</label>
                <input
                  type="url"
                  value={newWebsite}
                  onChange={(e) => setNewWebsite(e.target.value)}
                  placeholder="https://careers.company.com"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Company Description &amp; Overview</label>
                <textarea
                  rows={3}
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  placeholder="Brief summary of corporate recruitment focus, domain, and work culture..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 resize-none"
                />
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="px-5 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white transition flex items-center space-x-1.5 shadow-lg shadow-blue-600/25"
                >
                  {creating ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <>
                      <Plus className="w-4 h-4" />
                      <span>Register Partner</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
