import re
from typing import Dict, Any

class SentimentAnalyzer:
    """
    Interpretable, calibrated sentiment analysis engine for student placement reviews.
    Combines normalized placement sentiment lexicon with weighted TF-IDF style polarity scoring.
    """

    def __init__(self):
        # Domain-specific positive placement vocabulary with weights
        self.positive_lexicon: Dict[str, float] = {
            "smooth": 1.5, "friendly": 1.4, "supportive": 1.5, "encouraging": 1.4,
            "clear": 1.2, "interactive": 1.3, "welcoming": 1.4, "fair": 1.3,
            "helpful": 1.4, "positive": 1.5, "great": 1.4, "excellent": 1.6,
            "good": 1.1, "easy": 1.0, "moderate": 0.5, "structured": 1.2,
            "selected": 1.8, "offer": 1.8, "enjoyable": 1.4, "polite": 1.2,
            "well organized": 1.5, "professional": 1.3, "comfortable": 1.3,
            "constructive": 1.4, "approachable": 1.3, "satisfied": 1.4
        }

        # Domain-specific negative placement vocabulary with weights
        self.negative_lexicon: Dict[str, float] = {
            "harsh": 1.6, "rude": 1.8, "unprepared": 1.6, "disorganized": 1.7,
            "delayed": 1.3, "confusing": 1.4, "unfair": 1.7, "stressful": 1.4,
            "difficult": 1.1, "hard": 1.0, "tough": 0.9, "bad": 1.4,
            "terrible": 1.8, "poor": 1.5, "unhelpful": 1.5, "rigid": 1.2,
            "interrupted": 1.3, "disappointed": 1.5, "rejected": 1.4, "intimidating": 1.5,
            "chaotic": 1.7, "frustrating": 1.6, "unreasonable": 1.6, "rushed": 1.3
        }

        self.negation_words = {"not", "never", "no", "hardly", "barely", "scarcely", "neither"}
        self.intensifiers = {"very": 1.5, "extremely": 1.8, "highly": 1.6, "really": 1.4, "quite": 1.2}

    def analyze(self, text: str, user_rating: int = 3) -> Dict[str, Any]:
        """
        Analyzes free-text student feedback and returns:
        - sentiment_label: 'POSITIVE', 'NEUTRAL', or 'NEGATIVE'
        - sentiment_score: calibrated float from 0.0 to 1.0 (0.0 = very negative, 1.0 = very positive)
        - sentiment_confidence: float from 0.50 to 1.00
        """
        if not text or not text.strip():
            # If no free-text, calibrate purely based on 1-5 user rating
            normalized_rating = (user_rating - 1.0) / 4.0
            label = "POSITIVE" if normalized_rating >= 0.6 else ("NEGATIVE" if normalized_rating <= 0.4 else "NEUTRAL")
            return {
                "sentiment_label": label,
                "sentiment_score": round(normalized_rating, 2),
                "sentiment_confidence": 0.75
            }

        cleaned = text.lower()
        words = re.findall(r"\b[a-z']+\b", cleaned)
        
        pos_score = 0.0
        neg_score = 0.0
        
        for i, word in enumerate(words):
            # Check negation in previous 2 words
            is_negated = False
            if i > 0 and words[i - 1] in self.negation_words:
                is_negated = True
            elif i > 1 and words[i - 2] in self.negation_words:
                is_negated = True

            multiplier = 1.0
            if i > 0 and words[i - 1] in self.intensifiers:
                multiplier = self.intensifiers[words[i - 1]]

            if word in self.positive_lexicon:
                weight = self.positive_lexicon[word] * multiplier
                if is_negated:
                    neg_score += weight * 0.8
                else:
                    pos_score += weight

            if word in self.negative_lexicon:
                weight = self.negative_lexicon[word] * multiplier
                if is_negated:
                    pos_score += weight * 0.8
                else:
                    neg_score += weight

        # Combine text score with normalized user overall rating (prior weight)
        rating_score = (user_rating - 1.0) / 4.0 # Scale [1,5] -> [0.0, 1.0]

        total_lex_score = pos_score + neg_score
        if total_lex_score > 0:
            text_polarity = (pos_score - neg_score) / total_lex_score # [-1.0, 1.0]
            normalized_text_score = (text_polarity + 1.0) / 2.0      # [0.0, 1.0]
            # Blend: 60% text evidence + 40% explicit numerical user rating
            final_score = (0.60 * normalized_text_score) + (0.40 * rating_score)
            confidence = min(0.98, 0.70 + (total_lex_score * 0.05))
        else:
            final_score = rating_score
            confidence = 0.70

        final_score = max(0.0, min(1.0, final_score))

        if final_score >= 0.60:
            label = "POSITIVE"
        elif final_score <= 0.40:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        return {
            "sentiment_label": label,
            "sentiment_score": round(final_score, 3),
            "sentiment_confidence": round(confidence, 3)
        }

sentiment_analyzer = SentimentAnalyzer()
