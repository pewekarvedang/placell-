import axios from "axios";
import {
  AuthResponse,
  StudentProfile,
  Company,
  PlacementDrive,
  PlacementExperience,
  AnalyticsOverview,
  SkillGapAnalysis,
  ReadinessEvaluation,
  Skill,
  User,
  AuditLog
} from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to attach JWT bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle 401 session expirations gracefully
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      if (window.location.pathname !== "/login" && window.location.pathname !== "/register") {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Auth Endpoints
export const authApi = {
  login: async (credentials: { email: string; password: string }): Promise<AuthResponse> => {
    const res = await api.post<AuthResponse>("/auth/login", credentials);
    return res.data;
  },
  register: async (payload: any): Promise<User> => {
    const res = await api.post<User>("/auth/register", payload);
    return res.data;
  },
  getMe: async (): Promise<User> => {
    const res = await api.get<User>("/auth/me");
    return res.data;
  },
};

// Student Endpoints
export const studentApi = {
  getProfile: async (): Promise<StudentProfile> => {
    const res = await api.get<StudentProfile>("/students/me");
    return res.data;
  },
  updateProfile: async (data: Partial<StudentProfile>): Promise<StudentProfile> => {
    const res = await api.put<StudentProfile>("/students/me", data);
    return res.data;
  },
  addSkill: async (skill_id: string, proficiency_level = "Intermediate"): Promise<StudentProfile> => {
    const res = await api.post<StudentProfile>("/students/me/skills", { skill_id, proficiency_level });
    return res.data;
  },
  removeSkill: async (skill_id: string): Promise<StudentProfile> => {
    const res = await api.delete<StudentProfile>(`/students/me/skills/${skill_id}`);
    return res.data;
  },
  getReadiness: async (): Promise<ReadinessEvaluation> => {
    const res = await api.get<ReadinessEvaluation>("/students/me/readiness");
    return res.data;
  },
  getSkillGap: async (target_role_id?: string): Promise<SkillGapAnalysis> => {
    const res = await api.get<SkillGapAnalysis>("/students/me/skill-gap", {
      params: { target_role_id }
    });
    return res.data;
  },
};

// Company Endpoints
export const companyApi = {
  getCompanies: async (search?: string, industry?: string): Promise<Company[]> => {
    const res = await api.get<Company[]>("/companies", { params: { search, industry } });
    return res.data;
  },
  getAnalytics: async (companyId: string) => {
    const res = await api.get(`/companies/${companyId}/analytics`);
    return res.data;
  },
  createCompany: async (payload: any): Promise<Company> => {
    const res = await api.post<Company>("/companies", payload);
    return res.data;
  },
  getRoles: async (companyId: string): Promise<any[]> => {
    const res = await api.get<any[]>(`/companies/${companyId}/roles`);
    return res.data;
  },
};

// Placement Drive Endpoints
export const driveApi = {
  getDrives: async (status?: string): Promise<PlacementDrive[]> => {
    const res = await api.get<PlacementDrive[]>("/drives", { params: { status } });
    return res.data;
  },
  apply: async (driveId: string) => {
    const res = await api.post(`/drives/${driveId}/apply`);
    return res.data;
  },
  createDrive: async (payload: any): Promise<PlacementDrive> => {
    const res = await api.post<PlacementDrive>("/drives", payload);
    return res.data;
  },
  getApplications: async (driveId: string): Promise<any[]> => {
    const res = await api.get<any[]>(`/drives/${driveId}/applications`);
    return res.data;
  },
  updateApplicationStatus: async (applicationId: string, status: string): Promise<any> => {
    const res = await api.patch<any>(`/drives/applications/${applicationId}/status`, { status });
    return res.data;
  },
};

// Placement Experience Endpoints
export const experienceApi = {
  getVerified: async (search?: string, companyId?: string): Promise<PlacementExperience[]> => {
    const res = await api.get<PlacementExperience[]>("/experiences", { params: { search, company_id: companyId } });
    return res.data;
  },
  getMy: async (): Promise<PlacementExperience[]> => {
    const res = await api.get<PlacementExperience[]>("/experiences/my");
    return res.data;
  },
  getPending: async (): Promise<PlacementExperience[]> => {
    const res = await api.get<PlacementExperience[]>("/experiences/pending");
    return res.data;
  },
  submit: async (payload: any): Promise<PlacementExperience> => {
    const res = await api.post<PlacementExperience>("/experiences", payload);
    return res.data;
  },
  verify: async (experienceId: string, status: "VERIFIED" | "REJECTED", notes?: string): Promise<PlacementExperience> => {
    const res = await api.patch<PlacementExperience>(`/experiences/${experienceId}/verify`, {
      status,
      moderation_notes: notes
    });
    return res.data;
  },
};

// Analytics Endpoints
export const analyticsApi = {
  getOverview: async (): Promise<AnalyticsOverview> => {
    const res = await api.get<AnalyticsOverview>("/analytics/overview");
    return res.data;
  },
};

// Admin Endpoints
export const adminApi = {
  getUsers: async (): Promise<User[]> => {
    const res = await api.get<User[]>("/admin/users");
    return res.data;
  },
  getSkills: async (): Promise<Skill[]> => {
    const res = await api.get<Skill[]>("/admin/skills");
    return res.data;
  },
  addSkill: async (payload: { name: string; category: string; description?: string }): Promise<Skill> => {
    const res = await api.post<Skill>("/admin/skills", payload);
    return res.data;
  },
  getAuditLogs: async (limit = 100): Promise<AuditLog[]> => {
    const res = await api.get<AuditLog[]>("/admin/audit-logs", { params: { limit } });
    return res.data;
  },
  getDepartments: async (): Promise<any[]> => {
    const res = await api.get<any[]>("/admin/departments");
    return res.data;
  },
  addDepartment: async (payload: { code: string; name: string; description?: string }): Promise<any> => {
    const res = await api.post<any>("/admin/departments", payload);
    return res.data;
  },
};
