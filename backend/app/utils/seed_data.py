import random
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.department import Department
from app.models.skill import Skill, SkillCategory
from app.models.company import Company, JobRole, JobRoleSkill
from app.models.placement_drive import PlacementDrive, Application, DriveStatus, ApplicationStatus
from app.models.experience import PlacementExperience, InterviewRound, ExperienceStatus, RoundType
from app.models.ai_results import NLPAnalysisResult, ReadinessEvaluation
from app.ai.sentiment_analyzer import sentiment_analyzer
from app.ai.skill_extractor import skill_extractor
from app.ai.topic_analyzer import topic_analyzer
from app.ai.readiness_model import readiness_model

def seed_database():
    """Initializes and seeds database with realistic academic and placement datasets."""
    print("Beginning Placell database seeding...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).filter(User.email == "admin@college.edu").first():
            print("Database already contains seed data. Skipping duplicate seed.")
            return

        # 1. Departments
        print("1/7 Seeding Departments...")
        depts_data = [
            ("CSE", "Computer Science & Engineering", "Computing, software systems, and algorithmic theory"),
            ("CSBS", "Computer Science & Business Systems", "Computing with business intelligence and enterprise strategy"),
            ("AIML", "Artificial Intelligence & Machine Learning", "Neural architectures, computer vision, and cognitive systems"),
            ("IT", "Information Technology", "Web infrastructure, cloud applications, and distributed software systems"),
        ]
        dept_map = {}
        for code, name, desc in depts_data:
            dept = Department(code=code, name=name, description=desc)
            db.add(dept)
            db.flush()
            dept_map[code] = dept

        # 2. Users (Roles)
        print("2/7 Seeding Role Users...")
        default_pw = get_password_hash("Pass@123")
        admin_user = User(
            email="admin@college.edu",
            hashed_password=default_pw,
            full_name="Dr. S. K. Raman (System Admin)",
            role=UserRole.ADMIN,
            is_active=True
        )
        tpo_user = User(
            email="tpo@college.edu",
            hashed_password=default_pw,
            full_name="Prof. Anita Verma (Placement Officer)",
            role=UserRole.TPO,
            is_active=True
        )
        faculty_user = User(
            email="faculty.cse@college.edu",
            hashed_password=default_pw,
            full_name="Dr. Rajesh Gupta (CSE Coordinator)",
            role=UserRole.FACULTY,
            department_id=dept_map["CSE"].id,
            is_active=True
        )
        test_student_user = User(
            email="student@college.edu",
            hashed_password=default_pw,
            full_name="Vedang Pewekar",
            role=UserRole.STUDENT,
            department_id=dept_map["CSBS"].id,
            is_active=True
        )
        db.add_all([admin_user, tpo_user, faculty_user, test_student_user])
        db.flush()

        # 3. Skills Dictionary
        print("3/7 Seeding Skills Taxonomy...")
        skills_raw = [
            # Programming
            ("Python", SkillCategory.PROGRAMMING), ("Java", SkillCategory.PROGRAMMING),
            ("C++", SkillCategory.PROGRAMMING), ("C", SkillCategory.PROGRAMMING),
            ("JavaScript", SkillCategory.PROGRAMMING), ("TypeScript", SkillCategory.PROGRAMMING),
            ("Go", SkillCategory.PROGRAMMING), ("Rust", SkillCategory.PROGRAMMING),
            ("C#", SkillCategory.PROGRAMMING), ("SQL", SkillCategory.PROGRAMMING),
            # Databases
            ("DBMS", SkillCategory.DATABASE), ("MySQL", SkillCategory.DATABASE),
            ("PostgreSQL", SkillCategory.DATABASE), ("MongoDB", SkillCategory.DATABASE),
            ("Redis", SkillCategory.DATABASE), ("Oracle", SkillCategory.DATABASE),
            ("Cassandra", SkillCategory.DATABASE),
            # Core CS
            ("Data Structures", SkillCategory.CORE_CS), ("Algorithms", SkillCategory.CORE_CS),
            ("System Design", SkillCategory.CORE_CS), ("Operating Systems", SkillCategory.CORE_CS),
            ("Computer Networks", SkillCategory.CORE_CS), ("OOP", SkillCategory.CORE_CS),
            # Frameworks
            ("React", SkillCategory.FRAMEWORK), ("Node.js", SkillCategory.FRAMEWORK),
            ("FastAPI", SkillCategory.FRAMEWORK), ("Express", SkillCategory.FRAMEWORK),
            ("Django", SkillCategory.FRAMEWORK), ("Spring Boot", SkillCategory.FRAMEWORK),
            ("REST APIs", SkillCategory.FRAMEWORK), ("GraphQL", SkillCategory.FRAMEWORK),
            ("Next.js", SkillCategory.FRAMEWORK), ("Angular", SkillCategory.FRAMEWORK),
            # Cloud & DevOps
            ("AWS", SkillCategory.CLOUD_DEVOPS), ("Azure", SkillCategory.CLOUD_DEVOPS),
            ("Docker", SkillCategory.CLOUD_DEVOPS), ("Kubernetes", SkillCategory.CLOUD_DEVOPS),
            ("Git", SkillCategory.CLOUD_DEVOPS), ("Linux", SkillCategory.CLOUD_DEVOPS),
            ("CI/CD", SkillCategory.CLOUD_DEVOPS),
            # AI & Data
            ("Machine Learning", SkillCategory.AI_ML), ("Deep Learning", SkillCategory.AI_ML),
            ("NLP", SkillCategory.AI_ML), ("Pandas", SkillCategory.AI_ML),
            ("NumPy", SkillCategory.AI_ML), ("Scikit-learn", SkillCategory.AI_ML),
            ("Power BI", SkillCategory.AI_ML), ("Tableau", SkillCategory.AI_ML),
            ("Excel", SkillCategory.AI_ML), ("Statistics", SkillCategory.AI_ML),
            # Soft Skills
            ("Communication", SkillCategory.SOFT_SKILL), ("Problem Solving", SkillCategory.SOFT_SKILL),
            ("Leadership", SkillCategory.SOFT_SKILL), ("Teamwork", SkillCategory.SOFT_SKILL),
            ("Critical Thinking", SkillCategory.SOFT_SKILL),
        ]
        skill_objs = []
        for s_name, s_cat in skills_raw:
            s_obj = Skill(name=s_name, category=s_cat)
            db.add(s_obj)
            skill_objs.append(s_obj)
        db.flush()
        skill_dict = {s.name: s for s in skill_objs}

        # 4. Companies & Job Roles
        print("4/7 Seeding Corporate Recruiters & Roles...")
        companies_seed = [
            ("Google", "Information Technology", "Product", "Bangalore / Hyderabad", 18.0, 32.0, "Global search and software company."),
            ("Microsoft", "Information Technology", "Product", "Hyderabad / Noida", 16.0, 28.0, "Enterprise software, cloud, and AI."),
            ("Amazon", "E-Commerce & Cloud", "Product", "Bangalore / Chennai", 15.0, 26.0, "E-commerce and AWS cloud platform."),
            ("Razorpay", "FinTech", "Product", "Bangalore", 14.0, 24.0, "Payment gateway and financial infrastructure."),
            ("Swiggy", "Consumer Tech", "Product", "Bangalore", 12.0, 22.0, "On-demand food delivery and quick commerce."),
            ("Zomato", "Consumer Tech", "Product", "Gurgaon", 12.0, 20.0, "Dining discovery and instant logistics."),
            ("Adobe", "Software & Creative", "Product", "Noida / Bangalore", 15.0, 25.0, "Digital media and creative tools."),
            ("Salesforce", "Enterprise Cloud", "Product", "Hyderabad", 16.0, 27.0, "CRM and enterprise cloud applications."),
            ("JPMorgan Chase", "Banking & Finance", "Product", "Mumbai / Bangalore", 13.0, 20.0, "Investment banking and technology solutions."),
            ("Goldman Sachs", "Investment Banking", "Product", "Bangalore", 16.0, 26.0, "Financial instruments and quantitative trading."),
            ("Cisco", "Networking & Cloud", "Product", "Bangalore", 12.0, 18.0, "Networking hardware, telecom, and security."),
            ("Oracle", "Database & Cloud", "Product", "Bangalore / Hyderabad", 11.0, 18.0, "Enterprise databases and cloud ERP."),
            ("Infosys", "IT Services", "Service", "Pan-India", 4.5, 9.5, "Global IT consulting and digital transformation."),
            ("Tata Consultancy Services", "IT Services", "Service", "Pan-India", 4.0, 8.5, "IT services and consulting conglomerate."),
            ("Wipro", "IT Services", "Service", "Pan-India", 4.0, 8.0, "Global IT consulting and services."),
            ("Accenture", "Management & IT", "Service", "Pan-India", 5.0, 11.0, "Digital consulting and operations."),
            ("Cognizant", "IT Services", "Service", "Chennai / Bangalore", 4.5, 9.0, "Technology consulting and business services."),
            ("Walmart Global Tech", "Retail Tech", "Product", "Bangalore / Chennai", 14.0, 23.0, "Global retail technology and supply chain."),
            ("Uber", "Transportation Tech", "Product", "Hyderabad / Bangalore", 18.0, 30.0, "Mobility and autonomous routing systems."),
            ("PhonePe", "FinTech", "Product", "Bangalore", 13.0, 22.0, "UPI and mobile financial ecosystems."),
            ("Flipkart", "E-Commerce", "Product", "Bangalore", 14.0, 24.0, "Online retail marketplace and supply chain."),
            ("ServiceNow", "Enterprise SaaS", "Product", "Hyderabad", 15.0, 24.0, "Cloud workflow and automation platform."),
            ("Intuit", "Financial SaaS", "Product", "Bangalore", 15.0, 25.0, "Financial management tools (TurboTax, QuickBooks)."),
            ("Qualcomm", "Semiconductors", "Product", "Hyderabad / Bangalore", 14.0, 22.0, "Wireless technology, 5G, and chipsets."),
            ("NVIDIA", "AI & Hardware", "Product", "Bangalore / Pune", 18.0, 34.0, "GPUs, accelerated computing, and AI architectures."),
        ]

        created_companies = []
        created_roles = []
        for c_name, ind, ctype, loc, cmin, cmax, desc in companies_seed:
            comp = Company(
                name=c_name, industry=ind, company_type=ctype,
                location=loc, ctc_min_lpa=cmin, ctc_max_lpa=cmax,
                description=desc
            )
            db.add(comp)
            db.flush()
            created_companies.append(comp)

            # Assign roles
            sde_role = JobRole(company_id=comp.id, title="Software Development Engineer (SDE-1)", min_cgpa=7.0, description="Backend and distributed systems development.")
            db.add(sde_role)
            db.flush()
            created_roles.append(sde_role)

            # Assign skills to role
            sde_skills = ["Data Structures", "Algorithms", "SQL", "DBMS", "REST APIs", "Python", "OOP"]
            for s_name in sde_skills:
                if s_name in skill_dict:
                    db.add(JobRoleSkill(job_role_id=sde_role.id, skill_id=skill_dict[s_name].id, importance_weight=1.5))

            if ctype == "Product":
                da_role = JobRole(company_id=comp.id, title="Data Analyst / ML Engineer", min_cgpa=6.8, description="Analytical models and business intelligence.")
                db.add(da_role)
                db.flush()
                created_roles.append(da_role)
                for s_name in ["Python", "SQL", "Pandas", "Power BI", "Statistics", "Machine Learning"]:
                    if s_name in skill_dict:
                        db.add(JobRoleSkill(job_role_id=da_role.id, skill_id=skill_dict[s_name].id, importance_weight=1.2))

        db.flush()

        # 5. Placement Drives
        print("5/7 Seeding Placement Drives...")
        created_drives = []
        for i, comp in enumerate(created_companies[:18]):
            role = [r for r in created_roles if r.company_id == comp.id][0]
            drive_status = DriveStatus.COMPLETED if i < 12 else (DriveStatus.ACTIVE if i < 15 else DriveStatus.UPCOMING)
            drive_date_val = date.today() - timedelta(days=(20 - i) * 7)
            drive = PlacementDrive(
                company_id=comp.id,
                job_role_id=role.id,
                title=f"{comp.name} Campus Drive 2026 - {role.title}",
                drive_date=drive_date_val,
                status=drive_status,
                eligibility_cgpa=role.min_cgpa,
                eligibility_criteria="Minimum 70% in 10th/12th, no active backlogs.",
                ctc_offered_lpa=round((comp.ctc_min_lpa + comp.ctc_max_lpa) / 2.0, 1),
                rounds_description="Online Coding Assessment (2 questions), Technical Interview 1, Technical Interview 2, HR Round."
            )
            db.add(drive)
            db.flush()
            created_drives.append(drive)

        # 6. Students (100 Students)
        print("6/7 Seeding Student Cohort...")
        first_names = ["Aarav", "Ananya", "Rohan", "Sneha", "Aditya", "Pooja", "Vikram", "Isha", "Rahul", "Priya",
                       "Siddharth", "Neha", "Karan", "Tanvi", "Arjun", "Divya", "Gaurav", "Kavya", "Manish", "Ritu"]
        last_names = ["Sharma", "Verma", "Gupta", "Patel", "Singh", "Reddy", "Mehta", "Iyer", "Nair", "Joshi"]

        created_students = []
        # First ensure test_student_user profile exists
        from app.models.student import Student, StudentSkill
        test_student = Student(
            user_id=test_student_user.id,
            roll_number="22CSBS001",
            department_id=dept_map["CSBS"].id,
            cgpa=8.45,
            graduation_year=2026,
            projects_count=3,
            internships_count=1,
            certifications_count=2,
            preferred_role_title="Software Development Engineer (SDE-1)",
            bio="Passionate full-stack & backend developer interested in scalable cloud APIs and algorithmic problem-solving."
        )
        db.add(test_student)
        db.flush()
        created_students.append(test_student)

        # Give test student rich skills
        for sk in ["Python", "JavaScript", "React", "SQL", "DBMS", "FastAPI", "Git", "Data Structures"]:
            if sk in skill_dict:
                db.add(StudentSkill(student_id=test_student.id, skill_id=skill_dict[sk].id, proficiency_level="Advanced"))

        # Seed 99 more students across departments
        dept_keys = list(dept_map.keys())
        for idx in range(2, 101):
            fname = random.choice(first_names)
            lname = random.choice(last_names)
            email_val = f"student.{idx}@{random.choice(dept_keys).lower()}.college.edu"
            dept_k = random.choice(dept_keys)
            user_s = User(
                email=email_val,
                hashed_password=default_pw,
                full_name=f"{fname} {lname}",
                role=UserRole.STUDENT,
                department_id=dept_map[dept_k].id,
                is_active=True
            )
            db.add(user_s)
            db.flush()

            cgpa_val = round(random.uniform(6.2, 9.8), 2)
            student_obj = Student(
                user_id=user_s.id,
                roll_number=f"22{dept_k}{idx:03d}",
                department_id=dept_map[dept_k].id,
                cgpa=cgpa_val,
                graduation_year=2026,
                projects_count=random.randint(1, 4),
                internships_count=random.randint(0, 2),
                certifications_count=random.randint(0, 3),
                preferred_role_title="Software Development Engineer (SDE-1)"
            )
            db.add(student_obj)
            db.flush()
            created_students.append(student_obj)

            # Assign random skills (4-7 skills each)
            picked_skills = random.sample(list(skill_dict.values()), random.randint(4, 7))
            for p_sk in picked_skills:
                db.add(StudentSkill(
                    student_id=student_obj.id,
                    skill_id=p_sk.id,
                    proficiency_level=random.choice(["Beginner", "Intermediate", "Advanced"])
                ))

        db.flush()

        # 7. Placement Experiences & NLP Results
        print("7/7 Seeding Placement Experiences & Processing NLP Pipeline...")
        sample_reviews = [
            ("The coding round had 2 questions on binary search and dynamic programming. Technical interview focused heavily on SQL joins, indexing, and Python OOP concepts. The panel was supportive and gave hints. Selected!", True, 5, 4),
            ("First round was standard aptitude followed by DSA questions on arrays and graphs. Technical round dug into DBMS normalization and REST API status codes. HR interview was friendly and conversational.", True, 4, 3),
            ("Rigorous technical interview on System Design and microservices architecture. Interviewer asked about database sharding, caching with Redis, and Docker containerization. Very challenging but fair.", True, 5, 5),
            ("Aptitude round was easy, but the coding round was very tough with graph shortest path questions. In the interview, they grilled me on Operating Systems memory management and deadlocks.", False, 3, 4),
            ("Smooth hiring experience! Round 1 was MCQs on OOP and DBMS. Round 2 was a live coding round in Java where they asked for edge case handling on trees. The HR round was straightforward.", True, 5, 3),
            ("The interview was disorganized and started 45 minutes late. Technical questions were vague, jumping from React lifecycle to complex C++ pointers without clear context. Disappointing experience.", False, 2, 4),
            ("Great company culture! Technical interview included real-world problem solving with Pandas and SQL queries on user retention. Interviewers made me feel comfortable.", True, 4, 3),
            ("Coding round was manageable with two pointer and string questions. Technical interview was deeply focused on my resume projects and AWS deployment architecture.", True, 4, 3),
            ("The technical round was extremely fast-paced. They asked about Computer Networks TCP/IP handshake, ACID properties in MySQL, and Linux commands. Got the offer!", True, 5, 4),
            ("Very tough coding assessment with strict time limits. Could only solve one question partially. Technical interview was rigid and interviewer seemed uninterested.", False, 2, 5)
        ]

        exp_count = 0
        for st in created_students[:45]:
            # Each student contributes 2-3 experiences
            num_exps = random.randint(2, 3)
            for _ in range(num_exps):
                comp = random.choice(created_companies[:18])
                role = [r for r in created_roles if r.company_id == comp.id][0]
                rev_text, is_pl, rating_val, diff_val = random.choice(sample_reviews)

                # Add some variance to text
                exp_text = f"{rev_text} Interview round tested core concepts in Python, SQL, and Data Structures."
                
                exp = PlacementExperience(
                    student_id=st.id,
                    company_id=comp.id,
                    job_role_id=role.id,
                    overall_rating=rating_val,
                    difficulty_rating=diff_val,
                    rounds_count=3,
                    questions_asked="1. Explain indexing in DBMS. 2. Invert a binary tree. 3. What are RESTful idempotency rules?",
                    skills_tested="Python, SQL, Data Structures, DBMS",
                    free_text_feedback=exp_text,
                    is_placed=is_pl,
                    status=ExperienceStatus.VERIFIED,
                    verified_by_user_id=tpo_user.id
                )
                db.add(exp)
                db.flush()
                exp_count += 1

                # Rounds
                db.add(InterviewRound(experience_id=exp.id, round_number=1, round_type=RoundType.CODING, round_title="Online Coding", duration_minutes=60, difficulty=diff_val))
                db.add(InterviewRound(experience_id=exp.id, round_number=2, round_type=RoundType.TECHNICAL_INTERVIEW, round_title="Technical Interview 1", duration_minutes=45, difficulty=diff_val))
                db.add(InterviewRound(experience_id=exp.id, round_number=3, round_type=RoundType.HR_INTERVIEW, round_title="HR & Behavioral", duration_minutes=30, difficulty=2))

                # Process ASTMA NLP Pipeline
                sent = sentiment_analyzer.analyze(exp_text, user_rating=rating_val)
                skills_ext = skill_extractor.extract_from_text(exp_text, user_tagged_skills="Python, SQL, Data Structures")
                top_ext = topic_analyzer.analyze_topics_and_difficulty(exp_text, user_difficulty=diff_val)

                nlp_res = NLPAnalysisResult(
                    experience_id=exp.id,
                    sentiment_label=sent["sentiment_label"],
                    sentiment_score=sent["sentiment_score"],
                    sentiment_confidence=sent["sentiment_confidence"],
                    inferred_difficulty=top_ext["inferred_difficulty"],
                    extracted_skills=skills_ext,
                    extracted_topics=top_ext["extracted_topics"],
                    frequently_mentioned_terms=top_ext["frequently_mentioned_terms"]
                )
                db.add(nlp_res)

        # Pre-calculate readiness evaluation for test student
        test_st_skills = [ss.skill.name for ss in test_student.skills]
        target_role_skills = ["Data Structures", "Algorithms", "SQL", "DBMS", "REST APIs", "Python", "OOP", "System Design"]
        r_eval = readiness_model.evaluate(
            cgpa=test_student.cgpa,
            student_skills=test_st_skills,
            target_role_skills=target_role_skills,
            projects_count=test_student.projects_count,
            internships_count=test_student.internships_count,
            certifications_count=test_student.certifications_count
        )
        db.add(ReadinessEvaluation(
            student_id=test_student.id,
            readiness_percentage=r_eval["readiness_percentage"],
            readiness_tier=r_eval["readiness_tier"],
            feature_breakdown=r_eval["feature_breakdown"]
        ))

        db.commit()
        print(f"Database successfully seeded! Created {len(created_companies)} companies, {len(created_students)} students, {len(created_drives)} drives, and {exp_count} verified placement experiences with NLP records.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
