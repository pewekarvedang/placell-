import re
from typing import List, Set, Dict

class SkillExtractor:
    """
    Extensible Skill Extraction Pipeline using multi-category skill taxonomy,
    boundary token matching, and normalization.
    """

    def __init__(self):
        # Canonical skill definitions with alternate aliases and regex patterns
        self.skill_catalog: Dict[str, List[str]] = {
            # Programming Languages
            "Python": [r"\bpython\b", r"\bpython3\b"],
            "Java": [r"\bjava\b(?!script)"],
            "C++": [r"\bc\+\+\b", r"\bcpp\b"],
            "C": [r"\bc language\b", r"\bc programming\b", r"\bansi c\b"],
            "C#": [r"\bc#\b", r"\bc-sharp\b", r"\bcsharp\b"],
            "JavaScript": [r"\bjavascript\b", r"\bjs\b", r"\bes6\b"],
            "TypeScript": [r"\btypescript\b", r"\bts\b"],
            "Go": [r"\bgolang\b", r"\bgo language\b"],
            "Rust": [r"\brust\b"],
            "Ruby": [r"\bruby\b"],
            "PHP": [r"\bphp\b"],
            "Kotlin": [r"\bkotlin\b"],
            "Swift": [r"\bswift\b"],

            # Databases & Storage
            "SQL": [r"\bsql\b", r"\bstructured query language\b"],
            "MySQL": [r"\bmysql\b"],
            "PostgreSQL": [r"\bpostgresql\b", r"\bpostgres\b"],
            "MongoDB": [r"\bmongodb\b", r"\bmongo\b"],
            "Redis": [r"\bredis\b"],
            "Oracle": [r"\boracle db\b", r"\boracle database\b"],
            "SQLite": [r"\bsqlite\b"],
            "Cassandra": [r"\bcassandra\b"],
            "DBMS": [r"\bdbms\b", r"\bdatabase management\b"],

            # Web & Frameworks
            "React": [r"\breact\b", r"\breact\.?js\b", r"\breactjs\b"],
            "Node.js": [r"\bnode\.?js\b", r"\bnode\b", r"\bnodejs\b"],
            "Express": [r"\bexpress\b", r"\bexpress\.?js\b"],
            "Angular": [r"\bangular\b", r"\bangularjs\b"],
            "Vue.js": [r"\bvue\b", r"\bvue\.?js\b"],
            "Next.js": [r"\bnext\.?js\b", r"\bnextjs\b"],
            "FastAPI": [r"\bfastapi\b"],
            "Django": [r"\bdjango\b"],
            "Flask": [r"\bflask\b"],
            "Spring Boot": [r"\bspring boot\b", r"\bspringboot\b", r"\bspring framework\b"],
            "REST APIs": [r"\brest apis?\b", r"\brestful\b", r"\bapis?\b"],
            "GraphQL": [r"\bgraphql\b"],
            "HTML/CSS": [r"\bhtml\b", r"\bcss\b", r"\btailwind\b", r"\bbootstrap\b"],

            # Core Computer Science
            "Data Structures": [r"\bdata structures?\b", r"\bdsa\b"],
            "Algorithms": [r"\balgorithms?\b", r"\bdynamic programming\b", r"\bgreedy\b"],
            "System Design": [r"\bsystem design\b", r"\bhigh level design\b", r"\blow level design\b", r"\bhld\b", r"\blld\b"],
            "Operating Systems": [r"\boperating systems?\b", r"\bos concepts\b"],
            "Computer Networks": [r"\bcomputer networks?\b", r"\bnetworking\b", r"\btcp/ip\b"],
            "OOP": [r"\boop\b", r"\boops\b", r"\bobject oriented programming\b"],

            # Cloud, DevOps & Tools
            "AWS": [r"\baws\b", r"\bamazon web services\b"],
            "Azure": [r"\bazure\b", r"\bmicrosoft azure\b"],
            "Google Cloud": [r"\bgcp\b", r"\bgoogle cloud\b"],
            "Docker": [r"\bdocker\b", r"\bcontainerization\b"],
            "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
            "Git": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b"],
            "CI/CD": [r"\bci/cd\b", r"\bpipelines?\b"],
            "Linux": [r"\blinux\b", r"\bbash\b", r"\bshell scripting\b"],

            # Data Science & Analytics
            "Machine Learning": [r"\bmachine learning\b", r"\bml\b"],
            "Deep Learning": [r"\bdeep learning\b", r"\bdl\b", r"\bneural networks\b"],
            "NLP": [r"\bnlp\b", r"\bnatural language processing\b"],
            "Pandas": [r"\bpandas\b"],
            "NumPy": [r"\bnumpy\b"],
            "Scikit-learn": [r"\bscikit-learn\b", r"\bsklearn\b"],
            "Power BI": [r"\bpower bi\b", r"\bpowerbi\b"],
            "Tableau": [r"\btableau\b"],
            "Excel": [r"\bexcel\b", r"\bms excel\b"],
            "Statistics": [r"\bstatistics\b", r"\bprobability\b"],

            # Soft Skills
            "Communication": [r"\bcommunication\b", r"\bverbal skills\b"],
            "Problem Solving": [r"\bproblem solving\b", r"\banalytical thinking\b"],
            "Leadership": [r"\bleadership\b", r"\binitiative\b"],
            "Teamwork": [r"\bteamwork\b", r"\bcollaboration\b"],
            "Critical Thinking": [r"\bcritical thinking\b"],
        }

    def extract_from_text(self, text: str, user_tagged_skills: str = "") -> List[str]:
        """
        Extracts recognized skills from text, merges with any user-tagged skills,
        and returns a sorted unique list.
        """
        extracted: Set[str] = set()

        # Parse user tagged skills if provided as comma-separated
        if user_tagged_skills:
            for tag in user_tagged_skills.split(","):
                tag_clean = tag.strip()
                if tag_clean:
                    # Match canonical name if present
                    canonical = self.get_canonical_name(tag_clean)
                    extracted.add(canonical if canonical else tag_clean)

        if not text:
            return sorted(list(extracted))

        text_lower = text.lower()

        for canonical_name, patterns in self.skill_catalog.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    extracted.add(canonical_name)
                    break

        return sorted(list(extracted))

    def get_canonical_name(self, query: str) -> str:
        """Find canonical skill name for query if exists."""
        q_lower = query.lower().strip()
        for canonical, patterns in self.skill_catalog.items():
            if q_lower == canonical.lower():
                return canonical
            for pattern in patterns:
                if re.search(pattern, q_lower, re.IGNORECASE):
                    return canonical
        return query.strip()

skill_extractor = SkillExtractor()
