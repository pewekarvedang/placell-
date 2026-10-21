import React, { useEffect, useState } from "react";
import { experienceApi } from "../../services/api";
import { PlacementExperience } from "../../types";
import { Badge } from "../../components/common/Badge";
import {
  CheckCircle2,
  XCircle,
  Clock,
  Building2,
  BrainCircuit,
  MessageSquare,
  AlertCircle
} from "lucide-react";

export const ModerationQueue: React.FC = () => {
  const [pending, setPending] = useState<PlacementExperience[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const fetchPending = async () => {
    try {
      const data = await experienceApi.getPending();
      setPending(data);
    } catch (err) {
      console.error("Error loading pending experiences:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPending();
  }, []);

  const handleModeration = async (id: string, status: "VERIFIED" | "REJECTED") => {
    try {
      await experienceApi.verify(id, status, `Verified by Placement Directorate officer on ${new Date().toLocaleDateString()}`);
      setActionMessage(`Experience marked as ${status}.`);
      setPending(pending.filter((p) => p.id !== id));
      setTimeout(() => setActionMessage(null), 3000);
    } catch (err) {
      alert("Error updating experience moderation status.");
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
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Experience Moderation &amp; Verification Queue
            </h1>
            <Badge variant="warning" size="sm">
              {pending.length} Pending
            </Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            (ES Enterprise Workflow) Authorize qualitative student submissions before indexing into college-wide analytics.
          </p>
        </div>
      </div>

      {actionMessage && (
        <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300 flex items-center space-x-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{actionMessage}</span>
        </div>
      )}

      {pending.length === 0 ? (
        <div className="p-12 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-3">
          <CheckCircle2 className="w-10 h-10 text-emerald-400 mx-auto" />
          <h3 className="text-sm font-bold text-white">Queue is Clear!</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            All submitted placement experiences have been reviewed and verified by the placement cell.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {pending.map((exp) => (
            <div
              key={exp.id}
              className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-800">
                <div className="flex items-center space-x-3">
                  <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
                    <Building2 className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">{exp.company_name}</h3>
                    <p className="text-xs text-slate-400">
                      Role: {exp.job_role_title || "Software Engineer"} &bull; Student: {exp.student_roll_number} ({exp.student_department})
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <Badge variant="primary" size="sm">
                    Rating: {exp.overall_rating}/5
                  </Badge>
                  <Badge variant="warning" size="sm">
                    Diff: {exp.difficulty_rating}/5
                  </Badge>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {new Date(exp.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>

              {/* Free-text feedback */}
              <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80">
                <div className="flex items-start space-x-2">
                  <MessageSquare className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
                  <p className="text-xs text-slate-300 leading-relaxed italic">
                    "{exp.free_text_feedback}"
                  </p>
                </div>
                {exp.questions_asked && (
                  <p className="mt-2 text-[11px] text-slate-400 border-t border-slate-900 pt-2">
                    <strong className="text-slate-300">Questions: </strong>
                    {exp.questions_asked}
                  </p>
                )}
              </div>

              {/* NLP preview if parsed */}
              {exp.nlp_result && (
                <div className="flex items-center space-x-2 text-[11px] text-slate-400">
                  <BrainCircuit className="w-3.5 h-3.5 text-indigo-400" />
                  <span>
                    NLP Sentiment: <strong className="text-white">{exp.nlp_result.sentiment_label}</strong> &bull; Extracted Skills: {exp.nlp_result.extracted_skills.join(", ") || "None"}
                  </span>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  onClick={() => handleModeration(exp.id, "REJECTED")}
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 transition flex items-center space-x-1.5"
                >
                  <XCircle className="w-4 h-4" />
                  <span>Reject</span>
                </button>
                <button
                  onClick={() => handleModeration(exp.id, "VERIFIED")}
                  className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white shadow-md shadow-emerald-600/20 transition flex items-center space-x-1.5"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Approve &amp; Index</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
