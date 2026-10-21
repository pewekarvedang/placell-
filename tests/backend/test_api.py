import time
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "enterprise_systems" in data["modules"]
    assert "ai_nlp_pipeline" in data["modules"]

def test_student_login_and_profile():
    # Login as student
    response = client.post("/api/v1/auth/login", json={
        "email": "student@college.edu",
        "password": "Pass@123"
    })
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch profile
    profile_res = client.get("/api/v1/students/me", headers=headers)
    assert profile_res.status_code == 200
    pdata = profile_res.json()
    assert pdata["roll_number"] == "22CSBS001"
    assert len(pdata["skills"]) > 0

    # Fetch Readiness Score (ASTMA ML)
    readiness_res = client.get("/api/v1/students/me/readiness", headers=headers)
    assert readiness_res.status_code == 200
    rdata = readiness_res.json()
    assert "readiness_percentage" in rdata
    assert "feature_breakdown" in rdata

    # Fetch Skill Gap (ASTMA Explainable Engine)
    gap_res = client.get("/api/v1/students/me/skill-gap", headers=headers)
    assert gap_res.status_code == 200
    gdata = gap_res.json()
    assert "matched_skills" in gdata
    assert "recommendations" in gdata

def test_student_add_and_remove_skill():
    # Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "student@college.edu",
        "password": "Pass@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get all catalog skills
    skills_res = client.get("/api/v1/admin/skills")
    assert skills_res.status_code == 200
    all_skills = skills_res.json()
    test_skill = all_skills[0]

    # Add skill
    add_res = client.post("/api/v1/students/me/skills", json={
        "skill_id": test_skill["id"],
        "proficiency_level": "Advanced"
    }, headers=headers)
    assert add_res.status_code == 200

    # Remove skill
    del_res = client.delete(f"/api/v1/students/me/skills/{test_skill['id']}", headers=headers)
    assert del_res.status_code == 200

def test_analytics_overview():
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    adata = response.json()
    assert adata["kpis"]["total_companies"] > 0
    assert adata["kpis"]["total_experiences"] > 0
    assert "sentiment_distribution" in adata
    assert len(adata["top_demanded_skills"]) > 0
    assert len(adata["department_metrics"]) > 0

def test_experience_submission_and_nlp():
    # Login as student
    login_res = client.post("/api/v1/auth/login", json={
        "email": "student@college.edu",
        "password": "Pass@123"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get companies to link one
    companies_res = client.get("/api/v1/companies")
    company_id = companies_res.json()[0]["id"]

    # Submit experience
    exp_payload = {
        "company_id": company_id,
        "overall_rating": 5,
        "difficulty_rating": 4,
        "rounds_count": 3,
        "questions_asked": "Explain B-Trees and write SQL queries with window functions.",
        "skills_tested": "SQL, Python, Algorithms",
        "free_text_feedback": "Fantastic interview! The technical panel focused heavily on PostgreSQL queries and Python REST APIs. Coding was challenging but encouraging.",
        "is_placed": True,
        "rounds": [
            {"round_number": 1, "round_type": "CODING", "round_title": "DSA Round", "difficulty": 4},
            {"round_number": 2, "round_type": "TECHNICAL_INTERVIEW", "round_title": "Architecture Round", "difficulty": 4}
        ]
    }
    exp_res = client.post("/api/v1/experiences", json=exp_payload, headers=headers)
    assert exp_res.status_code == 200
    edata = exp_res.json()
    assert edata["nlp_result"] is not None
    assert edata["nlp_result"]["sentiment_label"] in ["POSITIVE", "NEUTRAL"]
    assert "SQL" in edata["nlp_result"]["extracted_skills"] or "Python" in edata["nlp_result"]["extracted_skills"]

def test_tpo_moderation_queue():
    # Login as TPO
    tpo_login = client.post("/api/v1/auth/login", json={
        "email": "tpo@college.edu",
        "password": "Pass@123"
    })
    assert tpo_login.status_code == 200
    tpo_token = tpo_login.json()["access_token"]
    tpo_headers = {"Authorization": f"Bearer {tpo_token}"}

    # View pending moderation
    pending_res = client.get("/api/v1/experiences/pending", headers=tpo_headers)
    assert pending_res.status_code == 200
    pending_list = pending_res.json()

    if len(pending_list) > 0:
        exp_id = pending_list[0]["id"]
        # Approve experience
        verify_res = client.patch(f"/api/v1/experiences/{exp_id}/verify", json={
            "status": "VERIFIED",
            "moderation_notes": "Approved by TPO test suite"
        }, headers=tpo_headers)
        assert verify_res.status_code == 200
        assert verify_res.json()["status"] == "VERIFIED"

def test_company_and_drive_management():
    # Login as TPO
    tpo_login = client.post("/api/v1/auth/login", json={
        "email": "tpo@college.edu",
        "password": "Pass@123"
    })
    tpo_token = tpo_login.json()["access_token"]
    tpo_headers = {"Authorization": f"Bearer {tpo_token}"}

    # 1. Create a Company
    comp_name = f"Acme AI {int(time.time() * 1000)}"
    comp_res = client.post("/api/v1/companies", json={
        "name": comp_name,
        "industry": "Artificial Intelligence",
        "company_type": "Product",
        "ctc_min_lpa": 12.0,
        "ctc_max_lpa": 24.0,
        "location": "Bengaluru",
        "description": "Autonomous AI infrastructure"
    }, headers=tpo_headers)
    assert comp_res.status_code == 200
    company = comp_res.json()
    assert company["name"] == comp_name

    # 2. Add Job Role to Company
    role_res = client.post("/api/v1/companies/roles", json={
        "company_id": company["id"],
        "title": "AI Engineer (L1)",
        "min_cgpa": 7.5,
        "description": "Core AI model development",
        "required_skill_ids": []
    }, headers=tpo_headers)
    assert role_res.status_code == 200
    job_role = role_res.json()

    # 3. Schedule Drive
    drive_res = client.post("/api/v1/drives", json={
        "company_id": company["id"],
        "job_role_id": job_role["id"],
        "title": "Acme AI 2026 Campus Drive",
        "drive_date": "2026-11-15",
        "status": "UPCOMING",
        "eligibility_cgpa": 7.0,
        "ctc_offered_lpa": 15.0,
        "rounds_description": "Coding Assessment, ML System Design, HR"
    }, headers=tpo_headers)
    assert drive_res.status_code == 200
    drive = drive_res.json()
    assert drive["title"] == "Acme AI 2026 Campus Drive"

    # 4. Student applies to drive
    student_login = client.post("/api/v1/auth/login", json={
        "email": "student@college.edu",
        "password": "Pass@123"
    })
    student_token = student_login.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    apply_res = client.post(f"/api/v1/drives/{drive['id']}/apply", headers=student_headers)
    assert apply_res.status_code == 200
    application = apply_res.json()
    assert application["status"] == "APPLIED"

    # 5. TPO checks applicants and updates status
    apps_res = client.get(f"/api/v1/drives/{drive['id']}/applications", headers=tpo_headers)
    assert apps_res.status_code == 200
    assert len(apps_res.json()) >= 1

    status_update = client.patch(f"/api/v1/drives/applications/{application['id']}/status", json={
        "status": "SHORTLISTED"
    }, headers=tpo_headers)
    assert status_update.status_code == 200
    assert status_update.json()["status"] == "SHORTLISTED"

def test_admin_governance():
    # Login as Admin
    admin_login = client.post("/api/v1/auth/login", json={
        "email": "admin@college.edu",
        "password": "Pass@123"
    })
    assert admin_login.status_code == 200
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Get users
    users_res = client.get("/api/v1/admin/users", headers=admin_headers)
    assert users_res.status_code == 200
    assert len(users_res.json()) > 0

    # Get departments
    depts_res = client.get("/api/v1/admin/departments", headers=admin_headers)
    assert depts_res.status_code == 200
    dept_codes = [d["code"] for d in depts_res.json()]
    assert "CSE" in dept_codes
    assert "CSBS" in dept_codes
    assert "AIML" in dept_codes
    assert "IT" in dept_codes

    # Get audit logs
    audit_res = client.get("/api/v1/admin/audit-logs", headers=admin_headers)
    assert audit_res.status_code == 200
    assert len(audit_res.json()) > 0
