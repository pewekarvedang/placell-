import React, { useEffect, useState } from "react";
import { experienceApi, companyApi } from "../../services/api";
import { PlacementExperience, Company } from "../../types";
import { Badge } from "../../components/common/Badge";
import {
  ScrollText,
  Search,
  Star,
  BrainCircuit,
  Building2,
  Calendar,
  MessageSquare,
  HelpCircle,
  Filter
} from "lucide-react";

export const ExperiencesList: React.FC = () => {
  const [experiences, setExperiences] = useState<PlacementExperience[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [search, setSearch] = useState("");
  const [selectedCompany, setSelectedCompany] = useState<string>("");
  const [loading, setLoading] = useState(true);

  const fetchExperiences = async () => {
    setLoading(true);
    try {
      const data = await experienceApi.getVerified(search || undefined, selectedCompany || undefined);
      setExperiences(data);
    } catch (err) {
      console.error("Error loading experiences:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const comps = await companyApi.getCompanies();
        setCompanies(comps);
        const data = await experienceApi.getVerified();
        setExperiences(data);
      } catch (err) {
        console.error("Error initializing experiences list:", err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchExperiences();
  };

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Placement Experiences Knowledge Base
          </h1>
          <Badge variant="primary" size="sm">
            {experiences.length} Verified Records
          </Badge>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Explore real interview accounts, coding questions, and technical topics tested by campus recruiters.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <form onSubmit={handleSearchSubmit} className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-sm">
        <div className="sm:col-span-2 relative">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
            <Search className="w-4 h-4" />
          </div>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search company, job role, or keywords (e.g. Python, SQL, Trees)..."
            className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="flex space-x-2">
          <select
            value={selectedCompany}
            onChange={(e) => setSelectedCompany(e.target.value)}
            className="flex-1 px-3 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
          >
            <option value="">All Companies</option>
            {companies.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs shadow-md shadow-blue-600/20 transition flex items-center space-x-1.5"
          >
            <Filter className="w-3.5 h-3.5" />
            <span>Filter</span>
          </button>
        </div>
      </form>

      {/* Experiences List */}
      {loading ? (
        <div className="p-12 flex justify-center">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : experiences.length === 0 ? (
        <div className="p-12 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-2">
          <ScrollText className="w-8 h-8 text-slate-500 mx-auto" />
          <p className="text-xs text-slate-400">No experiences matching current search criteria.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {experiences.map((exp) => (
            <div
              key={exp.id}
              className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm hover:border-slate-700/80 transition space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold text-sm">
                    <Building2 className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">{exp.company_name}</h3>
                    <p className="text-xs text-slate-400">
                      {exp.job_role_title || "Software Engineer"} &bull; Contributed by {exp.student_roll_number} ({exp.student_department})
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <div className="flex items-center space-x-1 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-md text-amber-400 text-xs font-bold">
                    <Star className="w-3.5 h-3.5 fill-amber-400" />
                    <span>{exp.overall_rating} / 5</span>
                  </div>

                  <Badge variant={exp.difficulty_rating >= 4 ? "danger" : exp.difficulty_rating <= 2 ? "success" : "warning"} size="sm">
                    Diff: {exp.difficulty_rating}/5
                  </Badge>

                  {exp.is_placed && (
                    <Badge variant="success" size="sm">
                      Placed / Offered
                    </Badge>
                  )}
                </div>
              </div>

              {/* Free text feedback */}
              <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800">
                <p className="text-xs text-slate-300 leading-relaxed">
                  "{exp.free_text_feedback}"
                </p>

                {exp.questions_asked && (
                  <div className="mt-3 pt-3 border-t border-slate-900 flex items-start space-x-2 text-xs text-slate-400">
                    <HelpCircle className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                    <div>
                      <strong className="text-slate-300">Questions Asked: </strong>
                      <span>{exp.questions_asked}</span>
                    </div>
                  </div>
                )}
              </div>

              {/* ASTMA NLP Results & Rounds Footer */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-1">
                {/* Extracted skills & topics */}
                {exp.nlp_result ? (
                  <div className="flex items-center space-x-2 flex-wrap gap-y-1">
                    <BrainCircuit className="w-4 h-4 text-indigo-400 shrink-0" />
                    <span className="text-[11px] font-semibold text-slate-400">Skills Extracted:</span>
                    {exp.nlp_result.extracted_skills.map((sk) => (
                      <span key={sk} className="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20">
                        {sk}
                      </span>
                    ))}
                    <Badge
                      variant={
                        exp.nlp_result.sentiment_label === "POSITIVE"
                          ? "success"
                          : exp.nlp_result.sentiment_label === "NEGATIVE"
                          ? "danger"
                          : "neutral"
                      }
                      size="sm"
                    >
                      {exp.nlp_result.sentiment_label} ({(exp.nlp_result.sentiment_score * 100).toFixed(0)}%)
                    </Badge>
                  </div>
                ) : (
                  <span className="text-[11px] text-slate-500">Structured Rounds: {exp.rounds_count}</span>
                )}

                <span className="text-[10px] font-mono text-slate-500 shrink-0">
                  Logged: {new Date(exp.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
