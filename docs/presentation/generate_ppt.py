import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6] # Blank layout

    # Color Palette (Enterprise Modern Dark)
    BG_COLOR = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    BORDER_COLOR = RGBColor(51, 65, 85)   # Slate 700
    WHITE = RGBColor(248, 250, 252)       # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    PRIMARY_BLUE = RGBColor(56, 189, 248) # Sky 400
    ACCENT_INDIGO = RGBColor(129, 140, 248) # Indigo 400
    SUCCESS_EMERALD = RGBColor(52, 211, 153) # Emerald 400
    WARNING_AMBER = RGBColor(251, 191, 36) # Amber 400

    def apply_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_pill="ACADEMIC DEFENSE"):
        # Header container
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category pill line
        p_pill = tf.paragraphs[0]
        p_pill.text = category_pill.upper()
        p_pill.font.size = Pt(11)
        p_pill.font.bold = True
        p_pill.font.color.rgb = PRIMARY_BLUE

        # Main title
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.space_before = Pt(4)

    def add_card(slide, left, top, width, height, bg_rgb=CARD_BG, border_rgb=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_rgb
        card.line.color.rgb = border_rgb
        card.line.width = Pt(1)
        return card

    def add_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    # Accent decorative banner
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.4))
    banner.fill.solid()
    banner.fill.fore_color.rgb = PRIMARY_BLUE
    banner.line.fill.background()

    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.4))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "FINAL-YEAR B.TECH CAPSTONE PROJECT DEFENSE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    p2 = tf1.add_paragraph()
    p2.text = "Placell"
    p2.font.size = Pt(44)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "AI-Powered Student Placement Experience and Career Analytics System"
    p3.font.size = Pt(20)
    p3.font.color.rgb = ACCENT_INDIGO
    p3.space_before = Pt(4)

    p4 = tf1.add_paragraph()
    p4.text = "Academic Integration: Enterprise Systems (ES) • IT Project Management (ITPM) • Advanced Technologies (ASTMA)"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(14)

    # Footer box with student metadata
    foot_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.6), Inches(11.0), Inches(1.2))
    tff = foot_box.text_frame
    pf1 = tff.paragraphs[0]
    pf1.text = "Candidate: Vedang Pewekar (Solo B.Tech CSBS Developer)  |  Branch: Computer Science & Business Systems (CSBS)"
    pf1.font.size = Pt(12)
    pf1.font.bold = True
    pf1.font.color.rgb = WHITE

    pf2 = tff.add_paragraph()
    pf2.text = "Constraint Compliance: 100% Software-Only Platform  •  Zero IoT / Physical Hardware Components"
    pf2.font.size = Pt(11)
    pf2.font.color.rgb = SUCCESS_EMERALD
    pf2.space_before = Pt(4)

    add_speaker_notes(s1, "Good morning respected examiners and guides. I am Vedang Pewekar, presenting Placell, an enterprise AI-powered platform for institutional placement intelligence and explainable career analytics. This project represents solo development across Enterprise Systems, ITPM, and ASTMA with strict software-only constraints.")

    # =========================================================================
    # SLIDE 2: Vision & Institutional Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, "Project Vision & Institutional Problem Statement", "THE PROBLEM CONTEXT")

    # Left card: The Core Dilemma
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c1_box = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tf2_1 = c1_box.text_frame
    tf2_1.word_wrap = True

    p = tf2_1.paragraphs[0]
    p.text = "Current State & Fragmented Data"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WARNING_AMBER

    bullets_c1 = [
        ("Disorganized Experience Logging: ", "Student placement and interview experiences remain scattered in informal WhatsApp chats, seniors' memory, or lost upon graduation."),
        ("Information Asymmetry: ", "Junior students prepare blindly without knowing real recruiter expectations, interview stages, or round difficulties."),
        ("Sub-optimal Placement Strategies: ", "Placement cells lack centralized quantitative intelligence to evaluate which rounds cause candidate rejections."),
        ("Curriculum-Industry Gap: ", "Academic departments cannot systematically identify missing competencies demanded across corporate campus drives.")
    ]
    for title, desc in bullets_c1:
        p_b = tf2_1.add_paragraph()
        p_b.space_before = Pt(12)
        run_t = p_b.add_run()
        run_t.text = "• " + title
        run_t.font.bold = True
        run_t.font.size = Pt(12)
        run_t.font.color.rgb = WHITE
        run_d = p_b.add_run()
        run_d.text = desc
        run_d.font.size = Pt(12)
        run_d.font.color.rgb = TEXT_MUTED

    # Right card: Placell Solution
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    c2_box = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf2_2 = c2_box.text_frame
    tf2_2.word_wrap = True

    p = tf2_2.paragraphs[0]
    p.text = "The Placell Solution"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_EMERALD

    bullets_c2 = [
        ("Centralized Knowledge Ingestion: ", "Single enterprise portal to record structured round data and free-form narrative interview feedback."),
        ("Natural Language Processing: ", "Automated NLP mining to extract sentiment polarity, technical skills, and frequently tested topics."),
        ("Explainable Skill Gap Analysis: ", "Real-time alignment between individual student profiles and live industry benchmarks with statistical justifications."),
        ("Multi-Tier Governance: ", "Role-scoped workspaces for Students, Placement Directorate Officers, Faculty Coordinators, and Administrators.")
    ]
    for title, desc in bullets_c2:
        p_b = tf2_2.add_paragraph()
        p_b.space_before = Pt(12)
        run_t = p_b.add_run()
        run_t.text = "✓ " + title
        run_t.font.bold = True
        run_t.font.size = Pt(12)
        run_t.font.color.rgb = WHITE
        run_d = p_b.add_run()
        run_d.text = desc
        run_d.font.size = Pt(12)
        run_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s2, "In higher education institutions, campus placement data is severely underutilized. Valuable qualitative feedback from interview experiences disappears when students graduate. Placell transforms this scattered qualitative feedback into an enterprise intelligence system using NLP and explainable analytics.")

    # =========================================================================
    # SLIDE 3: Academic Curriculum Mapping
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, "Explicit Academic Curriculum Mapping", "CORE CURRICULUM SYLLABUS")

    subjects = [
        ("ES", "Enterprise Systems", PRIMARY_BLUE, [
            "Centralized Relational Architecture: 10+ normalized entities in PostgreSQL/SQLAlchemy.",
            "4-Tier RBAC: Distinct permissions for Student, Placement Officer, Faculty, and Admin.",
            "Enterprise Moderation Workflow: TPO review queue authorizing student feedback before publication.",
            "Immutable Audit Trail: Timestamped tracking of logins, submissions, and status mutations.",
            "Department Scoping: Faculty dashboards isolated by academic department."
        ]),
        ("ITPM", "IT Project Management", ACCENT_INDIGO, [
            "Agile/Scrum Lifecycle: 14-week realistic single-engineer delivery schedule (7 sprints).",
            "Project Charter & WBS: Strict boundary definitions preventing scope creep.",
            "Risk Management: Formal 5-factor risk register with mitigation strategies.",
            "Cost Estimation: Open-source local execution yielding $0 direct expenditure.",
            "Quality Assurance: Pytest integration testing & automated build verification."
        ]),
        ("ASTMA", "Advanced Technologies", SUCCESS_EMERALD, [
            "NLP Sentiment Polarity: Calibrated lexicon and score distribution (Positive / Neutral / Negative).",
            "Skill Entity Matcher: 150+ technology taxonomy with boundary regex tokenization.",
            "Topic & Difficulty Extractor: Detection of DSA, System Design, and question difficulty.",
            "Supervised Tabular Readiness: Objective academic & technical readiness estimation.",
            "Explainable Recommendations: Frequency-backed rationale without black-box opacity."
        ]),
    ]

    for idx, (code, title, color, points) in enumerate(subjects):
        c_left = Inches(0.8 + (idx * 3.95))
        add_card(s3, c_left, Inches(1.8), Inches(3.8), Inches(5.0))
        box = s3.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.4), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p_code = tf.paragraphs[0]
        p_code.text = f"[{code}]"
        p_code.font.size = Pt(14)
        p_code.font.bold = True
        p_code.font.color.rgb = color

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(17)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE
        p_title.space_before = Pt(2)

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.space_before = Pt(8)
            parts = pt.split(":")
            r1 = p_pt.add_run()
            r1.text = "• " + parts[0] + ":"
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = WHITE
            r2 = p_pt.add_run()
            r2.text = parts[1]
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s3, "This slide is the core academic anchor of my final-year project. I explicitly demonstrate three university subjects: Enterprise Systems through RBAC, audit logging, and normalized schema; ITPM through solo Agile sprint scheduling, WBS, and risk analysis; and ASTMA through applied NLP and explainable machine learning.")

    # =========================================================================
    # SLIDE 4: System Architecture & Layered Monolith
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, "Layered System Architecture", "SOFTWARE ARCHITECTURE")

    layers = [
        ("1. Presentation Layer (Vite + React 19 + TypeScript + Tailwind)", PRIMARY_BLUE, [
            "Responsive Single Page Application (SPA) designed for desktop and mobile browsers.",
            "Role-based dynamic layouts (Navbar, Sidebar) adapting navigation based on user claims.",
            "Interactive charts rendered via Recharts (Bar, Line, Pie, Radar charts) and Lucide icons."
        ]),
        ("2. API & Security Layer (FastAPI + JWT + RBAC Guards)", ACCENT_INDIGO, [
            "OAuth2 password bearer specification with signed HS256 JWT access tokens.",
            "FastAPI dependency injection verifying roles: RequireRoles([ADMIN, TPO, FACULTY, STUDENT]).",
            "CORS middleware, input sanitization, and automated interceptor for immutable audit logs."
        ]),
        ("3. Service & ASTMA Intelligence Engine (Python 3.14)", SUCCESS_EMERALD, [
            "Decoupled business logic: StudentService, DriveService, CompanyService, AnalyticsService.",
            "SentimentAnalyzer: Calibrated text polarity with prior user rating blending.",
            "SkillExtractor & TopicAnalyzer: Boundary regex tokenizer with 150+ taxonomy.",
            "PlacementReadinessModel: Multi-factor tabular scoring with non-discriminatory ethical rules."
        ]),
        ("4. Persistence & Data Access (SQLAlchemy 2.0 + PostgreSQL / SQLite)", WARNING_AMBER, [
            "Declarative relational models with foreign keys, unique constraints, and cascade delete.",
            "Fully portable: Operates seamlessly on local SQLite for live demo or PostgreSQL in production."
        ])
    ]

    for idx, (title, color, points) in enumerate(layers):
        top_y = Inches(1.8 + (idx * 1.25))
        add_card(s4, Inches(0.8), top_y, Inches(11.7), Inches(1.15))
        box = s4.shapes.add_textbox(Inches(1.0), top_y + Inches(0.12), Inches(11.3), Inches(0.95))
        tf = box.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(3)
        p_d.text = "   • " + "   • ".join(points)
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s4, "I chose a clean layered modular monolith pattern over microservices. For a solo student project, microservices introduce excessive deployment overhead. A modular monolith provides enterprise separation of concerns between presentation, API routing, business services, and database persistence.")

    # =========================================================================
    # SLIDE 5: Enterprise Systems (ES) Deep-Dive
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, "Enterprise Systems (ES) Implementation", "ES CORE MODULE")

    es_blocks = [
        ("Role-Based Access Control (RBAC)", PRIMARY_BLUE, [
            ("Student: ", "Manages own portfolio, views personal readiness, runs skill gap analyzer, submits reviews."),
            ("Placement Officer (TPO): ", "Schedules placement drives, moderates student reviews, reviews institutional conversion metrics."),
            ("Faculty Coordinator: ", "Department-scoped access; analyzes departmental skill gaps to tailor training."),
            ("System Admin: ", "Full access; manages accounts, updates master skills dictionary, inspects audit logs.")
        ]),
        ("Enterprise Workflow & Governance", SUCCESS_EMERALD, [
            ("Dual-Modal Submission: ", "Enforces both structured round parameters and free-text narrative for auditability."),
            ("Moderation Queue: ", "TPO can approve or reject reviews with recorded justification before publication."),
            ("Immutable Audit Trail: ", "Captures Actor, Timestamp, IP Address, Action, and Entity ID on critical events."),
            ("Data Privacy Safeguards: ", "Strict anonymization of student roll numbers in public analytics aggregations.")
        ])
    ]

    for idx, (title, color, items) in enumerate(es_blocks):
        left_pos = Inches(0.8 + (idx * 5.95))
        add_card(s5, left_pos, Inches(1.8), Inches(5.8), Inches(5.0))
        box = s5.shapes.add_textbox(left_pos + Inches(0.3), Inches(2.0), Inches(5.2), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        for heading, body in items:
            p_item = tf.add_paragraph()
            p_item.space_before = Pt(10)
            r1 = p_item.add_run()
            r1.text = "• " + heading
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = WHITE
            r2 = p_item.add_run()
            r2.text = body
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s5, "Here is how Enterprise Systems concepts are demonstrated. Permissions are enforced at the API gateway via FastAPI dependency injection. Notice our moderation workflow: students submit experiences, but the placement directorate reviews them in a verification queue. Every critical change is logged in our audit table.")

    # =========================================================================
    # SLIDE 6: Relational Database Schema (ER Structure)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, "Normalized Database Design & Entities", "ENTERPRISE DATA ARCHITECTURE")

    # Table of entities
    rows = 6
    cols = 4
    table_shape = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.9))
    table = table_shape.table

    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(2.5)
    table.columns[3].width = Inches(3.8)

    headers = ["Entity Name", "Key Attributes", "Relational Constraints", "Enterprise Purpose"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = PRIMARY_BLUE

    data = [
        ("users & departments", "id (PK), email, hashed_pwd, role, department_id", "FK to departments, Unique email, Role Enum", "Authentication, RBAC enforcement, institutional scoping."),
        ("students & student_skills", "id (PK), user_id, cgpa, roll_number, projects_count", "1:1 with users, 1:N with skills, Cascade Delete", "Academic portfolio, proficiency ratings (Beginner/Adv)."),
        ("companies & job_roles", "id (PK), name, ctc_min/max, industry, min_cgpa", "1:N company to roles, M:N roles to required skills", "Recruiter catalog, compensation brackets, role benchmarks."),
        ("placement_drives & applications", "id (PK), company_id, drive_date, status, eligibility", "FK to company, job_role; 1:N applications", "Drive lifecycle (Upcoming/Active/Completed), application tracking."),
        ("placement_experiences & nlp_results", "id (PK), rating, feedback, sentiment, extracted_skills", "FK to student, company; 1:1 with NLP results", "Dual-modal logging, sentiment score, extracted taxonomy tags.")
    ]

    for r_idx, row_data in enumerate(data, start=1):
        for c_idx, text_val in enumerate(row_data):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_COLOR
            p = cell.text_frame.paragraphs[0]
            p.text = text_val
            p.font.size = Pt(11)
            p.font.color.rgb = WHITE if c_idx == 0 else TEXT_MUTED

    add_speaker_notes(s6, "The database schema is fully normalized into Third Normal Form. Notice the relationships: Users authenticate into Roles, Students link to Academic Departments and Skills, Companies sponsor Placement Drives, and Placement Experiences link to both structured Interview Rounds and automated NLP results.")

    # =========================================================================
    # SLIDE 7: ASTMA Natural Language Processing Pipeline
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7, "ASTMA: Qualitative Natural Language Processing", "ADVANCED TECHNOLOGIES")

    nlp_steps = [
        ("Step 1: Text Ingestion & Cleaning", PRIMARY_BLUE, [
            "Accepts free-form student feedback and questions asked.",
            "Normalizes case, expands English contractions, removes stop words.",
            "Cleans special characters while preserving technical tokens (e.g., C++, C#, .NET)."
        ]),
        ("Step 2: Calibrated Sentiment Classifier", ACCENT_INDIGO, [
            "Dual-factor polarity scoring combining placement domain lexicon with numerical ratings.",
            "Captures context modifiers: negations ('not fair') and intensifiers ('very tough').",
            "Outputs discrete label: POSITIVE (>=60%), NEUTRAL (40-60%), or NEGATIVE (<=40%) with confidence score."
        ]),
        ("Step 3: Boundary Regex Skill Entity Extractor", SUCCESS_EMERALD, [
            "Scans cleaned text against a curated taxonomy of 150+ skills across 7 domains.",
            "Word boundary regex (\b) prevents substring false positives (e.g., 'C' inside 'React').",
            "Automatically harmonizes synonyms (e.g., 'k8s' -> Kubernetes, 'reactjs' -> React)."
        ]),
        ("Step 4: Topic & Difficulty Inference", WARNING_AMBER, [
            "Categorizes rounds into Arrays/Strings, Trees/Graphs, DP, SQL, System Design, or HR.",
            "Infers interview difficulty (EASY, MODERATE, HARD) by evaluating keyword pressure."
        ])
    ]

    for idx, (title, color, points) in enumerate(nlp_steps):
        c_left = Inches(0.8 + (idx * 2.95))
        add_card(s7, c_left, Inches(1.8), Inches(2.85), Inches(5.0))
        box = s7.shapes.add_textbox(c_left + Inches(0.15), Inches(2.0), Inches(2.55), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.space_before = Pt(10)
            p_pt.text = "• " + pt
            p_pt.font.size = Pt(11)
            p_pt.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s7, "For ASTMA, we built a deterministic, reproducible NLP pipeline. When a student writes 'The technical interview grilled me on SQL joins and Python OOP', our pipeline extracts 'SQL' and 'Python', infers positive or neutral sentiment, and tags Database and OOP as core topics.")

    # =========================================================================
    # SLIDE 8: ASTMA Placement Readiness Estimator
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8, "ASTMA: Explainable Placement Readiness Model", "PREDICTIVE ANALYTICS")

    # Left card: Mathematics and Features
    add_card(s8, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    b1 = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.5))
    tf8_1 = b1.text_frame
    tf8_1.word_wrap = True

    p = tf8_1.paragraphs[0]
    p.text = "Supervised Tabular Feature Vector"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    feats = [
        ("Academic CGPA Foundation (25% Weight): ", "Normalized scaling across standard 0 to 10 scale."),
        ("Technical Skills Depth (25% Weight): ", "Verified technical and soft skills count logged in student inventory."),
        ("Target Role Alignment (25% Weight): ", "Direct Jaccard overlap ratio between possessed skills and target recruiter requirements."),
        ("Project Portfolio (15% Weight): ", "Completed engineering capstones and complex GitHub repositories."),
        ("Industry Experience (10% Weight): ", "Completed industry internships and professional certifications.")
    ]
    for name, desc in feats:
        p_f = tf8_1.add_paragraph()
        p_f.space_before = Pt(8)
        r1 = p_f.add_run()
        r1.text = "• " + name
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = WHITE
        r2 = p_f.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right card: Tiers & Ethics
    add_card(s8, Inches(7.2), Inches(1.8), Inches(5.3), Inches(5.0))
    b2 = s8.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.9), Inches(4.5))
    tf8_2 = b2.text_frame
    tf8_2.word_wrap = True

    p = tf8_2.paragraphs[0]
    p.text = "Readiness Tiers & Ethical Guardrails"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_EMERALD

    tiers = [
        ("Strong Candidate (>= 85%): ", "Exceptional academic credentials, full target skill alignment, projects."),
        ("Placement Ready (70% - 84%): ", "Meets major recruiter requirements; eligible for tier-1 campus drives."),
        ("Developing (50% - 69%): ", "Solid foundations; targeted skill improvement recommended."),
        ("Needs Improvement (< 50%): ", "Immediate skill-gap interventions and faculty mentorship indicated.")
    ]
    for name, desc in tiers:
        p_t = tf8_2.add_paragraph()
        p_t.space_before = Pt(6)
        r1 = p_t.add_run()
        r1.text = "✓ " + name
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = WHITE
        r2 = p_t.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    p_eth = tf8_2.add_paragraph()
    p_eth.space_before = Pt(14)
    r_eth = p_eth.add_run()
    r_eth.text = "ETHICAL NON-DISCRIMINATORY GUARANTEE:\n"
    r_eth.font.bold = True
    r_eth.font.size = Pt(11)
    r_eth.font.color.rgb = WARNING_AMBER
    r_eth2 = p_eth.add_run()
    r_eth2.text = "Strictly excludes demographic, gender, religious, or socioeconomic traits. Formulated purely as an educational decision-support estimate, not an employment guarantee."
    r_eth2.font.size = Pt(10)
    r_eth2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s8, "Our placement readiness model is completely transparent. We do not use black-box neural networks that cannot be explained. We formulate an objective 5-part feature vector. Most importantly, as required by AI ethics, we strictly exclude all demographic attributes.")

    # =========================================================================
    # SLIDE 9: Explainable Skill-Gap Analyzer & Recommendations
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9, "Explainable Skill-Gap & Recommendation Engine", "DECISION SUPPORT SYSTEM")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    b9 = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.5))
    tf9 = b9.text_frame
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = "Mathematical Set-Difference & Statistical Justification"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO

    p_eq = tf9.add_paragraph()
    p_eq.space_before = Pt(6)
    p_eq.text = "Skill Gap = S_Required(Target Role / Company) \\ S_Acquired(Student Profile)"
    p_eq.font.size = Pt(13)
    p_eq.font.bold = True
    p_eq.font.color.rgb = PRIMARY_BLUE

    steps = [
        ("1. Benchmark Extraction: ", "Retrieves required skill vector from active job roles and verified recruiter drive experiences."),
        ("2. Set Intersection & Competency Audit: ", "Identifies possessed skills (e.g., Python, SQL, Git) versus missing requirements (e.g., Docker, Power BI)."),
        ("3. Statistical Demand Weighting: ", "Computes the exact historical market frequency of missing skills across all verified company drives."),
        ("4. Explainable Rationale Generation (XAI): ", "Constructs auditable justifications. Example: 'Docker is recommended because it appeared in 68% of Cloud Engineer placement rounds, but is currently missing from your profile.'"),
        ("5. Actionable Roadmap Synthesis: ", "Provides actionable milestones: concept review, GitHub project integration, and problem set practice.")
    ]

    for title, desc in steps:
        p_s = tf9.add_paragraph()
        p_s.space_before = Pt(10)
        r1 = p_s.add_run()
        r1.text = "• " + title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = WHITE
        r2 = p_s.add_run()
        r2.text = desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s9, "Module 10 and 12 implement our Explainable Recommendation Engine. In traditional systems, recommendations are black-box suggestions. In Placell, every single recommendation shows WHY it was generated, citing the exact historical percentage of campus drives that tested that skill.")

    # =========================================================================
    # SLIDE 10: ITPM Project Management & 14-Week Roadmap
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_header(s10, "ITPM: 14-Week Solo Agile/Scrum Delivery Plan", "PROJECT MANAGEMENT ARTIFACT")

    # Table of 7 Sprints
    rows = 8
    cols = 4
    table_shape10 = s10.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.9))
    t10 = table_shape10.table

    t10.columns[0].width = Inches(1.5)
    t10.columns[1].width = Inches(2.0)
    t10.columns[2].width = Inches(5.8)
    t10.columns[3].width = Inches(2.4)

    h_itpm = ["Sprint", "Timeline", "Core Objectives & Deliverables", "Methodology State"]
    for c_idx, h in enumerate(h_itpm):
        cell = t10.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = PRIMARY_BLUE

    sprints_data = [
        ("Sprint 1", "Weeks 1 - 2", "Scope formulation, normalized database schemas, JWT auth engine, RBAC middleware.", "COMPLETED (Verified)"),
        ("Sprint 2", "Weeks 3 - 4", "Master entities CRUD: Departments, Skills catalog, Companies, Job Roles, Drives.", "COMPLETED (Verified)"),
        ("Sprint 3", "Weeks 5 - 6", "Student profile portfolio, interview logging wizard, TPO moderation queue.", "COMPLETED (Verified)"),
        ("Sprint 4", "Weeks 7 - 8", "ASTMA NLP pipeline: sentiment classifier, boundary skill extractor, topics.", "COMPLETED (Verified)"),
        ("Sprint 5", "Weeks 9 - 10", "Readiness scoring model, explainable skill-gap analyzer, frequency recommendations.", "COMPLETED (Verified)"),
        ("Sprint 6", "Weeks 11 - 12", "React 19 enterprise dashboards (Student, TPO, Admin, Faculty) with Recharts.", "COMPLETED (Verified)"),
        ("Sprint 7", "Weeks 13 - 14", "Pytest automated integration test suite, synthetic data seeding, viva preparation.", "COMPLETED (Verified)")
    ]

    for r_idx, (sp, time_val, obj_val, st_val) in enumerate(sprints_data, start=1):
        t10.cell(r_idx, 0).text = sp
        t10.cell(r_idx, 1).text = time_val
        t10.cell(r_idx, 2).text = obj_val
        t10.cell(r_idx, 3).text = st_val
        for c in range(4):
            cell = t10.cell(r_idx, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_COLOR
            cell.text_frame.paragraphs[0].font.size = Pt(10)
            if c == 0:
                cell.text_frame.paragraphs[0].font.bold = True
                cell.text_frame.paragraphs[0].font.color.rgb = WHITE
            elif c == 3:
                cell.text_frame.paragraphs[0].font.color.rgb = SUCCESS_EMERALD
            else:
                cell.text_frame.paragraphs[0].font.color.rgb = TEXT_MUTED

    add_speaker_notes(s10, "For IT Project Management, I structured the project around a 14-week Agile lifecycle tailored for a single student engineer. Rather than a vague plan, we executed seven 2-week sprints, achieving 100% of milestones ahead of schedule.")

    # =========================================================================
    # SLIDE 11: ITPM Risk Register & Mitigation Strategy
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11)
    add_header(s11, "ITPM: Formal Risk Register & Mitigation Matrix", "RISK MANAGEMENT ARTIFACT")

    rows = 6
    cols = 5
    table_shape11 = s11.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.9))
    t11 = table_shape11.table

    t11.columns[0].width = Inches(1.2)
    t11.columns[1].width = Inches(3.2)
    t11.columns[2].width = Inches(1.3)
    t11.columns[3].width = Inches(1.3)
    t11.columns[4].width = Inches(4.7)

    h_risk = ["Risk ID", "Identified Risk Event", "Severity", "Likelihood", "Mitigation Strategy Implemented"]
    for c_idx, h in enumerate(h_risk):
        cell = t11.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = PRIMARY_BLUE

    risks = [
        ("R-01", "Short Feedback Reviews (NLP Cold Start)", "HIGH", "MED", "Dual-modal submission requires tagged skills tested alongside free-text narrative."),
        ("R-02", "Student Privacy Infringement", "HIGH", "LOW", "Query-level anonymization; private profile data completely stripped in aggregate reports."),
        ("R-03", "Model Bias & Unethical Predictions", "CRITICAL", "LOW", "Strict exclusion of demographic attributes; designated as decision-support estimate."),
        ("R-04", "Scope Creep for Solo Engineer", "HIGH", "MED", "Modular monolith architecture (FastAPI + Vite React) avoiding microservices bloat."),
        ("R-05", "Empty Database Demo Failure", "CRITICAL", "LOW", "Built-in synthetic seeder generates 100 students, 25 companies, and 114 reviews on boot.")
    ]

    for r_idx, (rid, rev, sev, lik, mit) in enumerate(risks, start=1):
        t11.cell(r_idx, 0).text = rid
        t11.cell(r_idx, 1).text = rev
        t11.cell(r_idx, 2).text = sev
        t11.cell(r_idx, 3).text = lik
        t11.cell(r_idx, 4).text = mit
        for c in range(5):
            cell = t11.cell(r_idx, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_COLOR
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if c == 0:
                p.font.bold = True
                p.font.color.rgb = WHITE
            elif c == 2 and sev == "CRITICAL":
                p.font.bold = True
                p.font.color.rgb = WARNING_AMBER
            elif c == 4:
                p.font.color.rgb = SUCCESS_EMERALD
            else:
                p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s11, "Risk management is a critical chapter in ITPM. I identified 5 primary technical and operational risks. For instance, risk R-03 was model bias, mitigated by strictly eliminating demographic attributes. Risk R-05 was an empty database during defense, mitigated by our automatic seed script.")

    # =========================================================================
    # SLIDE 12: ITPM Resource Allocation & Cost Estimation
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12)
    add_header(s12, "ITPM: Resource Plan & Zero-Budget Costing", "FEASIBILITY & COST ESTIMATION")

    cost_items = [
        ("Engineering Effort (Solo Labor)", PRIMARY_BLUE, [
            "1 Solo Undergraduate Student Developer.",
            "20 productive hours per week over 14 weeks = 280 Engineering Hours.",
            "Fully delivered within academic capstone curriculum ($0 direct cost)."
        ]),
        ("Hardware Compute Environment", ACCENT_INDIGO, [
            "Existing personal workstation (Windows 11, local compute).",
            "Zero requirement for external cloud GPUs, server clusters, or paid hardware.",
            "Strictly compliant with the prompt's zero IoT hardware constraint."
        ]),
        ("Open-Source Technology Stack", SUCCESS_EMERALD, [
            "Backend: Python 3.14, FastAPI, SQLAlchemy 2.0, Pydantic V2 (MIT License).",
            "Frontend: React 19, TypeScript, Vite 8, Tailwind CSS v4, Recharts (MIT License).",
            "Persistence: PostgreSQL 16 / SQLite Engine (Zero licensing overhead)."
        ]),
        ("Total Financial Expenditure", WARNING_AMBER, [
            "Direct Capital Outlay: ₹0 / $0.",
            "100% reproducible on any standard university laptop or computer lab machine.",
            "Sustainable and permanent academic institutional viability."
        ])
    ]

    for idx, (title, color, points) in enumerate(cost_items):
        c_left = Inches(0.8 + (idx * 2.95))
        add_card(s12, c_left, Inches(1.8), Inches(2.85), Inches(5.0))
        box = s12.shapes.add_textbox(c_left + Inches(0.15), Inches(2.0), Inches(2.55), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.space_before = Pt(10)
            p_pt.text = "• " + pt
            p_pt.font.size = Pt(11)
            p_pt.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s12, "Under ITPM Cost Management, the project was deliberately engineered for zero budget. By selecting FastAPI, SQLite/PostgreSQL, React, and Scikit-learn, the entire application runs locally on standard student laptops with zero cloud subscription expenses.")

    # =========================================================================
    # SLIDE 13: UI/UX Design & User Experience
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13)
    add_header(s13, "User Experience & Enterprise Dashboards", "UI/UX DESIGN SYSTEM")

    ui_cards = [
        ("Student Personal Workspace", PRIMARY_BLUE, [
            "Placement Readiness Gauge: Dynamic score visualization (0-100%) with tier badges.",
            "Feature Contribution Breakdown: Explainable transparency for CGPA, skills, and projects.",
            "Skill-Gap Matrix: Color-coded matched competencies vs. missing requirements.",
            "Review Submission Wizard: Dynamic rounds builder with live NLP feedback."
        ]),
        ("Placement Cell Directorate (TPO)", ACCENT_INDIGO, [
            "Institutional Command Center: Macro KPIs on student conversion and partner drives.",
            "Experience Moderation Queue: One-click verification or rejection with moderator notes.",
            "Corporate Directory: Compensation brackets (LPA) and deep-dive analytics modal.",
            "Campus Drives Scheduler: Eligibility CGPA thresholds and applicant tracking."
        ]),
        ("Analytics & Administrative Suite", SUCCESS_EMERALD, [
            "Sentiment Polarity Charts: Interactive Recharts pie breakdown across verified reviews.",
            "Top Demanded Skills: Horizontal bar chart indexing recruiter skill frequency.",
            "Department Comparison: Faculty cohort analytics comparing CSE, CSBS, AIML, and IT.",
            "Immutable Audit Trail: Searchable log table recording user actions and security events."
        ])
    ]

    for idx, (title, color, points) in enumerate(ui_cards):
        c_left = Inches(0.8 + (idx * 3.95))
        add_card(s13, c_left, Inches(1.8), Inches(3.8), Inches(5.0))
        box = s13.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.4), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.space_before = Pt(10)
            parts = pt.split(":")
            r1 = p_pt.add_run()
            r1.text = "• " + parts[0] + ":"
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = WHITE
            r2 = p_pt.add_run()
            r2.text = parts[1]
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s13, "The user interface adheres to clean enterprise design principles. We utilized Tailwind CSS with Plus Jakarta Sans typography. The login page includes one-click demo persona buttons so examiners can immediately experience the interface from all 4 role perspectives.")

    # =========================================================================
    # SLIDE 14: Quality Assurance & Automated Testing
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_background(s14)
    add_header(s14, "Quality Assurance & Automated Verification", "TESTING & VALIDATION")

    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    b14_1 = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.5))
    tf14_1 = b14_1.text_frame
    tf14_1.word_wrap = True

    p = tf14_1.paragraphs[0]
    p.text = "Automated Pytest Suite (100% Pass)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_EMERALD

    test_cases = [
        ("test_health_check: ", "Verifies operational status of all ES, NLP, and readiness subsystems."),
        ("test_student_login_and_profile: ", "Validates JWT token issuance, protected profile lookup, and readiness calculation."),
        ("test_analytics_overview: ", "Ensures accurate computation of college KPIs, sentiment distributions, and department metrics."),
        ("test_experience_submission_and_nlp: ", "Submits narrative feedback and asserts automated NLP extraction of sentiment labels and skill entities.")
    ]
    for name, desc in test_cases:
        p_t = tf14_1.add_paragraph()
        p_t.space_before = Pt(10)
        r1 = p_t.add_run()
        r1.text = "✓ " + name
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = WHITE
        r2 = p_f.add_run() if False else p_t.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    # Right Card: Synthetic Seeding & Build Quality
    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    b14_2 = s14.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf14_2 = b14_2.text_frame
    tf14_2.word_wrap = True

    p = tf14_2.paragraphs[0]
    p.text = "Verification Metrics & Data Scale"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE

    scale_metrics = [
        ("Pre-Seeded Synthetic Cohort: ", "100 students across 4 engineering departments (CSE, CSBS, AIML, IT)."),
        ("Recruiter Network: ", "25 companies (Google, Microsoft, Amazon, Razorpay, TCS, etc.) with 45+ job roles."),
        ("Campus Drives: ", "18 active and completed placement drives with tracked applicant statuses."),
        ("Verified Experiences Knowledge Base: ", "114 placement experiences fully analyzed with sentiment, difficulty, and skill tags."),
        ("Frontend Production Bundle: ", "Vite build transforms 2,541 modules in 1.41 seconds with 0 TypeScript or lint errors.")
    ]
    for name, desc in scale_metrics:
        p_m = tf14_2.add_paragraph()
        p_m.space_before = Pt(10)
        r1 = p_m.add_run()
        r1.text = "• " + name
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = WHITE
        r2 = p_m.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s14, "Quality Assurance is fully automated. Our pytest suite verifies authentication, student profiles, analytical aggregations, and NLP extraction. Additionally, our database seed script pre-populates over 100 students and 114 verified experiences so examiners can inspect live data immediately.")

    # =========================================================================
    # SLIDE 15: Limitations & Future Scope
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    apply_background(s15)
    add_header(s15, "Project Limitations & Future Scope", "SYSTEM EXTENSIBILITY")

    lim_items = [
        ("Current System Limitations", WARNING_AMBER, [
            ("Cold Start on Novel Skills: ", "Newly invented frameworks require updating the central skill dictionary."),
            ("English Language NLP Corpus: ", "Current text preprocessing is optimized for English interview reviews."),
            ("Self-Assessed Skill Proficiency: ", "Student skills are self-reported rather than verified by live coding tests.")
        ]),
        ("Future Roadmap & Extensions", PRIMARY_BLUE, [
            ("Automated Resume PDF Parsing: ", "Extract candidate skills and projects automatically via PDF OCR ingestion."),
            ("AI Mock Interview Simulator: ", "Interactive chat assessment generating real-time performance feedback."),
            ("Multi-College Federation: ", "Multi-tenant cloud architecture aggregating recruitment data across university clusters."),
            ("Live Alumni Mentorship Matching: ", "Pairing junior students with placed alumni based on shared skill gap targets.")
        ])
    ]

    for idx, (title, color, items) in enumerate(lim_items):
        c_left = Inches(0.8 + (idx * 5.95))
        add_card(s15, c_left, Inches(1.8), Inches(5.8), Inches(5.0))
        box = s15.shapes.add_textbox(c_left + Inches(0.3), Inches(2.0), Inches(5.2), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        for heading, body in items:
            p_item = tf.add_paragraph()
            p_item.space_before = Pt(12)
            r1 = p_item.add_run()
            r1.text = "• " + heading
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = WHITE
            r2 = p_item.add_run()
            r2.text = body
            r2.font.size = Pt(11)
            r2.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s15, "In an academic defense, acknowledging boundaries demonstrates engineering maturity. While Placell currently relies on an extensible skill dictionary and English text, our modular architecture makes it easy to integrate PDF resume parsing and AI mock interview simulations in the future.")

    # =========================================================================
    # SLIDE 16: Conclusion & Viva Voce Defense Summary
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    apply_background(s16)
    add_header(s16, "Conclusion & Academic Defense Summary", "VIVA VOCE CONCLUSION")

    add_card(s16, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    b16 = s16.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.5))
    tf16 = b16.text_frame
    tf16.word_wrap = True

    p = tf16.paragraphs[0]
    p.text = "Key Academic Contributions of Placell"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = SUCCESS_EMERALD

    summary_pts = [
        ("Full Curriculum Alignment: ", "Successfully maps to Enterprise Systems (RBAC, workflows, database, audit), ITPM (Agile sprints, WBS, risks, costing), and ASTMA (applied NLP, supervised ML, explainable AI)."),
        ("100% Software-Only Execution: ", "Achieved comprehensive career decision-support without requiring mandatory IoT sensors or hardware simulators."),
        ("High-Impact Institutional Value: ", "Solves the real-world higher education dilemma of lost placement feedback, transforming qualitative data into actionable student recommendations."),
        ("Production-Grade Codebase: ", "Built with modern standards (FastAPI, React 19, TypeScript, Tailwind, SQLAlchemy), automated test coverage, and instant demo seeding."),
        ("Ethical & Transparent AI: ", "Presents all machine learning outputs as educational decision-support tools with zero demographic bias.")
    ]

    for title, desc in summary_pts:
        p_pt = tf16.add_paragraph()
        p_pt.space_before = Pt(10)
        r1 = p_pt.add_run()
        r1.text = "✓ " + title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = WHITE
        r2 = p_pt.add_run()
        r2.text = desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = TEXT_MUTED

    p_close = tf16.add_paragraph()
    p_close.space_before = Pt(16)
    r_c = p_close.add_run()
    r_c.text = "THANK YOU! Open for Questions & Live System Demonstration."
    r_c.font.bold = True
    r_c.font.size = Pt(14)
    r_c.font.color.rgb = PRIMARY_BLUE

    add_speaker_notes(s16, "To conclude, Placell proves that an ambitious enterprise AI system can be planned, engineered, and tested by a single student following structured ITPM disciplines. The system is live, pre-seeded, and ready for demonstration. Thank you, and I look forward to your questions.")

    output_path = "d:/projects/docs/presentation/Placell_Final_Year_Viva_Presentation.pptx"
    prs.save(output_path)
    prs.save("d:/projects/docs/presentation/PlaceInsight_Final_Year_Viva_Presentation.pptx")
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
