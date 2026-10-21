export type UserRole = "ADMIN" | "TPO" | "FACULTY" | "STUDENT";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  department_id?: string;
  department_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: UserRole;
  user_id: string;
  email: string;
  full_name: string;
  department_id?: string;
  department_code?: string;
}

export interface StudentSkill {
  skill_id: string;
  skill_name: string;
  category: string;
  proficiency_level: string;
}

export interface StudentProfile {
  id: string;
  user_id: string;
  roll_number: string;
  full_name: string;
  email: string;
  department_id: string;
  department_code: string;
  department_name: string;
  cgpa: number;
  graduation_year: number;
  projects_count: number;
  internships_count: number;
  certifications_count: number;
  preferred_role_title: string;
  bio?: string;
  resume_url?: string;
  skills: StudentSkill[];
}

export interface Skill {
  id: string;
  name: string;
  category: string;
  description?: string;
}

export interface JobRole {
  id: string;
  company_id: string;
  title: string;
  min_cgpa: number;
  description?: string;
  required_skills: string[];
}

export interface Company {
  id: string;
  name: string;
  industry: string;
  company_type: string;
  website?: string;
  location?: string;
  ctc_min_lpa: number;
  ctc_max_lpa: number;
  description?: string;
  roles_count: number;
  experiences_count: number;
  average_difficulty: number;
  positive_sentiment_percent: number;
}

export interface PlacementDrive {
  id: string;
  company_id: string;
  company_name: string;
  job_role_id: string;
  job_role_title: string;
  title: string;
  drive_date: string;
  status: "UPCOMING" | "ACTIVE" | "COMPLETED" | "CANCELLED";
  eligibility_cgpa: number;
  eligibility_criteria?: string;
  ctc_offered_lpa: number;
  rounds_description?: string;
  applicants_count: number;
  selected_count: number;
}

export interface InterviewRound {
  id?: string;
  round_number: number;
  round_type: "APTITUDE" | "CODING" | "TECHNICAL_INTERVIEW" | "HR_INTERVIEW" | "GROUP_DISCUSSION" | "SYSTEM_DESIGN" | "OTHER";
  round_title?: string;
  description?: string;
  duration_minutes?: number;
  difficulty: number;
}

export interface NLPResult {
  sentiment_label: "POSITIVE" | "NEUTRAL" | "NEGATIVE";
  sentiment_score: number;
  sentiment_confidence: number;
  inferred_difficulty: "EASY" | "MODERATE" | "HARD";
  extracted_skills: string[];
  extracted_topics: string[];
  frequently_mentioned_terms: string[];
}

export interface PlacementExperience {
  id: string;
  student_id: string;
  student_roll_number: string;
  student_department: string;
  company_id: string;
  company_name: string;
  job_role_id?: string;
  job_role_title?: string;
  overall_rating: number;
  difficulty_rating: number;
  rounds_count: number;
  questions_asked?: string;
  skills_tested?: string;
  free_text_feedback: string;
  is_placed: boolean;
  status: "PENDING" | "VERIFIED" | "REJECTED";
  created_at: string;
  rounds: InterviewRound[];
  nlp_result?: NLPResult;
}

export interface ReadinessBreakdown {
  score: number;
  weight: string;
  description: string;
}

export interface ReadinessEvaluation {
  readiness_percentage: number;
  readiness_tier: "NEEDS_IMPROVEMENT" | "DEVELOPING" | "PLACEMENT_READY" | "STRONG";
  readiness_tier_display: string;
  feature_breakdown: Record<string, ReadinessBreakdown>;
  ethical_safeguard_notice: string;
}

export interface RecommendationItem {
  skill: string;
  priority: "HIGH" | "MEDIUM" | "LOW";
  frequency_in_drives: string;
  rationale: string;
  action_steps: string[];
}

export interface SkillGapAnalysis {
  target_role: string;
  matched_skills: string[];
  missing_skills: string[];
  match_percentage: number;
  recommendations: RecommendationItem[];
}

export interface DashboardKPIs {
  total_students: number;
  total_companies: number;
  total_drives: number;
  total_experiences: number;
  overall_placement_rate: number;
  average_experience_rating: number;
  average_interview_difficulty: number;
  verified_experiences_count: number;
}

export interface AnalyticsOverview {
  kpis: DashboardKPIs;
  sentiment_distribution: {
    positive: number;
    neutral: number;
    negative: number;
    positive_count: number;
    neutral_count: number;
    negative_count: number;
  };
  top_demanded_skills: Array<{
    skill_name: string;
    category: string;
    mention_count: number;
    percentage: number;
  }>;
  top_hiring_companies: Array<{
    company_id: string;
    company_name: string;
    industry: string;
    total_experiences: number;
    placed_count: number;
    avg_rating: number;
    avg_difficulty: number;
    ctc_max_lpa: number;
  }>;
  interview_difficulty_breakdown: Record<string, number>;
  department_metrics: Array<{
    department_code: string;
    department_name: string;
    total_students: number;
    placed_students: number;
    placement_rate: number;
    average_cgpa: number;
    average_readiness: number;
    top_skill_gaps: string[];
  }>;
  monthly_placement_trends: Array<{
    month: string;
    drives: number;
    experiences: number;
    placed: number;
  }>;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  user_email?: string;
  user_role?: string;
  action: string;
  entity_name: string;
  entity_id?: string;
  details?: string;
  ip_address?: string;
  timestamp: string;
}
