# Placell: AI-Powered Student Placement Experience and Career Analytics System

> **A software-only enterprise web platform engineered for higher-education placement cells (TPOs), academic departments, and students.**  
> Built by **Vedang Pewekar** as a final-year B.Tech Computer Science & Business Systems (CSBS) capstone project mapping explicitly to **Enterprise Systems (ES)**, **Information Technology Project Management (ITPM)**, and **Advanced Technologies & Modern Applications (ASTMA)** with zero mandatory hardware or IoT sensors.

---

## 1. Academic Subject Mapping

| Subject Area | Academic Focus | Concrete System Implementation in Placell |
| :--- | :--- | :--- |
| **ES** (Enterprise Systems) | Workflows, RBAC, Data Integrity, Auditing, Multi-tenant/Dept Scoping | Normalized relational schema, 4-tier Role-Based Access Control (`Admin`, `Placement Officer / TPO`, `Faculty Coordinator`, `Student`), immutable audit logging, experience verification workflow, department-level scoping, and institutional reports. |
| **ITPM** (IT Project Management) | Lifecycle planning, Solo delivery, Risk, Quality, Agile Sprints, Cost/WBS | 14-week single-engineer Agile/Scrum roadmap, Work Breakdown Structure (WBS), Risk Register with severity scoring, zero-budget cost estimation, and comprehensive verification matrix (`docs/itpm/ITPM_PROJECT_MANAGEMENT_PLAN.md`). |
| **ASTMA** (Advanced Technologies) | Applied NLP, Supervised ML, Information Extraction, Explainable AI | Calibrated sentiment analysis (positive/neutral/negative confidence), boundary regex & dictionary skill extraction (150+ taxonomy), interview topic & difficulty inference, supervised placement readiness estimator, and explainable skill-gap recommendation engine. |

---

## 2. High-Level Architecture

```
React 19 Frontend (Vite + TypeScript + Tailwind CSS + Recharts + Lucide)
                                 │
                     HTTPS / REST API Requests
                                 ▼
                     FastAPI Application Gateway
         (OAuth2 Bearer / JWT Auth Guard / RBAC Role Guard / Audit Logger)
                                 │
             ┌───────────────────┴───────────────────┐
             ▼                                       ▼
       Service Layer                           ASTMA AI/ML Services
 (Auth, Student, Drive, Exp)            (Sentiment, Skill Extractor, Readiness)
             │                                       │
             └───────────────────┬───────────────────┘
                                 ▼
                 SQLAlchemy 2.0 Relational Models
                                 ▼
            PostgreSQL / Local SQLite (placell.db)
```

---

## 3. Demo Persona Credentials (For Viva Voce Presentation)

All default accounts are pre-seeded and share the password: **`Pass@123`**

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Student** | `student@college.edu` | `Pass@123` | View personal readiness gauge, update academic profile, analyze skill-gap, log interview experiences, apply to drives. |
| **Placement Officer (TPO)** | `tpo@college.edu` | `Pass@123` | Placement cell command center, moderation queue to approve/reject student submissions, company intelligence, macro analytics. |
| **Faculty Coordinator** | `faculty.cse@college.edu` | `Pass@123` | Department-level analytics, curriculum gap insights, placement trends. |
| **System Admin** | `admin@college.edu` | `Pass@123` | User and role governance, master skills dictionary, system-wide immutable audit trail. |

*(The login screen includes quick one-click buttons to instantly switch between these 4 roles).*

---

## 4. Key Functional Modules

1. **Authentication & RBAC (ES):** Secure JWT authentication with role-based route protection across 4 institutional personas.
2. **Student Academic Portfolio (ES):** CGPA, projects count, internships, certifications, and skills inventory.
3. **Corporate Partner & Drive Management (ES):** Company directory with compensation brackets (LPA), drive scheduling, and student application routing.
4. **Placement Experience Submission Wizard (ES + ASTMA):** Dual-modal logger supporting structured interview rounds (Coding, Technical, HR) and free-text narrative feedback.
5. **ASTMA NLP Extraction Pipeline:**
   - **Sentiment Analysis:** Calibrated text polarity classification yielding `POSITIVE`, `NEUTRAL`, or `NEGATIVE` with confidence scoring.
   - **Skill Extraction:** Multi-category taxonomy (150+ skills) with boundary regex pattern matching.
   - **Topic & Difficulty Inference:** Automated classification of interview topics and question difficulty.
6. **ASTMA Placement Readiness Model:** Interpretable tabular estimation model using objective academic and technical attributes. Strictly excludes all demographic or sensitive factors. Labeled as an educational decision-support estimate.
7. **Explainable Skill-Gap Analyzer:** Compares student skills against target company requirements and generates quantified justifications:
   > *"Power BI is recommended because it appeared in 74% of analyzed Data Analyst interview rounds while it is currently missing from your profile."*
8. **Enterprise Dashboards & Visualizations:** Interactive Recharts charts for sentiment distribution, skill demand, department comparisons, and monthly hiring trends.
9. **Enterprise Moderation & Audit Logging (ES):** TPO moderation queue to review student submissions, coupled with an immutable audit log trail.

---

## 5. Deployment & Quickstart Guide

### Option A: One-Click Production Start (Windows)
Double-click `start_app.bat` or run in terminal:
```powershell
.\start_app.bat
```
* Builds the React frontend (if needed) and serves the **entire unified application (Frontend + Backend)** on `http://localhost:8000`.
* Automatically opens your default web browser to the login page.

---

### Option B: Docker Container Deployment (Multi-Platform)
Deploy with Docker Compose:
```bash
docker compose up --build -d
```
* Compiles frontend assets in Node.js, packages backend dependencies in Python 3.12, and runs the unified production container on `http://localhost:8000`.

---

### Option C: Concurrent Development Environment
Run backend and frontend with live Hot Module Replacement (HMR):
```powershell
.\start_dev.bat
```
* **Frontend:** `http://localhost:5173`
* **Backend API:** `http://localhost:8000`
* **Swagger API Documentation:** `http://localhost:8000/docs`

---

### Running Automated Test Suite
From the project root:
```powershell
$env:PYTHONPATH="backend"
py -m pytest tests/backend/test_api.py -v
```
*(All 8 integration test suites covering JWT authentication, student readiness, skill extraction, moderation queue, company/drive creation, applicant tracking, and administrative audit logs will execute with 100% pass rate).*

---

## 6. Project Directory Layout

```
├── backend/
│   ├── app/
│   │   ├── ai/                # ASTMA: Sentiment, Skill Extractor, Topic, Readiness, Recommendations
│   │   ├── core/              # Config, Security (JWT/bcrypt), Database session, RBAC guards
│   │   ├── models/            # SQLAlchemy 2.0 Entities (User, Student, Company, Drive, Experience, Audit)
│   │   ├── routes/            # REST API endpoints (/auth, /students, /companies, /drives, /experiences, /analytics, /admin)
│   │   ├── schemas/           # Pydantic V2 DTO validation schemas
│   │   ├── services/          # Business logic and database access layer
│   │   ├── utils/             # Database seeder (200+ cohort synthetic dataset)
│   │   └── main.py            # FastAPI application entry point
│   └── placell.db             # SQLite database (with full PostgreSQL support via DATABASE_URL)
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Navbar, Sidebar, StatCard, Badge, Common controls
│   │   ├── context/           # AuthContext (JWT session management)
│   │   ├── pages/             # Student, TPO, Faculty, Admin, and Shared analytics pages
│   │   ├── services/          # Axios typed API client
│   │   ├── types/             # Strict TypeScript DTO definitions
│   │   ├── App.tsx            # Protected role router
│   │   └── main.tsx           # React entry point
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│   ├── itpm/                  # ITPM Project Management Plan, WBS, Gantt, Risk Register
│   ├── architecture/          # Academic architecture specifications
│   └── reports/               # SRS and academic report documentation
│
└── tests/
    └── backend/               # Automated Pytest suite
```

---

## 7. Academic Integrity & Ethics Statement

Placell is designed as an educational decision-support analytics system. It does not predict or guarantee employment. All machine learning algorithms strictly exclude demographic, gender, racial, religious, or socioeconomic attributes, adhering to fairness and transparency standards in academic computing.
