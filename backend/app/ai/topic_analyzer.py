import re
from typing import List, Dict, Any

class TopicAnalyzer:
    """
    Extracts core interview topics and infers question difficulty indicators
    from unstructured placement reviews.
    """

    def __init__(self):
        self.topic_catalog: Dict[str, List[str]] = {
            "Arrays & Strings": [r"\barray\b", r"\bstring manipulation\b", r"\bsliding window\b", r"\btwo pointer\b"],
            "Trees & Graphs": [r"\btrees?\b", r"\bbinary tree\b", r"\bbst\b", r"\bgraphs?\b", r"\bbfs\b", r"\bdfs\b", r"\btrie\b"],
            "Dynamic Programming": [r"\bdp\b", r"\bdynamic programming\b", r"\bmemoization\b", r"\bknapsack\b"],
            "SQL & Queries": [r"\bsql queries\b", r"\bjoins\b", r"\bindexing\b", r"\bnormalization\b", r"\btriggers\b"],
            "System Architecture": [r"\bsystem design\b", r"\bmicroservices\b", r"\bcaching\b", r"\bload balancer\b", r"\bscalability\b"],
            "Core CS Fundamentals": [r"\bdeadlock\b", r"\bthreading\b", r"\bvirtual memory\b", r"\bos\b", r"\bpolymorphism\b", r"\binheritance\b"],
            "REST & Web APIs": [r"\brest apis?\b", r"\bhttp methods\b", r"\bauthentication\b", r"\bjwt\b", r"\bstatus codes\b"],
            "Project & Resume Grilling": [r"\bprojects?\b", r"\bresume\b", r"\barchitecture explanation\b", r"\bdeep dive\b"],
            "Behavioral & Situational": [r"\bhr round\b", r"\bscenario based\b", r"\bconflict\b", r"\bstrengths\b", r"\bweaknesses\b"],
            "Aptitude & Puzzles": [r"\baptitude\b", r"\bpuzzles?\b", r"\bquantitative\b", r"\blogical reasoning\b"]
        }

        self.difficulty_markers = {
            "HARD": [r"\bhard\b", r"\bvery difficult\b", r"\bcomplex\b", r"\bexhausting\b", r"\btricky\b", r"\brigorous\b", r"\bdeep\b", r"\bintense\b"],
            "EASY": [r"\beasy\b", r"\bsimple\b", r"\bstraightforward\b", r"\bbasic\b", r"\belementary\b", r"\bsmooth\b", r"\bstandard\b"],
            "MODERATE": [r"\bmoderate\b", r"\baverage\b", r"\bbalanced\b", r"\bmanageable\b", r"\bmedium\b"]
        }

    def analyze_topics_and_difficulty(self, text: str, user_difficulty: int = 3) -> Dict[str, Any]:
        """
        Extracts topics, frequent terms, and determines inferred difficulty.
        """
        extracted_topics: List[str] = []
        text_lower = text.lower() if text else ""

        for topic, patterns in self.topic_catalog.items():
            for pat in patterns:
                if re.search(pat, text_lower, re.IGNORECASE):
                    extracted_topics.append(topic)
                    break

        if not extracted_topics:
            extracted_topics = ["Technical Assessment", "General Interview"]

        # Inferred difficulty analysis
        hard_count = sum(1 for pat in self.difficulty_markers["HARD"] if re.search(pat, text_lower))
        easy_count = sum(1 for pat in self.difficulty_markers["EASY"] if re.search(pat, text_lower))

        if user_difficulty >= 4 or hard_count > easy_count:
            inferred = "HARD"
        elif user_difficulty <= 2 or easy_count > hard_count:
            inferred = "EASY"
        else:
            inferred = "MODERATE"

        # Extract top frequent terms (stopwords filtered)
        stopwords = {
            "the", "and", "was", "were", "they", "asked", "about", "for", "with", "this",
            "that", "from", "interview", "round", "questions", "questions asked", "then",
            "very", "have", "had", "will", "would", "could", "should", "some", "more"
        }
        words = re.findall(r"\b[a-z]{3,}\b", text_lower)
        filtered = [w for w in words if w not in stopwords]
        
        counts: Dict[str, int] = {}
        for w in filtered:
            counts[w] = counts.get(w, 0) + 1
        
        top_terms = [item[0] for item in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:6]]

        return {
            "extracted_topics": extracted_topics,
            "inferred_difficulty": inferred,
            "frequently_mentioned_terms": top_terms
        }

topic_analyzer = TopicAnalyzer()
