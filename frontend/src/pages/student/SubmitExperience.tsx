import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { companyApi, experienceApi } from "../../services/api";
import { Company, PlacementExperience } from "../../types";
import { Badge } from "../../components/common/Badge";
import {
  FilePlus,
  Star,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Plus,
  Trash2,
  ArrowRight,
  BrainCircuit,
  MessageSquare
} from "lucide-react";

export const SubmitExperience: React.FC = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submittedExp, setSubmittedExp] = useState<PlacementExperience | null>(null);

  // Form Fields
  const [companyId, setCompanyId] = useState("");
  const [overallRating, setOverallRating] = useState(4);
  const [difficultyRating, setDifficultyRating] = useState(3);
  const [questionsAsked, setQuestionsAsked] = useState("");
  const [skillsTested, setSkillsTested] = useState("");
  const [feedback, setFeedback] = useState("");
  const [isPlaced, setIsPlaced] = useState(true);

  // Dynamic Rounds
  const [rounds, setRounds] = useState<Array<{ round_number: number; round_type: any; round_title: string; difficulty: number }>>([
    { round_number: 1, round_type: "CODING", round_title: "Online Assessment", difficulty: 3 },
    { round_number: 2, round_type: "TECHNICAL_INTERVIEW", round_title: "Technical Interview 1", difficulty: 4 },
  ]);

  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const data = await companyApi.getCompanies();
        setCompanies(data);
        if (data.length > 0) {
          setCompanyId(data[0].id);
        }
      } catch (err) {
        console.error("Error loading companies:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchCompanies();
  }, []);

  const addRound = () => {
    setRounds([
      ...rounds,
      {
        round_number: rounds.length + 1,
        round_type: "TECHNICAL_INTERVIEW",
        round_title: `Round ${rounds.length + 1}`,
        difficulty: 3,
      },
    ]);
  };

  const removeRound = (index: number) => {
    if (rounds.length <= 1) return;
    const nextRounds = rounds.filter((_, i) => i !== index).map((r, i) => ({ ...r, round_number: i + 1 }));
    setRounds(nextRounds);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback.trim()) {
      setError("Please provide your qualitative interview feedback for NLP processing.");
      return;
    }
    setError(null);
    setSubmitting(true);

    try {
      const payload = {
        company_id: companyId,
        overall_rating: overallRating,
        difficulty_rating: difficultyRating,
        rounds_count: rounds.length,
        questions_asked: questionsAsked,
        skills_tested: skillsTested,
        free_text_feedback: feedback,
        is_placed: isPlaced,
        rounds: rounds,
      };
      const res = await experienceApi.submit(payload);
      setSubmittedExp(res);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // If submitted successfully, display live ASTMA NLP result breakdown
  if (submittedExp) {
    return (
      <div className="p-8 max-w-4xl mx-auto space-y-6">
        <div className="p-6 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-center space-y-3">
          <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 mx-auto flex items-center justify-center">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-extrabold text-white">Experience Successfully Logged!</h2>
          <p className="text-xs text-slate-300 max-w-lg mx-auto">
            Your placement interview review has been parsed and indexed by the ASTMA NLP Pipeline.
          </p>
        </div>

        {/* NLP Results Display */}
        {submittedExp.nlp_result && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-5">
            <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
              <BrainCircuit className="w-5 h-5 text-indigo-400" />
              <h3 className="text-sm font-bold text-white">
                ASTMA Natural Language Processing Pipeline Output
              </h3>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Sentiment Inferred</span>
                <div className="mt-1 flex items-baseline space-x-2">
                  <Badge
                    variant={
                      submittedExp.nlp_result.sentiment_label === "POSITIVE"
                        ? "success"
                        : submittedExp.nlp_result.sentiment_label === "NEGATIVE"
                        ? "danger"
                        : "neutral"
                    }
                  >
                    {submittedExp.nlp_result.sentiment_label}
                  </Badge>
                  <span className="text-xs font-mono text-slate-400">
                    {(submittedExp.nlp_result.sentiment_score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Difficulty Marker</span>
                <div className="mt-1">
                  <span className="text-xs font-bold text-amber-400 font-mono">
                    {submittedExp.nlp_result.inferred_difficulty}
                  </span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Confidence Score</span>
                <div className="mt-1">
                  <span className="text-xs font-mono font-bold text-blue-400">
                    {(submittedExp.nlp_result.sentiment_confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>

            <div>
              <p className="text-xs font-bold text-slate-300 mb-2">
                Recognized Technical &amp; Soft Skills
              </p>
              <div className="flex flex-wrap gap-2">
                {submittedExp.nlp_result.extracted_skills.map((sk) => (
                  <Badge key={sk} variant="primary" size="sm">
                    {sk}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs font-bold text-slate-300 mb-2">
                Core Interview Topics Extracted
              </p>
              <div className="flex flex-wrap gap-2">
                {submittedExp.nlp_result.extracted_topics.map((tp) => (
                  <Badge key={tp} variant="purple" size="sm">
                    {tp}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="flex justify-center space-x-4">
          <button
            onClick={() => {
              setSubmittedExp(null);
              setFeedback("");
              setQuestionsAsked("");
            }}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition"
          >
            Submit Another Experience
          </button>
          <button
            onClick={() => navigate("/experiences")}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-500 shadow-lg shadow-blue-600/25 transition"
          >
            Browse All Experiences
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Log Placement &amp; Interview Experience
          </h1>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
            ES Module 5 + ASTMA NLP
          </span>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Share your interview process to enrich institutional intelligence and guide peer preparation.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center space-x-2 text-xs text-rose-300">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Step 1: Company & Ratings */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-white pb-3 border-b border-slate-800">
            1. Recruiter &amp; Overall Evaluation
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Company
              </label>
              <select
                value={companyId}
                onChange={(e) => setCompanyId(e.target.value)}
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
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Placement Outcome
              </label>
              <select
                value={isPlaced ? "yes" : "no"}
                onChange={(e) => setIsPlaced(e.target.value === "yes")}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="yes">Received Offer / Placed</option>
                <option value="no">Interviewed (Not Selected)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Overall Experience Rating (1 - 5)
              </label>
              <div className="flex items-center space-x-3 mt-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setOverallRating(star)}
                    className="p-1 text-slate-600 hover:text-amber-400 transition"
                  >
                    <Star
                      className={`w-6 h-6 ${
                        star <= overallRating
                          ? "text-amber-400 fill-amber-400"
                          : "text-slate-700"
                      }`}
                    />
                  </button>
                ))}
                <span className="text-xs font-bold text-slate-300 ml-2">
                  {overallRating} / 5 Stars
                </span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Interview Difficulty Rating (1 - 5)
              </label>
              <div className="flex items-center space-x-3 mt-2">
                {[1, 2, 3, 4, 5].map((diff) => (
                  <button
                    key={diff}
                    type="button"
                    onClick={() => setDifficultyRating(diff)}
                    className={`px-3 py-1 rounded-lg text-xs font-bold border transition ${
                      difficultyRating === diff
                        ? "bg-blue-600 text-white border-blue-500"
                        : "bg-slate-950 text-slate-400 border-slate-800 hover:bg-slate-800"
                    }`}
                  >
                    {diff}
                  </button>
                ))}
                <span className="text-xs text-slate-400 ml-2">
                  {difficultyRating <= 2
                    ? "Easy"
                    : difficultyRating === 3
                    ? "Moderate"
                    : "Challenging"}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Step 2: Structured Interview Rounds */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h2 className="text-sm font-bold text-white">
              2. Interview Stages / Rounds ({rounds.length})
            </h2>
            <button
              type="button"
              onClick={addRound}
              className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Round</span>
            </button>
          </div>

          <div className="space-y-3">
            {rounds.map((r, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row items-center gap-3"
              >
                <span className="w-6 h-6 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center text-xs font-bold shrink-0">
                  {r.round_number}
                </span>

                <div className="flex-1 w-full grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <input
                    type="text"
                    value={r.round_title}
                    onChange={(e) => {
                      const next = [...rounds];
                      next[idx].round_title = e.target.value;
                      setRounds(next);
                    }}
                    placeholder="Round Title (e.g. Technical Coding)"
                    className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                  />

                  <select
                    value={r.round_type}
                    onChange={(e) => {
                      const next = [...rounds];
                      next[idx].round_type = e.target.value;
                      setRounds(next);
                    }}
                    className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
                  >
                    <option value="CODING">Coding Assessment</option>
                    <option value="TECHNICAL_INTERVIEW">Technical Interview</option>
                    <option value="SYSTEM_DESIGN">System Design</option>
                    <option value="HR_INTERVIEW">HR &amp; Behavioral</option>
                    <option value="APTITUDE">Aptitude Test</option>
                    <option value="GROUP_DISCUSSION">Group Discussion</option>
                    <option value="OTHER">Other Round</option>
                  </select>
                </div>

                {rounds.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeRound(idx)}
                    className="p-2 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition"
                    title="Remove round"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step 3: Free-Text Narrative for NLP Engine */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <MessageSquare className="w-5 h-5 text-indigo-400" />
            <h2 className="text-sm font-bold text-white">
              3. Qualitative Narrative Feedback (Input to ASTMA NLP)
            </h2>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Tagged Skills Tested (Optional hints)
            </label>
            <input
              type="text"
              value={skillsTested}
              onChange={(e) => setSkillsTested(e.target.value)}
              placeholder="e.g. Python, SQL, REST APIs, DBMS"
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Sample Questions Asked (Optional)
            </label>
            <input
              type="text"
              value={questionsAsked}
              onChange={(e) => setQuestionsAsked(e.target.value)}
              placeholder="e.g. How does indexing work in MySQL? Invert binary tree."
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-semibold text-slate-300">
                Detailed Feedback Narrative *
              </label>
              <span className="text-[10px] text-indigo-400 flex items-center space-x-1">
                <Sparkles className="w-3 h-3" />
                <span>Parsed by Sentiment &amp; Skill Extractor</span>
              </span>
            </div>
            <textarea
              required
              rows={5}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-blue-500 resize-none leading-relaxed"
              placeholder="Describe what occurred during your rounds. Mention topics asked, tools used, coding problems solved, and how the interviewers evaluated you..."
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full py-3 px-4 rounded-xl font-bold text-sm bg-blue-600 hover:bg-blue-500 text-white shadow-xl shadow-blue-600/25 flex items-center justify-center space-x-2 transition disabled:opacity-50"
        >
          <span>{submitting ? "Analyzing & Submitting..." : "Submit Placement Experience"}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
};
