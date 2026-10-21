# Placell &mdash; Final-Year B.Tech Viva Voce Presentation Deck
## Slide Deck Transcript, Visual Architecture & Oral Defense Script

**PowerPoint File:** [`docs/presentation/Placell_Final_Year_Viva_Presentation.pptx`](file:///d:/projects/docs/presentation/Placell_Final_Year_Viva_Presentation.pptx)  
**Project Title:** Placell: AI-Powered Student Placement Experience and Career Analytics System  
**Candidate:** Vedang Pewekar (Solo B.Tech CSBS Developer)  
**Curriculum Mapping:** Enterprise Systems (ES) • IT Project Management (ITPM) • Advanced Technologies (ASTMA)  
**Execution Type:** 100% Software-Only Platform (Zero Hardware / IoT Devices)  

---

### Slide 1: Title & Academic Identification
- **Title:** Placell: AI-Powered Student Placement Experience and Career Analytics System
- **Subtitle:** Final-Year B.Tech Computer Science & Business Systems (CSBS) Capstone Project
- **Presenter:** Vedang Pewekar
- **Subject Coverage:** Explicit demonstration of **Enterprise Systems (ES)**, **IT Project Management (ITPM)**, and **Advanced Technologies & Modern Applications (ASTMA)**.
- **Constraints Compliance:** 100% Software-Only Platform • Zero Mandatory IoT / Hardware Sensors.
- **Speaker Script:**
  > *"Respected examiners and guides, good morning. I am Vedang Pewekar, presenting Placell, an enterprise platform that captures qualitative placement feedback, extracts NLP intelligence, and generates explainable career analytics. This project represents solo delivery mapping directly to ES, ITPM, and ASTMA without requiring any hardware components."*

---

### Slide 2: Vision & Institutional Problem Statement
- **Current State:**
  - Student placement reviews and interview experiences remain scattered in informal WhatsApp chats, seniors' memory, or disappear upon graduation.
  - Junior students prepare blindly without knowing actual interview stages or round difficulties.
  - Placement cells lack centralized quantitative intelligence to evaluate round-by-round rejection bottlenecks.
  - Academic departments cannot systematically identify curriculum deficits demanded across corporate drives.
- **The Placell Solution:**
  - Centralized knowledge ingestion of structured rounds and free-form narrative feedback.
  - Automated Natural Language Processing (sentiment analysis, skill entity matching, interview topics).
  - Explainable skill-gap recommendations backed by statistical drive occurrence.
  - Multi-tier role governance across Students, Placement Officers, Faculty, and Admins.
- **Speaker Script:**
  > *"Every year, hundreds of students interview at top tech firms, yet this feedback is lost when seniors graduate. Placell turns this unstructured qualitative feedback into institutional intelligence, closing the gap between university preparation and recruiter expectations."*

---

### Slide 3: Explicit Academic Curriculum Mapping
- **ES (Enterprise Systems):**
  - Centralized normalized PostgreSQL database with 10+ entities.
  - 4-Tier Role-Based Access Control (`Admin`, `Placement Officer`, `Faculty Coordinator`, `Student`).
  - Moderation workflow: TPO review queue authorizing student feedback before publication.
  - Immutable audit logs tracking user logins, reviews, and status changes.
  - Departmental data scoping for faculty coordinators.
- **ITPM (Information Technology Project Management):**
  - 14-week Agile/Scrum delivery lifecycle with 7 two-week sprints.
  - Work Breakdown Structure (WBS) from initiation to viva closure.
  - Formal 5-factor risk register with mitigation strategies.
  - Zero-budget economic cost estimation leveraging open-source tooling.
  - Automated testing plan and verification matrix.
- **ASTMA (Advanced Technologies & Modern Applications):**
  - Calibrated sentiment polarity classifier (Positive / Neutral / Negative).
  - 150+ technology taxonomy entity extractor with word boundary regex.
  - Interview topic clustering and difficulty indicators.
  - Supervised tabular placement readiness estimation model.
  - Explainable recommendation engine with quantifiable statistical justification.
- **Speaker Script:**
  > *"This slide is the core academic anchor of my project. For Enterprise Systems, I demonstrate multi-tier RBAC, workflows, and audit logging. For ITPM, I show a disciplined 14-week solo Agile roadmap with risk management. For ASTMA, I demonstrate applied NLP and explainable machine learning."*

---

### Slide 4: Layered System Architecture
- **Layer 1: Presentation (React 19 + TypeScript + Vite + Tailwind CSS):**
  - Single Page Application with dynamic role layouts and interactive Recharts visualizations.
- **Layer 2: API Gateway & Security (FastAPI):**
  - OAuth2 bearer JWT token authentication, CORS middleware, and role dependency guards (`RequireRoles`).
- **Layer 3: Business & ASTMA Services:**
  - Modular service layer (`StudentService`, `CompanyService`, `DriveService`, `ExperienceService`) coupled with ASTMA AI models (`SentimentAnalyzer`, `SkillExtractor`, `ReadinessModel`).
- **Layer 4: Persistence Layer (SQLAlchemy 2.0 + PostgreSQL / SQLite):**
  - Normalized relational database with cascade deletes and foreign keys.
- **Speaker Script:**
  > *"We deliberately engineered a layered modular monolith rather than microservices. For a single engineer, microservices add unnecessary network latency and deployment complexity. Our layered monolith enforces clean separation of concerns while running locally with zero latency."*

---

### Slide 5: Enterprise Systems (ES) Implementation
- **Role-Based Access Control Matrix:**
  - `Student`: Profile portfolio, readiness gauge, skill gap analyzer, interview logging, drive applications.
  - `Placement Officer (TPO)`: Drive creation, moderation queue, company catalog, macro analytics.
  - `Faculty Coordinator`: Department-scoped metrics, curriculum skill gaps, placement trends.
  - `System Admin`: Account governance, central skills dictionary, immutable audit trail.
- **Enterprise Workflow:**
  - Student submits dual-modal experience &rarr; Placed in TPO moderation queue &rarr; TPO approves or rejects with recorded notes &rarr; Indexed into college analytics &rarr; Audit log recorded.
- **Speaker Script:**
  > *"Enterprise systems require clear boundaries of authority. In Placell, permissions are enforced at the API gateway via dependency injection. Notice our moderation queue: students contribute data, but placement officers authorize it before it updates the global analytics."*

---

### Slide 6: Normalized Relational Database Schema
- **Entity Overview:**
  - `users` & `departments` (Authentication, roles, department scoping).
  - `students` & `student_skills` (Academic credentials, proficiency levels).
  - `companies` & `job_roles` (Recruiter catalog, CTC packages, benchmark skills).
  - `placement_drives` & `applications` (Drive scheduling, student applicant tracking).
  - `placement_experiences`, `interview_rounds`, & `nlp_analysis_results` (Interviews, timeline, extracted NLP vectors).
  - `audit_logs` (Security and compliance audit trail).
- **Speaker Script:**
  > *"Our database is normalized to Third Normal Form. Each experience record links to both structured interview rounds and automated NLP extraction results, ensuring relational consistency and query performance."*

---

### Slide 7: ASTMA Qualitative Natural Language Processing
- **Pipeline Stages:**
  1. **Preprocessing:** Normalization, contraction expansion, stopword removal, preserving technical symbols (`C++`, `.NET`).
  2. **Calibrated Sentiment Analysis:** Dual-factor polarity combining placement lexicon weights, negations (`not fair`), and explicit user ratings. Output: `POSITIVE`, `NEUTRAL`, or `NEGATIVE` with confidence score.
  3. **Boundary Regex Skill Extraction:** Scans text against 150+ technology taxonomy across 7 domains. Boundary tokens (`\b`) eliminate false positives.
  4. **Topic & Difficulty Inference:** Identifies DSA, System Design, SQL, and HR topics, calculating question difficulty indicators.
- **Speaker Script:**
  > *"For ASTMA, our NLP pipeline extracts structured intelligence from unstructured paragraphs. When a student writes 'The technical interview grilled me on SQL joins and Python OOP', our pipeline extracts 'SQL' and 'Python', infers positive sentiment, and tags Database and OOP as core topics."*

---

### Slide 8: ASTMA Explainable Placement Readiness Model
- **Supervised Tabular Feature Vector:**
  - Academic CGPA (25% Weight)
  - Technical Skills Depth (25% Weight)
  - Target Role Overlap Ratio (25% Weight)
  - Portfolio Projects (15% Weight)
  - Industry Internships & Certifications (10% Weight)
- **Categorization Tiers:**
  - `Strong Candidate` (&ge; 85%)
  - `Placement Ready` (70% &ndash; 84%)
  - `Developing` (50% &ndash; 69%)
  - `Needs Improvement` (< 50%)
- **Ethical Safeguard:**
  - Zero demographic, gender, religious, or socioeconomic traits used. Explicitly badged as an educational decision-support estimate.
- **Speaker Script:**
  > *"Our readiness model avoids black-box opacity. It uses an objective 5-part feature vector, providing students with exact percentage contributions for their CGPA, skills, and projects. Most importantly, it completely excludes sensitive demographic attributes."*

---

### Slide 9: Explainable Skill-Gap Analyzer & Recommendations
- **Formula:** $\text{Skill Gap} = S_{\text{Required}}(\text{Role}) \setminus S_{\text{Acquired}}(\text{Student})$
- **Methodology:**
  1. Computes set difference between student profile and company requirements.
  2. Calculates historical market occurrence of missing skills across verified drives.
  3. Formulates auditable rationale:
     > *"Power BI is recommended because it appeared in 74% of analyzed Data Analyst interview rounds, but is currently absent from your profile."*
  4. Outlines actionable learning milestones (concept review, GitHub project, problem sets).
- **Speaker Script:**
  > *"Traditional recommenders simply give opaque suggestions. In Placell, every single recommendation cites the exact historical percentage of campus drives that tested that skill, giving students clear reasons to study missing topics."*

---

### Slide 10: ITPM 14-Week Solo Agile Delivery Schedule
- **Sprint 1 (Weeks 1-2):** Scope, normalized schema, JWT auth, RBAC guards.
- **Sprint 2 (Weeks 3-4):** Master entities (Departments, Skills, Companies, Drives).
- **Sprint 3 (Weeks 5-6):** Student portfolio manager, interview submission wizard, TPO moderation queue.
- **Sprint 4 (Weeks 7-8):** ASTMA NLP pipeline (Sentiment, skill extraction, topics).
- **Sprint 5 (Weeks 9-10):** Readiness model, skill-gap analyzer, explainable recommendation engine.
- **Sprint 6 (Weeks 11-12):** React 19 dashboards with Recharts visualizations.
- **Sprint 7 (Weeks 13-14):** Automated testing, synthetic cohort seeding (100 students, 114 reviews), viva closure.
- **Speaker Script:**
  > *"For IT Project Management, I structured development into seven 2-week Agile sprints. This disciplined pacing enabled me to deliver an enterprise-grade platform on time as a solo engineer."*

---

### Slide 11: ITPM Risk Register & Mitigation Strategy
- **R-01 (Short Reviews / Cold Start):** Mitigated by dual-modal submission combining tagged skills with free text.
- **R-02 (Privacy Infringement):** Mitigated by query-level anonymization in aggregated public views.
- **R-03 (Model Bias):** Mitigated by eliminating demographic attributes and labeling outputs as decision support.
- **R-04 (Scope Creep):** Mitigated by using a modular monolith pattern instead of microservices.
- **R-05 (Empty Database on Presentation Day):** Mitigated by automated synthetic seeding on first boot.
- **Speaker Script:**
  > *"Our risk management plan identified 5 core technical risks. By implementing mitigations early—such as query-level anonymization and automated database seeding—we ensured system reliability and zero failure during demonstration."*

---

### Slide 12: ITPM Resource Allocation & Zero-Budget Costing
- **Labor Effort:** 1 Solo Student Developer (280 engineering hours across 14 weeks).
- **Compute:** Local workstation compute (Windows 11). Zero paid cloud servers required.
- **Software:** Open-source stack (Python, FastAPI, React 19, SQLite, Tailwind).
- **Total Financial Expenditure:** ₹0 / $0 &mdash; 100% reproducible on any university machine.
- **Speaker Script:**
  > *"Under ITPM cost estimation, the platform was engineered for zero budget. By selecting open-source technologies, the entire system runs locally on standard university hardware without subscription expenses."*

---

### Slide 13: UI/UX Design & User Experience
- **Student Workspace:** Readiness circular gauge, feature contribution progress bars, skill-gap comparison, review submission wizard.
- **Placement Cell Directorate:** Placement conversion metrics, active drives tracker, experience moderation queue.
- **Analytics & Governance:** Recharts sentiment pie charts, skill demand horizontal bar charts, department comparison, and immutable audit logs.
- **Demo Switcher:** One-click role buttons on the login screen to demonstrate all 4 user perspectives immediately.
- **Speaker Script:**
  > *"The interface uses modern design standards with Tailwind CSS and Recharts. During the live demo, examiners can use the one-click role switcher to experience the system from student, placement officer, faculty, and administrator perspectives."*

---

### Slide 14: Quality Assurance & Automated Verification
- **Pytest Integration Suite (100% Pass):**
  - `test_health_check` &mdash; Validates ES, NLP, and readiness subsystems.
  - `test_student_login_and_profile` &mdash; Asserts JWT auth and readiness calculation.
  - `test_analytics_overview` &mdash; Asserts college KPIs and sentiment distributions.
  - `test_experience_submission_and_nlp` &mdash; Asserts automated sentiment and skill entity extraction.
- **Synthetic Data Scale:**
  - 100 students across 4 departments (CSE, CSBS, AIML, IT).
  - 25 companies with 45+ job roles.
  - 18 placement drives.
  - 116 verified experiences with NLP metadata.
- **Speaker Script:**
  > *"Quality assurance is automated via Pytest. Furthermore, our database seed script populates 100 students and 116 verified interview experiences, ensuring that all dashboards display real data immediately."*

---

### Slide 15: Limitations & Future Scope
- **Current Boundaries:** English text corpus, self-reported proficiency, dictionary-based skill extensions.
- **Future Enhancements:** Automated resume PDF parsing via OCR, interactive AI mock interview simulator, multi-college university federation.
- **Speaker Script:**
  > *"Acknowledging boundaries demonstrates engineering maturity. While Placell currently focuses on English reviews and an extensible skill dictionary, our modular architecture makes it easy to integrate PDF resume parsing and AI mock interview simulations in the future."*

---

### Slide 16: Conclusion & Viva Voce Defense Summary
- **Core Engineering Achievements:**
  - Complete curriculum mapping across **Enterprise Systems**, **IT Project Management**, and **Advanced Technologies**.
  - 100% software-only delivery with zero IoT hardware requirements.
  - Transforms qualitative interview reviews into actionable institutional intelligence.
  - High-performance production code with automated tests and instant viva demonstration capabilities.
- **Speaker Script:**
  > *"To conclude, Placell proves that an enterprise AI platform can be planned, engineered, and validated by a single student following structured ITPM disciplines. The system is live and ready for demonstration. Thank you, and I look forward to your questions."*

---

## Probable Viva Voce Questions & Recommended Answers

| Probable Examiner Question | Recommended Defense Response |
| :--- | :--- |
| **Q1: Why did you not use a Large Language Model (like GPT-4) for sentiment analysis?** | *"For an academic enterprise platform, reproducibility, deterministic execution, and zero cost are paramount. Third-party LLM APIs introduce non-deterministic outputs, API latency, vendor lock-in, and ongoing billing. Our calibrated TF-IDF and lexicon-based NLP runs locally in milliseconds with 100% explainability and zero external cost."* |
| **Q2: Does your readiness score guarantee student placement?** | *"No, and we explicitly disclaim employment guarantees on the student dashboard. The score is strictly an educational decision-support indicator designed to identify missing technical preparation and guide corrective learning."* |
| **Q3: How does your system prevent students from submitting fake reviews?** | *"Through our Enterprise Systems moderation workflow. When a student submits a review, its initial status is queued. Placement officers review the content in a dedicated verification queue before it is published to the knowledge base or factored into college analytics."* |
| **Q4: Why did you choose a monolithic architecture instead of microservices?** | *"Under ITPM resource planning for a solo engineer, microservices introduce unnecessary operational overhead (RPC latency, service discovery, container orchestration). A modular monolith with clean service boundaries provides the exact same separation of concerns while maximizing development velocity and local portability."* |
