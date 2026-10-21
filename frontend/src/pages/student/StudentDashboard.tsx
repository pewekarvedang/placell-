import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { studentApi, experienceApi } from "../../services/api";
import { StudentProfile, ReadinessEvaluation, PlacementExperience } from "../../types";
import { StatCard } from "../../components/common/StatCard";
import { Badge } from "../../components/common/Badge";
import {
  GraduationCap,
  Sparkles,
  Target,
  FileCheck,
  TrendingUp,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Code2
} from "lucide-react";

export const StudentDashboard: React.FC = () => {
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [readiness, setReadiness] = useState<ReadinessEvaluation | null>(null);
  const [myExperiences, setMyExperiences] = useState<PlacementExperience[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profData, readData, expData] = await Promise.all([
          studentApi.getProfile(),
          studentApi.getReadiness(),
          experienceApi.getMy(),
        ]);
        setProfile(profData);
        setReadiness(readData);
        setMyExperiences(expData);
      } catch (err) {
        console.error("Error loading student dashboard:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs text-slate-400">Loading student analytics...</p>
        </div>
      </div>
    );
  }

  const getTierColor = (tier?: string) => {
    switch (tier) {
      case "STRONG":
        return "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";
      case "PLACEMENT_READY":
        return "text-blue-400 bg-blue-500/10 border-blue-500/20";
      case "DEVELOPING":
        return "text-amber-400 bg-amber-500/10 border-amber-500/20";
      default:
        return "text-rose-400 bg-rose-500/10 border-rose-500/20";
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Welcome Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-blue-900/40 via-indigo-900/20 to-slate-900 border border-slate-800 p-6 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-white">
              Welcome back, {profile?.full_name}!
            </h1>
            <Badge variant="primary" size="sm">Roll: {profile?.roll_number}</Badge>
          </div>
          <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
            {profile?.department_name} ({profile?.department_code}) &bull; Target Career Benchmark:{" "}
            <span className="font-semibold text-white">{profile?.preferred_role_title}</span>
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Link
            to="/skill-gap"
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/25 flex items-center space-x-2 transition"
          >
            <Target className="w-4 h-4" />
            <span>Analyze Skill-Gap</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/submit-experience"
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Log Interview
          </Link>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Academic CGPA"
          value={profile?.cgpa.toFixed(2) || "0.00"}
          subtitle="Out of 10.0 scale"
          icon={GraduationCap}
          color="blue"
        />
        <StatCard
          title="Verified Skills"
          value={profile?.skills.length || 0}
          subtitle="In your technical profile"
          icon={Code2}
          color="emerald"
        />
        <StatCard
          title="Portfolio Projects"
          value={profile?.projects_count || 0}
          subtitle={`${profile?.internships_count || 0} industry internship(s)`}
          icon={TrendingUp}
          color="purple"
        />
        <StatCard
          title="Submitted Reviews"
          value={myExperiences.length}
          subtitle="Evaluated by NLP pipeline"
          icon={FileCheck}
          color="amber"
        />
      </div>

      {/* ASTMA Placement Readiness Model Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Score & Gauge Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                ASTMA AI Readiness Model
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Supervised ML
              </span>
            </div>

            <div className="mt-6 flex flex-col items-center text-center">
              <div className="relative w-36 h-36 flex items-center justify-center">
                {/* Visual circular representation */}
                <div className="w-32 h-32 rounded-full border-8 border-slate-800 flex items-center justify-center">
                  <div className="text-center">
                    <span className="text-4xl font-extrabold text-white tracking-tight">
                      {readiness?.readiness_percentage}%
                    </span>
                    <span className="block text-[10px] uppercase font-semibold text-slate-400 mt-0.5">
                      Readiness
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-4">
                <span
                  className={`inline-block px-3 py-1 rounded-full text-xs font-bold border ${getTierColor(
                    readiness?.readiness_tier
                  )}`}
                >
                  {readiness?.readiness_tier_display}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800/80">
            <div className="flex items-start space-x-2 text-[11px] text-slate-400 leading-relaxed">
              <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>
                {readiness?.ethical_safeguard_notice}
              </span>
            </div>
          </div>
        </div>

        {/* Feature Breakdown Explanation */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Explainable Feature Contributions</h3>
              <p className="text-xs text-slate-400">
                Breakdown of how your academic and technical profile drives the readiness estimate
              </p>
            </div>
            <Link
              to="/profile"
              className="text-xs font-semibold text-blue-400 hover:text-blue-300 transition"
            >
              Update Profile &rarr;
            </Link>
          </div>

          <div className="space-y-4">
            {readiness?.feature_breakdown &&
              Object.entries(readiness.feature_breakdown).map(([key, item]) => (
                <div key={key} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-bold text-slate-200 capitalize">
                      {key.replace(/_/g, " ")}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-mono font-semibold text-blue-400">
                        {item.score}%
                      </span>
                      <span className="text-[10px] text-slate-400">
                        (Weight: {item.weight})
                      </span>
                    </div>
                  </div>
                  {/* Progress bar */}
                  <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-blue-500 h-1.5 rounded-full transition-all duration-500"
                      style={{ width: `${item.score}%` }}
                    ></div>
                  </div>
                  <p className="mt-2 text-[11px] text-slate-400">{item.description}</p>
                </div>
              ))}
          </div>
        </div>
      </div>

      {/* Target Skills Summary */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-white">Your Technical Skills Inventory</h3>
            <p className="text-xs text-slate-400">
              Logged in your profile and recognized by our NLP match taxonomy
            </p>
          </div>
          <Link
            to="/profile"
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            + Add New Skill
          </Link>
        </div>

        <div className="flex flex-wrap gap-2">
          {profile?.skills && profile.skills.length > 0 ? (
            profile.skills.map((s) => (
              <span
                key={s.skill_id}
                className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-950 border border-slate-800 text-slate-200"
              >
                <span>{s.skill_name}</span>
                <span className="text-[10px] text-slate-400 bg-slate-800 px-1.5 py-0.2 rounded font-mono">
                  {s.proficiency_level}
                </span>
              </span>
            ))
          ) : (
            <p className="text-xs text-slate-400 italic">
              No skills added yet. Head to your profile to add skills!
            </p>
          )}
        </div>
      </div>
    </div>
  );
};
