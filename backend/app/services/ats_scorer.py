import re
from typing import Dict, Any, List, Set
import logging

logger = logging.getLogger(__name__)


class ATSScorer:
    """
    Analyze resumes and calculate ATS (Applicant Tracking System) scores.
    This is a comprehensive scoring system based on real ATS requirements.
    """

    def __init__(self):
        # Scoring weights
        self.weights = {
            'keyword_match': 0.30,  # 30% - Keyword matching
            'formatting': 0.15,     # 15% - Clean formatting
            'completeness': 0.20,   # 20% - Required sections present
            'experience': 0.15,     # 15% - Quantifiable achievements
            'skills': 0.10,         # 10% - Technical skills presence
            'readability': 0.10,    # 10% - Text clarity and structure
        }

    def calculate_score(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        job_keywords: List[str] = None,
        job_required_skills: List[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive ATS score

        Returns:
            Dict with score, feedback, and recommendations
        """
        try:
            # Initialize scores
            scores = {}

            # 1. Keyword Match Score (if JD provided)
            if job_keywords:
                scores['keyword_match'] = self._score_keyword_match(
                    resume_text, job_keywords, job_required_skills or []
                )
            else:
                scores['keyword_match'] = 70.0  # Default neutral score

            # 2. Formatting Score
            scores['formatting'] = self._score_formatting(resume_text)

            # 3. Completeness Score
            scores['completeness'] = self._score_completeness(resume_data)

            # 4. Experience Score
            scores['experience'] = self._score_experience(resume_text, resume_data)

            # 5. Skills Score
            scores['skills'] = self._score_skills(resume_data)

            # 6. Readability Score
            scores['readability'] = self._score_readability(resume_text)

            # Calculate weighted total score
            total_score = sum(
                scores[category] * self.weights[category]
                for category in scores
            )

            # Generate feedback
            feedback = self._generate_feedback(scores, resume_data, job_keywords)

            return {
                'score': round(total_score, 1),
                'category_scores': {k: round(v, 1) for k, v in scores.items()},
                'feedback': feedback,
                'missing_keywords': feedback.get('missing_keywords', []),
                'suggestions': feedback.get('suggestions', []),
                'strengths': feedback.get('strengths', []),
                'weaknesses': feedback.get('weaknesses', []),
            }

        except Exception as e:
            logger.error(f"Error calculating ATS score: {e}")
            raise

    def _score_keyword_match(
        self,
        resume_text: str,
        job_keywords: List[str],
        required_skills: List[str]
    ) -> float:
        """Score based on keyword matching"""
        if not job_keywords:
            return 70.0

        resume_lower = resume_text.lower()
        keywords_lower = [kw.lower() for kw in job_keywords]
        required_lower = [skill.lower() for skill in required_skills]

        # Count matched keywords
        matched_keywords = sum(1 for kw in keywords_lower if kw in resume_lower)
        keyword_match_rate = matched_keywords / len(keywords_lower) if keywords_lower else 0

        # Count matched required skills (weighted more heavily)
        matched_required = sum(1 for skill in required_lower if skill in resume_lower)
        required_match_rate = matched_required / len(required_lower) if required_lower else 0

        # Combined score (required skills weighted 60%, general keywords 40%)
        combined_score = (required_match_rate * 0.6 + keyword_match_rate * 0.4) * 100

        return min(combined_score, 100)

    def _score_formatting(self, resume_text: str) -> float:
        """Score formatting quality"""
        score = 100.0

        # Check for problematic formatting
        issues = []

        # 1. Too many special characters
        special_chars = len(re.findall(r'[^a-zA-Z0-9\s\.,\-\(\)\[\]\/]', resume_text))
        if special_chars > len(resume_text) * 0.05:  # More than 5% special chars
            score -= 15
            issues.append("Too many special characters - may confuse ATS")

        # 2. Check for tables (ATS often can't parse them well)
        if '\t' in resume_text:
            score -= 10
            issues.append("Contains tabs - use spaces instead")

        # 3. Check for headers/footers patterns
        if re.search(r'Page \d+ of \d+', resume_text):
            score -= 5
            issues.append("Page numbers detected - remove headers/footers")

        # 4. Check for graphics/charts indicators
        if '[image]' in resume_text.lower() or '[chart]' in resume_text.lower():
            score -= 10
            issues.append("Contains images/charts - ATS cannot read these")

        # 5. Check for consistent bullet points
        bullet_types = len(set(re.findall(r'^[•\-\*\+]', resume_text, re.MULTILINE)))
        if bullet_types > 2:
            score -= 5
            issues.append("Inconsistent bullet points - use one style")

        # 6. Check for proper spacing
        if '\n\n\n' in resume_text:  # Too much spacing
            score -= 5
            issues.append("Excessive spacing detected")

        return max(score, 0)

    def _score_completeness(self, resume_data: Dict[str, Any]) -> float:
        """Score based on required sections"""
        score = 0
        required_sections = {
            'contact': 20,
            'experience': 30,
            'education': 20,
            'skills': 20,
            'summary': 10,
        }

        for section, points in required_sections.items():
            if section in resume_data and resume_data[section]:
                # Check if section has meaningful data
                if section == 'contact':
                    if resume_data[section].get('email'):
                        score += points
                elif section == 'skills' or section == 'experience':
                    if len(resume_data[section]) > 0:
                        score += points
                elif section == 'education':
                    if len(resume_data[section]) > 0:
                        score += points
                elif section == 'summary':
                    if resume_data[section] and len(resume_data[section]) > 50:
                        score += points

        return min(score, 100)

    def _score_experience(self, resume_text: str, resume_data: Dict[str, Any]) -> float:
        """Score experience section quality"""
        score = 70.0  # Base score

        # 1. Check for quantifiable achievements (numbers, percentages, metrics)
        numbers = re.findall(r'\b\d+[%\+]?\b', resume_text)
        if len(numbers) > 5:
            score += 20
        elif len(numbers) > 2:
            score += 10

        # 2. Check for action verbs
        action_verbs = [
            'led', 'managed', 'developed', 'created', 'increased', 'decreased',
            'improved', 'designed', 'implemented', 'achieved', 'delivered',
            'launched', 'built', 'optimized', 'reduced', 'generated', 'drove'
        ]
        resume_lower = resume_text.lower()
        action_verb_count = sum(1 for verb in action_verbs if verb in resume_lower)
        if action_verb_count > 5:
            score += 10

        # 3. Check experience length
        experience_entries = resume_data.get('experience', [])
        if len(experience_entries) >= 2:
            score += 10
        elif len(experience_entries) >= 1:
            score += 5

        return min(score, 100)

    def _score_skills(self, resume_data: Dict[str, Any]) -> float:
        """Score skills section"""
        skills = resume_data.get('skills', [])

        if not skills:
            return 0

        # More skills generally better (up to a point)
        skill_count = len(skills)

        if skill_count >= 15:
            return 100
        elif skill_count >= 10:
            return 85
        elif skill_count >= 7:
            return 70
        elif skill_count >= 5:
            return 60
        elif skill_count >= 3:
            return 40
        else:
            return 20

    def _score_readability(self, resume_text: str) -> float:
        """Score text readability"""
        score = 100.0

        # 1. Check average sentence length
        sentences = re.split(r'[.!?]+', resume_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if sentences:
            avg_words_per_sentence = sum(len(s.split()) for s in sentences) / len(sentences)

            # Ideal: 15-20 words per sentence
            if avg_words_per_sentence > 30:
                score -= 15
            elif avg_words_per_sentence < 10:
                score -= 10

        # 2. Check for overly long paragraphs
        paragraphs = resume_text.split('\n\n')
        long_paragraphs = sum(1 for p in paragraphs if len(p.split()) > 100)
        if long_paragraphs > 3:
            score -= 10

        # 3. Check for jargon overload
        jargon_words = [
            'synergy', 'leverage', 'paradigm', 'disruptive', 'innovative',
            'rockstar', 'ninja', 'guru', 'thought leader'
        ]
        resume_lower = resume_text.lower()
        jargon_count = sum(1 for word in jargon_words if word in resume_lower)
        if jargon_count > 3:
            score -= 15

        return max(score, 0)

    def _generate_feedback(
        self,
        scores: Dict[str, float],
        resume_data: Dict[str, Any],
        job_keywords: List[str] = None
    ) -> Dict[str, Any]:
        """Generate detailed feedback and recommendations"""
        feedback = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': [],
            'missing_keywords': [],
        }

        # Analyze each category
        for category, score in scores.items():
            if score >= 80:
                feedback['strengths'].append(self._get_strength_message(category))
            elif score < 60:
                feedback['weaknesses'].append(self._get_weakness_message(category))
                feedback['suggestions'].extend(self._get_suggestions(category, resume_data))

        # Missing keywords
        if job_keywords:
            resume_text_lower = str(resume_data).lower()
            missing = [kw for kw in job_keywords if kw.lower() not in resume_text_lower]
            feedback['missing_keywords'] = missing[:10]  # Top 10 missing

            if missing:
                feedback['suggestions'].append(
                    f"Add these missing keywords: {', '.join(missing[:5])}"
                )

        return feedback

    def _get_strength_message(self, category: str) -> str:
        """Get strength message for category"""
        messages = {
            'keyword_match': "Excellent keyword match with job requirements",
            'formatting': "Clean, ATS-friendly formatting",
            'completeness': "All required sections present",
            'experience': "Strong experience descriptions with quantifiable results",
            'skills': "Comprehensive skills section",
            'readability': "Clear and concise writing",
        }
        return messages.get(category, f"Strong {category}")

    def _get_weakness_message(self, category: str) -> str:
        """Get weakness message for category"""
        messages = {
            'keyword_match': "Low keyword match with job requirements",
            'formatting': "Formatting issues that may confuse ATS",
            'completeness': "Missing required sections",
            'experience': "Experience section lacks impact and metrics",
            'skills': "Limited skills listed",
            'readability': "Text is difficult to parse",
        }
        return messages.get(category, f"Weak {category}")

    def _get_suggestions(self, category: str, resume_data: Dict[str, Any]) -> List[str]:
        """Get specific suggestions for improvement"""
        suggestions = []

        if category == 'keyword_match':
            suggestions.append("Add more job-specific keywords throughout your resume")
            suggestions.append("Mirror the language used in the job description")

        elif category == 'formatting':
            suggestions.append("Use standard fonts (Arial, Calibri, Times New Roman)")
            suggestions.append("Remove tables, text boxes, and headers/footers")
            suggestions.append("Use simple bullet points (•, -, or *)")

        elif category == 'completeness':
            if not resume_data.get('contact', {}).get('email'):
                suggestions.append("Add your email address")
            if not resume_data.get('summary'):
                suggestions.append("Add a professional summary at the top")
            if not resume_data.get('skills'):
                suggestions.append("Add a dedicated skills section")

        elif category == 'experience':
            suggestions.append("Add quantifiable metrics (numbers, percentages, results)")
            suggestions.append("Start bullet points with strong action verbs")
            suggestions.append("Focus on achievements, not just responsibilities")

        elif category == 'skills':
            suggestions.append("Add more relevant technical and soft skills")
            suggestions.append("Include both hard and soft skills")

        elif category == 'readability':
            suggestions.append("Break up long paragraphs")
            suggestions.append("Use shorter, clearer sentences")
            suggestions.append("Reduce buzzwords and jargon")

        return suggestions
