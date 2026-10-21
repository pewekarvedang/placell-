# Information Technology Project Management (ITPM) Plan
## Project: Placell &mdash; AI-Powered Student Placement Experience and Career Analytics System
**Author:** Vedang Pewekar (Solo B.Tech CSBS Developer)  
**Academic Curriculum Mapping:** ITPM (Information Technology Project Management)  
**Project Execution Mode:** Agile/Scrum (Solo Engineering Cadence)  
**Total Timeline:** 14 Weeks (7 Sprints)  

---

### 1. Project Charter & Problem Statement

#### 1.1 Problem Statement
Higher education placement directorates and students face severe information asymmetry during recruitment seasons. Campus placement processes generate vast amounts of qualitative feedback (e.g., questions asked, difficulty, round structures, interviewer expectations), yet this valuable data remains scattered in unorganized WhatsApp chats, personal notes, or lost entirely upon graduation. Consequently:
1. **Students** prepare blindly without knowing real recruiter expectations or their specific skill gaps.
2. **Placement Cells (TPOs)** lack real-time quantitative dashboards showing company-wise sentiment, round difficulty, and conversion bottlenecks.
3. **Faculty Coordinators** cannot identify curriculum deficits to tailor pre-placement training.

#### 1.2 Project Objectives
- **Centralized Knowledge Ingestion:** Establish an enterprise platform for recording structured round details and unstructured narrative feedback.
- **Automated Text Mining (ASTMA):** Apply Natural Language Processing to extract sentiment polarity, technical/soft skill mentions, and interview topics.
- **Decision-Support Analytics:** Formulate explainable skill-gap evaluations and placement readiness estimates without demographic bias.
- **Role-Based Governance (ES):** Enforce strict RBAC (`Admin`, `TPO`, `Faculty`, `Student`) and audit trails.

---

### 2. Stakeholder Analysis

| Stakeholder Role | Concerns / Expectations | Impact on Project | Communication Channel |
| :--- | :--- | :---: | :--- |
| **Final-Year Students** | Accurate company interview patterns, actionable skill recommendations, privacy of personal data. | High | In-app Workspace, Notification banners |
| **Placement Officers (TPO)** | Moderation of student submissions, company conversion analytics, aggregated reports. | High | Placement Directorate Dashboard, Export reports |
| **Faculty / Coordinators** | Department-level skill performance, curriculum-to-industry alignment. | Medium | Faculty Analytics Portal |
| **System Administrator** | User account management, master dictionary maintenance, immutable audit logs. | Medium | Admin Console |
| **Academic Guide / Evaluator**| Rigorous demonstration of ES, ITPM, and ASTMA concepts, working software. | Critical | Bi-weekly Sprint Viva Reviews |

---

### 3. Feasibility Study

1. **Technical Feasibility:** The system utilizes a modular monolithic architecture (FastAPI backend + Vite React SPA) with open-source machine learning and NLP tooling (`numpy`, `pandas`, `scikit-learn`, `SQLAlchemy`). Feasibility is verified at 100%.
2. **Economic Feasibility:** The project operates with zero external licensing fees. Development and execution leverage existing local compute hardware and standard university free-tier tools (Budget: ₹0 / $0).
3. **Operational Feasibility:** The intuitive, responsive UI requires zero prior training for students or faculty coordinators.
4. **Schedule Feasibility:** 14 weeks is realistic for a dedicated solo engineer following structured 2-week Agile sprints.

---

### 4. Work Breakdown Structure (WBS)

```
1.0 Project Initiation & Architecture Formulation
    1.1 Problem Discovery & Scope Boundary Freezing
    1.2 Academic Subject Mapping Matrix (ES + ITPM + ASTMA)
    1.3 Software Architecture Design & Schema Modeling
2.0 Enterprise Systems (ES) Foundation
    2.1 PostgreSQL Database Initialization & Normalized Entity Schemas
    2.2 Multi-tier Role-Based Access Control (Admin, TPO, Faculty, Student)
    2.3 JWT Security, Password Hashing & Audit Log Subsystem
    2.4 Master Data Entities (Departments, Skills, Companies, Drives)
3.0 Student Ingestion & Verification Workflows (ES)
    3.1 Student Academic Portfolio & Skills Inventory CRUD
    3.2 Dual-Modal Placement Experience Submission Wizard
    3.3 TPO Experience Moderation Queue (Approve / Reject Workflow)
4.0 ASTMA Natural Language Processing & AI Models
    4.1 Lexicon & TF-IDF Weighted Sentiment Polarity Classifier
    4.2 Boundary Regex & Multi-Category Skill Entity Extractor
    4.3 Interview Topic & Difficulty Indicator Extraction Engine
    4.4 Non-Discriminatory Supervised Placement Readiness Model
    4.5 Explainable Skill-Gap Analyzer with Frequency Rationale
5.0 Enterprise Visualizations & Dashboards
    5.1 Student Personalized Workspace & Readiness Circular Gauge
    5.2 Placement Cell Command Center & Recruiter Performance Matrix
    5.3 Institutional Recharts Analytics Suite (Sentiment, Demand, Depts)
    5.4 Corporate Directory & Deep-Dive Company Intelligence Modal
6.0 Verification, Quality Assurance & Seeding
    6.1 Pytest Automated Integration & Endpoint Test Suite
    6.2 Realistic 200+ Student Cohort Synthetic Dataset Seeder
    6.3 Frontend Responsive Testing & Edge-Case Input Validation
7.0 Project Closure & Academic Defense
    7.1 ITPM Artifact Consolidation & Final Technical Thesis
    7.2 Viva Voce Demonstration Preparation & Slides
```

---

### 5. 14-Week Agile Sprint Schedule (Gantt Milestones)

| Sprint | Timeline | Objectives & Key Deliverables | Status |
| :---: | :---: | :--- | :---: |
| **Sprint 1** | Week 1 &ndash; 2 | Requirements analysis, normalized database design, project scaffolding, JWT authentication, and RBAC middleware. | COMPLETED |
| **Sprint 2** | Week 3 &ndash; 4 | Master entities: Departments, Skills Dictionary, Companies, Job Roles, and Placement Drives lifecycle management. | COMPLETED |
| **Sprint 3** | Week 5 &ndash; 6 | Student portfolio manager, interview experience logging wizard, and TPO moderation/verification queue. | COMPLETED |
| **Sprint 4** | Week 7 &ndash; 8 | ASTMA NLP pipeline: sentiment analysis, skill taxonomy matching, interview topic extraction, and inferred difficulty. | COMPLETED |
| **Sprint 5** | Week 9 &ndash; 10 | Placement readiness evaluation model, explainable skill-gap analyzer, and statistical recommendation generator. | COMPLETED |
| **Sprint 6** | Week 11 &ndash; 12 | Enterprise frontend dashboards (Student, TPO, Admin, Faculty) with interactive Recharts visualizations. | COMPLETED |
| **Sprint 7** | Week 13 &ndash; 14 | Pytest automated test suite, synthetic seeding (100 students, 25 companies, 114 experiences), and thesis documentation. | COMPLETED |

---

### 6. Risk Register & Mitigation Strategy

| Risk ID | Risk Description | Severity | Likelihood | Mitigation Strategy |
| :---: | :--- | :---: | :---: | :--- |
| **R-01** | **Unstructured Short Reviews (Cold Start):** Student reviews lack sufficient text for NLP entity extraction. | High | Med | Implemented a dual-modal submission pattern: mandatory structured tags for skills tested combined with free-text feedback. |
| **R-02** | **Privacy Infringement:** Student contact details exposed to unauthorized peers. | High | Low | Enforced strict query-level anonymization in experiences feeds; student profiles are accessible only by the owner or authorized TPO. |
| **R-03** | **Model Bias & Unethical Outputs:** Readability models penalizing students based on demographic factors. | Critical | Low | Excluded all protected attributes (gender, religion, caste, socioeconomics). Model is explicitly labeled as a Decision-Support estimate. |
| **R-04** | **Scope Creep for Solo Student:** Complex microservices architecture causing delivery delays. | High | Med | Adopted a robust modular monolith pattern with FastAPI and Vite React SPA, running without external paid cloud dependencies. |
| **R-05** | **Empty Initial System (Demo Failure):** Empty database during presentation. | Critical | Low | Built an automatic, deterministic database seeder that populates 100 students, 25 companies, and 114 verified experiences with NLP metrics on first startup. |

---

### 7. Cost Estimation (Solo Academic Project)

| Resource Element | Justification | Direct Cost |
| :--- | :--- | :---: |
| **Developer / Architect Labor** | 1 Solo Student Developer (~20 hrs/week &times; 14 weeks = 280 hrs) | Academic Project (₹0 / $0) |
| **Compute Hardware** | Existing development workstation (Windows 11, local compute) | Existing Asset (₹0 / $0) |
| **Runtime Software** | Python 3.14, Node.js 24, Vite 8, React 19 (MIT Open Source) | ₹0 / $0 |
| **Database System** | Local PostgreSQL 16 / SQLite Engine (Open Source) | ₹0 / $0 |
| **Total Project Expenditure** | **Fully reproducible, open-source academic architecture** | **₹0 / $0** |

---

### 8. Quality Assurance & Testing Plan

1. **Unit & API Testing:** Executed via `pytest` and `fastapi.testclient.TestClient`. Validates authentication token generation, unauthorized access blocking, experience submissions, NLP result extraction, and readiness evaluations.
2. **Deterministic Data Integrity:** Database foreign keys, unique constraints, and enum validations guarantee relational consistency.
3. **Frontend Verification:** Built with TypeScript strict type-checking and automated Vite bundle compiler (`tsc -b && vite build`) verifying 0 syntax or type warnings.
