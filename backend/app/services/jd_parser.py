import re
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class JobDescriptionParser:
    """Parse job descriptions and extract structured data"""

    def __init__(self):
        # Common skills patterns
        self.tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'ruby', 'php',
            'react', 'angular', 'vue', 'node.js', 'next.js', 'django', 'flask', 'fastapi', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git', 'ci/cd',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
            'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision', 'data science',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'spark', 'hadoop',
            'rest api', 'graphql', 'microservices', 'serverless', 'agile', 'scrum', 'devops',
        ]

        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
            'time management', 'project management', 'analytical', 'creative', 'adaptable',
            'collaborative', 'detail-oriented', 'organized', 'strategic', 'innovative',
        ]

    def parse(self, jd_text: str) -> Dict[str, Any]:
        """
        Parse job description and extract structured data

        Returns:
            Dict with all extracted information
        """
        try:
            return {
                'keywords': self._extract_keywords(jd_text),
                'required_skills': self._extract_required_skills(jd_text),
                'preferred_skills': self._extract_preferred_skills(jd_text),
                'experience_years': self._extract_experience_years(jd_text),
                'education_level': self._extract_education(jd_text),
                'salary_range': self._extract_salary(jd_text),
                'location': self._extract_location(jd_text),
                'remote_friendly': self._check_remote(jd_text),
                'responsibilities': self._extract_responsibilities(jd_text),
                'qualifications': self._extract_qualifications(jd_text),
                'company_info': self._extract_company_info(jd_text),
            }
        except Exception as e:
            logger.error(f"Error parsing job description: {e}")
            raise

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract all relevant keywords from JD"""
        keywords = set()
        text_lower = text.lower()

        # Extract technical skills
        for skill in self.tech_skills:
            if skill.lower() in text_lower:
                keywords.add(skill)

        # Extract soft skills
        for skill in self.soft_skills:
            if skill.lower() in text_lower:
                keywords.add(skill)

        # Extract nouns and important phrases (simplified)
        # In production, you'd use spaCy or similar for better extraction
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        keywords.update(words[:20])  # Top 20 capitalized phrases

        return sorted(list(keywords))

    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills"""
        skills = []

        # Look for "Required" or "Must have" section
        required_section = re.search(
            r'(?:required|must have|minimum qualifications?|essential)[\s:]+(.*?)(?:\n\n|preferred|nice to have|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if required_section:
            section_text = required_section.group(1).lower()

            # Extract technical skills from this section
            for skill in self.tech_skills:
                if skill.lower() in section_text:
                    skills.append(skill)

            # Extract from bullet points
            bullets = re.findall(r'[•\-\*]\s*(.+)', section_text)
            for bullet in bullets[:10]:
                bullet = bullet.strip()
                if len(bullet) < 100:  # Reasonable skill length
                    # Check if it mentions a skill
                    for skill in self.tech_skills:
                        if skill.lower() in bullet and skill not in skills:
                            skills.append(skill)
                            break

        return skills[:15]  # Top 15 required skills

    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred/nice-to-have skills"""
        skills = []

        # Look for "Preferred" or "Nice to have" section
        preferred_section = re.search(
            r'(?:preferred|nice to have|bonus|plus)[\s:]+(.*?)(?:\n\n|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if preferred_section:
            section_text = preferred_section.group(1).lower()

            # Extract technical skills
            for skill in self.tech_skills:
                if skill.lower() in section_text:
                    skills.append(skill)

        return skills[:10]  # Top 10 preferred skills

    def _extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience required"""
        # Common patterns
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

    def _extract_education(self, text: str) -> Optional[str]:
        """Extract education level required"""
        education_keywords = {
            "PhD": r'ph\.?d|doctorate',
            "Master's": r'master\'?s?|ms|mba|m\.s\.',
            "Bachelor's": r'bachelor\'?s?|bs|ba|b\.s\.|b\.a\.',
            "Associate's": r'associate\'?s?|aa|as|a\.s\.',
        }

        text_lower = text.lower()

        for degree, pattern in education_keywords.items():
            if re.search(pattern, text_lower):
                return degree

        return None

    def _extract_salary(self, text: str) -> Optional[Dict[str, int]]:
        """Extract salary range"""
        # Common salary patterns
        patterns = [
            r'\$(\d{1,3}(?:,\d{3})*)\s*[-–to]\s*\$(\d{1,3}(?:,\d{3})*)',  # $100,000 - $150,000
            r'(\d{1,3})k\s*[-–to]\s*(\d{1,3})k',  # 100k - 150k
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                min_sal = match.group(1).replace(',', '')
                max_sal = match.group(2).replace(',', '')

                # Convert k to thousands
                if 'k' in text.lower():
                    min_sal = str(int(min_sal) * 1000)
                    max_sal = str(int(max_sal) * 1000)

                return {
                    'min': int(min_sal),
                    'max': int(max_sal),
                }

        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract job location"""
        # Look for location patterns
        location_pattern = r'(?:location|based in|office in)[\s:]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:,\s*[A-Z]{2})?)'

        match = re.search(location_pattern, text)
        if match:
            return match.group(1)

        # Look for city, state patterns
        city_state = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s*([A-Z]{2})\b', text)
        if city_state:
            return f"{city_state.group(1)}, {city_state.group(2)}"

        return None

    def _check_remote(self, text: str) -> bool:
        """Check if position is remote-friendly"""
        remote_keywords = [
            'remote', 'work from home', 'wfh', 'distributed', 'anywhere',
            'home office', 'virtual', 'telecommute'
        ]

        text_lower = text.lower()
        return any(keyword in text_lower for keyword in remote_keywords)

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []

        # Look for responsibilities section
        resp_section = re.search(
            r'(?:responsibilities|duties|what you\'ll do)[\s:]+(.*?)(?:\n\n|qualifications|requirements|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if resp_section:
            section_text = resp_section.group(1)

            # Extract bullet points
            bullets = re.findall(r'[•\-\*]\s*(.+)', section_text)
            responsibilities = [b.strip() for b in bullets if len(b.strip()) > 10][:10]

        return responsibilities

    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract qualifications"""
        qualifications = []

        # Look for qualifications section
        qual_section = re.search(
            r'(?:qualifications|requirements|what we\'re looking for)[\s:]+(.*?)(?:\n\n|responsibilities|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if qual_section:
            section_text = qual_section.group(1)

            # Extract bullet points
            bullets = re.findall(r'[•\-\*]\s*(.+)', section_text)
            qualifications = [b.strip() for b in bullets if len(b.strip()) > 10][:10]

        return qualifications

    def _extract_company_info(self, text: str) -> Dict[str, Any]:
        """Extract company information"""
        info = {
            'description': None,
            'size': None,
            'industry': None,
        }

        # Look for "About" section
        about_section = re.search(
            r'(?:about us|about the company|company overview)[\s:]+(.*?)(?:\n\n|responsibilities|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if about_section:
            info['description'] = about_section.group(1).strip()[:500]

        # Look for company size
        size_match = re.search(r'(\d+\+?)\s*employees', text, re.IGNORECASE)
        if size_match:
            info['size'] = size_match.group(1)

        return info

    def extract_match_score(self, resume_text: str, jd_data: Dict[str, Any]) -> float:
        """
        Calculate how well a resume matches the job description

        Returns:
            Match score from 0-100
        """
        score = 0
        total_weight = 0

        resume_lower = resume_text.lower()

        # 1. Required skills match (40%)
        required_skills = jd_data.get('required_skills', [])
        if required_skills:
            matched = sum(1 for skill in required_skills if skill.lower() in resume_lower)
            score += (matched / len(required_skills)) * 40
            total_weight += 40

        # 2. Keywords match (30%)
        keywords = jd_data.get('keywords', [])
        if keywords:
            matched = sum(1 for kw in keywords if kw.lower() in resume_lower)
            score += (matched / len(keywords)) * 30
            total_weight += 30

        # 3. Preferred skills match (15%)
        preferred_skills = jd_data.get('preferred_skills', [])
        if preferred_skills:
            matched = sum(1 for skill in preferred_skills if skill.lower() in resume_lower)
            score += (matched / len(preferred_skills)) * 15
            total_weight += 15

        # 4. Experience match (15%)
        exp_years = jd_data.get('experience_years')
        if exp_years:
            # Try to extract years from resume (simplified)
            resume_years = re.findall(r'(\d+)\+?\s*years?', resume_lower)
            if resume_years:
                max_years = max(int(y) for y in resume_years)
                if max_years >= exp_years:
                    score += 15
                elif max_years >= exp_years * 0.7:  # 70% of required
                    score += 10
                total_weight += 15

        if total_weight == 0:
            return 0

        return min(round(score, 1), 100)
