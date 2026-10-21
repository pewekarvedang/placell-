import React, { useEffect, useState } from "react";
import { studentApi, companyApi } from "../../services/api";
import { SkillGapAnalysis, Company } from "../../types";
import { Badge } from "../../components/common/Badge";
import {
  Target,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Sparkles,
  ArrowRight,
  TrendingUp,
  BookOpen
} from "lucide-react";

export const SkillGapView: React.FC = () => {
  const [gapData, setGapData] = useState<SkillGapAnalysis | null>(null);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [gapRes, compsRes] = await Promise.all([
          studentApi.getSkillGap(),
          companyApi.getCompanies(),
        ]);
        setGapData(gapRes);
        setCompanies(compsRes);
      } catch (err) {
        console.error("Error loading skill gap analysis:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Skill-Gap Analyzer &amp; Recommendations
            </h1>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
              ASTMA Module 10 &amp; 12
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic gap analysis matching your student portfolio against industry placement requirements.
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-2.5 rounded-xl">
          <Target className="w-4 h-4 text-blue-400" />
          <span className="text-xs font-semibold text-slate-300">
            Target: <span className="text-white font-bold">{gapData?.target_role}</span>
          </span>
        </div>
      </div>

      {/* Match Score Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Target Competency Overlap
            </span>
            <div className="flex items-baseline space-x-3 mt-1">
              <span className="text-3xl font-extrabold text-white">
                {gapData?.match_percentage}%
              </span>
              <span className="text-xs font-semibold text-slate-300">
                {gapData && gapData.match_percentage >= 70
                  ? "Well-aligned with market expectations"
                  : "Key critical skill gaps detected"}
              </span>
            </div>
          </div>

          <Badge
            variant={gapData && gapData.match_percentage >= 70 ? "success" : "warning"}
            size="md"
          >
            {gapData && gapData.match_percentage >= 70 ? "Strong Alignment" : "Action Required"}
          </Badge>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
          <div
            className={`h-2 rounded-full transition-all duration-700 ${
              gapData && gapData.match_percentage >= 70 ? "bg-emerald-500" : "bg-amber-500"
            }`}
            style={{ width: `${gapData?.match_percentage || 0}%` }}
          ></div>
        </div>
      </div>

      {/* Comparison Grid: Matched vs Missing */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Matched Competencies */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center space-x-2 pb-4 border-b border-slate-800 mb-4">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <h2 className="text-sm font-bold text-white">
              Possessed Competencies ({gapData?.matched_skills.length || 0})
            </h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {gapData?.matched_skills && gapData.matched_skills.length > 0 ? (
              gapData.matched_skills.map((s) => (
                <span
                  key={s}
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500/10 text-emerald-300 border border-emerald-500/20"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span>{s}</span>
                </span>
              ))
            ) : (
              <p className="text-xs text-slate-400 italic">No exact overlaps detected.</p>
            )}
          </div>
        </div>

        {/* Missing / Gaps */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center space-x-2 pb-4 border-b border-slate-800 mb-4">
            <AlertTriangle className="w-5 h-5 text-rose-400" />
            <h2 className="text-sm font-bold text-white">
              Identified Skill Gaps ({gapData?.missing_skills.length || 0})
            </h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {gapData?.missing_skills && gapData.missing_skills.length > 0 ? (
              gapData.missing_skills.map((s) => (
                <span
                  key={s}
                  className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-500/10 text-rose-300 border border-rose-500/20"
                >
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                  <span>{s}</span>
                </span>
              ))
            ) : (
              <p className="text-xs text-emerald-400 italic">
                Zero skill gaps! You meet 100% of benchmark requirements.
              </p>
            )}
          </div>
        </div>
      </div>

      {/* ASTMA Explainable Recommendation Cards */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
          <div className="flex items-center space-x-2.5">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <div>
              <h2 className="text-sm font-bold text-white">
                Explainable Career Recommendations
              </h2>
              <p className="text-[11px] text-slate-400">
                Prioritized based on frequency in verified recruiter evaluations
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {gapData?.recommendations && gapData.recommendations.length > 0 ? (
            gapData.recommendations.map((rec, index) => (
              <div
                key={rec.skill}
                className="p-5 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 transition"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                  <div className="flex items-center space-x-3">
                    <span className="w-6 h-6 rounded-full bg-blue-600/20 text-blue-400 flex items-center justify-center text-xs font-bold font-mono">
                      {index + 1}
                    </span>
                    <h3 className="text-sm font-bold text-white tracking-tight">
                      Master {rec.skill}
                    </h3>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Badge
                      variant={
                        rec.priority === "HIGH"
                          ? "danger"
                          : rec.priority === "MEDIUM"
                          ? "warning"
                          : "neutral"
                      }
                      size="sm"
                    >
                      {rec.priority} Priority
                    </Badge>
                    <span className="text-[11px] text-slate-400 font-mono">
                      Market Demand: <strong className="text-white">{rec.frequency_in_drives}</strong>
                    </span>
                  </div>
                </div>

                {/* Explainable Rationale */}
                <div className="mt-2.5 p-3 rounded-lg bg-slate-900 border border-slate-800/80">
                  <div className="flex items-start space-x-2 text-xs text-slate-300 leading-relaxed">
                    <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    <p>
                      <strong className="text-amber-400">Why recommended: </strong>
                      {rec.rationale}
                    </p>
                  </div>
                </div>

                {/* Actionable Steps */}
                <div className="mt-3 pl-2 border-l-2 border-slate-800 space-y-1">
                  <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                    Action Roadmap:
                  </p>
                  {rec.action_steps.map((step, sIdx) => (
                    <div key={sIdx} className="flex items-center space-x-2 text-xs text-slate-400">
                      <ArrowRight className="w-3 h-3 text-blue-400 shrink-0" />
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-400 italic">
              No recommendations needed &mdash; your skill set satisfies all benchmark role parameters.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};
