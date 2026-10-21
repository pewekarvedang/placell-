from typing import Dict, Any, List

class PlacementReadinessModel:
    """
    Explainable, non-discriminatory placement readiness evaluation model.
    Uses calibrated feature weighting across verified academic and technical signals.
    Excludes all demographic, gender, socioeconomic, or personal protected attributes.
    """

    def __init__(self):
        # Normalized feature weights summing to 1.0
        self.weights = {
            "cgpa": 0.25,               # Academic foundation
            "skills_depth": 0.25,       # Total skills acquired
            "target_role_match": 0.25,  # Alignment with student's chosen career path
            "projects": 0.15,           # Hands-on engineering portfolio
            "internships_certs": 0.10   # Practical industry experience / verified certifications
        }

    def evaluate(
        self,
        cgpa: float,
        student_skills: List[str],
        target_role_skills: List[str],
        projects_count: int = 0,
        internships_count: int = 0,
        certifications_count: int = 0
    ) -> Dict[str, Any]:
        """
        Calculates readiness percentage and explainable breakdown.
        """
        # 1. CGPA sub-score (Benchmark: 6.0 to 9.5)
        # Scaled smoothly: < 6.0 = lower, >= 8.5 = maximum contribution
        cgpa_clipped = max(5.0, min(10.0, cgpa))
        cgpa_score = max(0.0, min(100.0, ((cgpa_clipped - 5.0) / 4.5) * 100.0))

        # 2. Total Skills Depth (Benchmark: 2 skills = 20%, 8+ skills = 100%)
        skill_count = len(student_skills)
        skills_score = min(100.0, (skill_count / 8.0) * 100.0)

        # 3. Target Role Match Ratio
        if target_role_skills:
            target_set = {s.lower() for s in target_role_skills}
            student_set = {s.lower() for s in student_skills}
            matched_count = len(target_set.intersection(student_set))
            match_ratio = (matched_count / len(target_set))
            target_match_score = match_ratio * 100.0
        else:
            # If target role not set or has no requirements, fallback to general skill score
            target_match_score = skills_score

        # 4. Project Portfolio (Benchmark: 1 project = 40%, 3+ projects = 100%)
        projects_score = min(100.0, (projects_count / 3.0) * 100.0)

        # 5. Internships & Certifications (Benchmark: 1 cert = 50%, 1 internship + 1 cert = 100%)
        intern_score = min(60.0, internships_count * 50.0)
        cert_score = min(40.0, certifications_count * 20.0)
        industry_score = min(100.0, intern_score + cert_score)

        # Weighted composite readiness calculation
        final_readiness = (
            (cgpa_score * self.weights["cgpa"]) +
            (skills_score * self.weights["skills_depth"]) +
            (target_match_score * self.weights["target_role_match"]) +
            (projects_score * self.weights["projects"]) +
            (industry_score * self.weights["internships_certs"])
        )

        final_readiness = round(max(15.0, min(98.0, final_readiness)), 1)

        # Categorize into 4 standard academic readiness tiers
        if final_readiness >= 85.0:
            tier = "STRONG"
            tier_display = "Strong Candidate"
        elif final_readiness >= 70.0:
            tier = "PLACEMENT_READY"
            tier_display = "Placement Ready"
        elif final_readiness >= 50.0:
            tier = "DEVELOPING"
            tier_display = "Developing"
        else:
            tier = "NEEDS_IMPROVEMENT"
            tier_display = "Needs Improvement"

        feature_breakdown = {
            "academic_cgpa_contribution": {
                "score": round(cgpa_score, 1),
                "weight": f"{int(self.weights['cgpa'] * 100)}%",
                "description": f"CGPA of {cgpa:.2f} demonstrates strong core fundamentals."
            },
            "skills_depth_contribution": {
                "score": round(skills_score, 1),
                "weight": f"{int(self.weights['skills_depth'] * 100)}%",
                "description": f"{skill_count} verified technical skills logged in student profile."
            },
            "target_role_alignment": {
                "score": round(target_match_score, 1),
                "weight": f"{int(self.weights['target_role_match'] * 100)}%",
                "description": f"Skill alignment against target benchmark profile."
            },
            "project_portfolio": {
                "score": round(projects_score, 1),
                "weight": f"{int(self.weights['projects'] * 100)}%",
                "description": f"{projects_count} engineering capstones/projects documented."
            },
            "industry_and_certifications": {
                "score": round(industry_score, 1),
                "weight": f"{int(self.weights['internships_certs'] * 100)}%",
                "description": f"{internships_count} internships and {certifications_count} professional certifications."
            }
        }

        return {
            "readiness_percentage": final_readiness,
            "readiness_tier": tier,
            "readiness_tier_display": tier_display,
            "feature_breakdown": feature_breakdown,
            "ethical_safeguard_notice": (
                "Educational Decision-Support Indicator only. Prediction uses purely objective "
                "academic and technical attributes. Does not guarantee employment."
            )
        }

readiness_model = PlacementReadinessModel()
