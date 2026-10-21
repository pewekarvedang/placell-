import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { analyticsApi, driveApi, experienceApi } from "../../services/api";
import { AnalyticsOverview, PlacementDrive, PlacementExperience } from "../../types";
import { StatCard } from "../../components/common/StatCard";
import { Badge } from "../../components/common/Badge";
import {
  Users,
  Building2,
  Briefcase,
  TrendingUp,
  FileCheck2,
  CheckCircle2,
  Clock,
  ArrowRight,
  ExternalLink,
  ShieldAlert
} from "lucide-react";

export const TPODashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsOverview | null>(null);
  const [drives, setDrives] = useState<PlacementDrive[]>([]);
  const [pendingExps, setPendingExps] = useState<PlacementExperience[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aRes, dRes, pRes] = await Promise.all([
          analyticsApi.getOverview(),
          driveApi.getDrives(),
          experienceApi.getPending(),
        ]);
        setAnalytics(aRes);
        setDrives(dRes);
        setPendingExps(pRes);
      } catch (err) {
        console.error("Error loading TPO dashboard:", err);
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
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Placement Cell Directorate Command Center
            </h1>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
              ES Officer Portal
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Institutional overview of corporate recruitment pipelines, student conversion, and verified experiences.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Link
            to="/moderation"
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white flex items-center space-x-2 transition shadow-lg shadow-indigo-600/25"
          >
            <Clock className="w-4 h-4" />
            <span>Moderation Queue ({pendingExps.length})</span>
          </Link>
          <Link
            to="/analytics"
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            Detailed Analytics &rarr;
          </Link>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Registered Students"
          value={analytics?.kpis.total_students || 0}
          subtitle="All active departments"
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Institutional Placement Rate"
          value={`${analytics?.kpis.overall_placement_rate || 0}%`}
          subtitle="Batch 2026 conversion"
          icon={TrendingUp}
          trend="+5.2% YoY"
          trendPositive={true}
          color="emerald"
        />
        <StatCard
          title="Recruiting Partners"
          value={analytics?.kpis.total_companies || 0}
          subtitle="Product & Service firms"
          icon={Building2}
          color="purple"
        />
        <StatCard
          title="Verified Experiences"
          value={analytics?.kpis.verified_experiences_count || 0}
          subtitle="Indexed in NLP knowledge base"
          icon={FileCheck2}
          color="amber"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Campus Drives */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
            <div className="flex items-center space-x-2">
              <Briefcase className="w-5 h-5 text-blue-400" />
              <h2 className="text-sm font-bold text-white">Campus Placement Drives</h2>
            </div>
            <Link to="/drives" className="text-xs font-semibold text-blue-400 hover:text-blue-300">
              View All ({drives.length}) &rarr;
            </Link>
          </div>

          <div className="space-y-3">
            {drives.slice(0, 5).map((d) => (
              <div
                key={d.id}
                className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-white">{d.company_name}</span>
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
                  <p className="text-xs text-slate-400 mt-0.5">{d.job_role_title}</p>
                  <p className="text-[11px] text-slate-500 font-mono mt-1">
                    Date: {d.drive_date} &bull; Min CGPA: {d.eligibility_cgpa} &bull; Package: {d.ctc_offered_lpa} LPA
                  </p>
                </div>

                <div className="text-right shrink-0">
                  <span className="text-xs font-mono font-bold text-blue-400">
                    {d.applicants_count} Applicants
                  </span>
                  <span className="block text-[10px] text-slate-500">
                    {d.selected_count} Selected
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Hiring Recruiters */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
            <div className="flex items-center space-x-2">
              <Building2 className="w-5 h-5 text-purple-400" />
              <h2 className="text-sm font-bold text-white">Top Recruiters</h2>
            </div>
            <Link to="/companies" className="text-xs font-semibold text-blue-400 hover:text-blue-300">
              Directory &rarr;
            </Link>
          </div>

          <div className="space-y-3">
            {analytics?.top_hiring_companies.slice(0, 5).map((c) => (
              <div
                key={c.company_id}
                className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between"
              >
                <div>
                  <p className="text-xs font-bold text-white">{c.company_name}</p>
                  <p className="text-[10px] text-slate-400">
                    {c.industry} &bull; Up to {c.ctc_max_lpa} LPA
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-bold text-emerald-400">
                    {c.placed_count} Offers
                  </span>
                  <span className="block text-[10px] text-slate-500">
                    {c.total_experiences} reviews
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
