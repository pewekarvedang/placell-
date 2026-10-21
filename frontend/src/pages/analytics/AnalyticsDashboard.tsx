import React, { useEffect, useState } from "react";
import { analyticsApi } from "../../services/api";
import { AnalyticsOverview } from "../../types";
import { StatCard } from "../../components/common/StatCard";
import { Badge } from "../../components/common/Badge";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import {
  BarChart3,
  PieChart as PieIcon,
  TrendingUp,
  BrainCircuit,
  Building2,
  GraduationCap,
  Sparkles,
  Calendar
} from "lucide-react";

export const AnalyticsDashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsOverview | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await analyticsApi.getOverview();
        setData(res);
      } catch (err) {
        console.error("Error loading analytics:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // Sentiment chart data
  const sentimentChartData = [
    { name: "Positive", value: data.sentiment_distribution.positive, count: data.sentiment_distribution.positive_count, color: "#10b981" },
    { name: "Neutral", value: data.sentiment_distribution.neutral, count: data.sentiment_distribution.neutral_count, color: "#64748b" },
    { name: "Negative", value: data.sentiment_distribution.negative, count: data.sentiment_distribution.negative_count, color: "#f43f5e" },
  ];

  // Difficulty chart data
  const difficultyChartData = Object.entries(data.interview_difficulty_breakdown).map(([k, v]) => ({
    name: k,
    count: v,
  }));

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Page Header */}
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Institutional Placement &amp; Sentiment Analytics
          </h1>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
            ASTMA Intelligence Engine
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Aggregated quantitative metrics and qualitative NLP signals derived from verified student experiences.
        </p>
      </div>

      {/* Top Level KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Placement Success"
          value={`${data.kpis.overall_placement_rate}%`}
          subtitle={`${data.kpis.total_students} Total Students`}
          icon={TrendingUp}
          color="emerald"
        />
        <StatCard
          title="Average Experience Rating"
          value={`${data.kpis.average_experience_rating} / 5`}
          subtitle="Based on verified reviews"
          icon={GraduationCap}
          color="blue"
        />
        <StatCard
          title="Interview Difficulty Index"
          value={`${data.kpis.average_interview_difficulty} / 5`}
          subtitle="Inferred from round analytics"
          icon={BrainCircuit}
          color="purple"
        />
        <StatCard
          title="Verified Reviews"
          value={data.kpis.verified_experiences_count}
          subtitle={`Across ${data.kpis.total_companies} companies`}
          icon={Building2}
          color="amber"
        />
      </div>

      {/* Charts Row 1: Sentiment Analysis & Top Demanded Skills */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Analysis (ASTMA Module 7) */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
              <div className="flex items-center space-x-2">
                <PieIcon className="w-5 h-5 text-emerald-400" />
                <h2 className="text-sm font-bold text-white">Sentiment Distribution (NLP Output)</h2>
              </div>
              <Badge variant="primary" size="sm">
                ASTMA Module 7
              </Badge>
            </div>
            <p className="text-xs text-slate-400 mb-4">
              Calibrated text polarity scoring across free-form student placement reviews.
            </p>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sentimentChartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={85}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {sentimentChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                    formatter={(val: any) => [`${val}%`, "Share"]}
                  />
                  <Legend wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 pt-4 border-t border-slate-800 text-center">
            <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
              <span className="block text-xs font-bold text-emerald-400">{data.sentiment_distribution.positive}%</span>
              <span className="text-[10px] text-slate-400">Positive</span>
            </div>
            <div className="p-2 rounded-lg bg-slate-800 border border-slate-700">
              <span className="block text-xs font-bold text-slate-300">{data.sentiment_distribution.neutral}%</span>
              <span className="text-[10px] text-slate-400">Neutral</span>
            </div>
            <div className="p-2 rounded-lg bg-rose-500/10 border border-rose-500/20">
              <span className="block text-xs font-bold text-rose-400">{data.sentiment_distribution.negative}%</span>
              <span className="text-[10px] text-slate-400">Negative</span>
            </div>
          </div>
        </div>

        {/* Top Demanded Skills (ASTMA Module 8) */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5 text-blue-400" />
              <h2 className="text-sm font-bold text-white">Top Demanded Skills (Recruiter Mentions)</h2>
            </div>
            <Badge variant="primary" size="sm">
              ASTMA Module 8
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mb-4">
            Extracted from technical interview rounds and requirements specifications.
          </p>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data.top_demanded_skills.slice(0, 7)}
                layout="vertical"
                margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
              >
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="skill_name" type="category" stroke="#94a3b8" fontSize={11} width={80} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                  formatter={(val: any) => [val, "Mentions"]}
                />
                <Bar dataKey="mention_count" fill="#3b82f6" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Charts Row 2: Department Comparison (ES) & Monthly Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Comparison (ES Requirement) */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div className="flex items-center space-x-2">
              <GraduationCap className="w-5 h-5 text-purple-400" />
              <h2 className="text-sm font-bold text-white">Department Placement Comparison (ES)</h2>
            </div>
            <Badge variant="purple" size="sm">
              ES Cohort
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mb-4">
            Placement conversion rates and readiness indices across academic branches.
          </p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.department_metrics}>
                <XAxis dataKey="department_code" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                />
                <Legend wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }} />
                <Bar dataKey="placement_rate" name="Placement Rate %" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="average_readiness" name="Readiness Index %" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Monthly Placement Drive Trends */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div className="flex items-center space-x-2">
              <Calendar className="w-5 h-5 text-amber-400" />
              <h2 className="text-sm font-bold text-white">Drive &amp; Selection Trends</h2>
            </div>
            <Badge variant="warning" size="sm">
              Time Series
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mb-4">
            Monthly trajectory of conducted campus drives and recruited students.
          </p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.monthly_placement_trends}>
                <XAxis dataKey="month" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "12px" }}
                />
                <Legend wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }} />
                <Line type="monotone" dataKey="drives" name="Campus Drives" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="placed" name="Students Placed" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
