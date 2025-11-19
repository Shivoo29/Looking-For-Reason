import PyPDF2
import docx
import pdfplumber
import re
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ResumeParser:
    """Parse resumes and extract structured data"""

    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        self.github_pattern = r'github\.com/[\w-]+'

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse resume file and extract data"""
        try:
            # Extract text based on file type
            if file_path.endswith('.pdf'):
                raw_text = self._extract_pdf_text(file_path)
            elif file_path.endswith('.docx'):
                raw_text = self._extract_docx_text(file_path)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_text = f.read()
            else:
                raise ValueError(f"Unsupported file format: {file_path}")

            # Extract structured data
            parsed_data = self._extract_structured_data(raw_text)

            return {
                'raw_text': raw_text,
                'parsed_data': parsed_data,
            }

        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            raise

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            logger.warning(f"pdfplumber failed, trying PyPDF2: {e}")
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""

        return text.strip()

    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()

    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extract structured data from raw text"""
        return {
            'contact': self._extract_contact_info(text),
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience': self._extract_experience(text),
            'certifications': self._extract_certifications(text),
            'summary': self._extract_summary(text),
        }

    def _extract_contact_info(self, text: str) -> Dict[str, Optional[str]]:
        """Extract contact information"""
        # Extract email
        email_match = re.search(self.email_pattern, text)
        email = email_match.group(0) if email_match else None

        # Extract phone
        phone_match = re.search(self.phone_pattern, text)
        phone = phone_match.group(0) if phone_match else None

        # Extract LinkedIn
        linkedin_match = re.search(self.linkedin_pattern, text)
        linkedin = linkedin_match.group(0) if linkedin_match else None

        # Extract GitHub
        github_match = re.search(self.github_pattern, text)
        github = github_match.group(0) if github_match else None

        # Extract name (usually first line)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = lines[0] if lines else None

        return {
            'name': name,
            'email': email,
            'phone': phone,
            'linkedin': linkedin,
            'github': github,
        }

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume"""
        # Common skill keywords
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'node', 'sql', 'nosql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'agile', 'scrum',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'data science',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'html', 'css', 'rest api', 'graphql', 'microservices', 'ci/cd',
            'leadership', 'communication', 'project management', 'problem solving',
            'fastapi', 'django', 'flask', 'express', 'next.js', 'vue', 'angular',
            'postgresql', 'mongodb', 'redis', 'elasticsearch',
        ]

        text_lower = text.lower()
        found_skills = []

        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())

        # Look for skills section
        skills_section_match = re.search(
            r'(?:skills?|technical skills?|core competencies)[\s:]+(.+?)(?:\n\n|\n[A-Z])',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if skills_section_match:
            skills_text = skills_section_match.group(1)
            # Extract comma-separated or bullet-pointed skills
            skill_items = re.split(r'[,•\n]', skills_text)
            for item in skill_items:
                item = item.strip()
                if item and len(item) < 50:  # Reasonable skill length
                    if item not in found_skills:
                        found_skills.append(item)

        return list(set(found_skills))[:30]  # Limit to 30 skills

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []

        # Common degree keywords
        degree_keywords = [
            r'bachelor', r'master', r'phd', r'doctorate', r'associate',
            r'b\.s\.', r'm\.s\.', r'b\.a\.', r'm\.a\.', r'mba',
        ]

        degree_pattern = '|'.join(degree_keywords)

        # Find education section
        education_section = re.search(
            r'(?:education|academic background)[\s:]+(.+?)(?:\n\n|\n[A-Z]{3,})',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if education_section:
            edu_text = education_section.group(1)
            lines = edu_text.split('\n')

            for line in lines:
                if re.search(degree_pattern, line, re.IGNORECASE):
                    education.append({
                        'degree': line.strip(),
                        'institution': '',  # Could be enhanced with NER
                        'year': self._extract_year(line),
                    })

        return education[:5]  # Limit to 5 entries

    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience"""
        experience = []

        # Find experience section
        exp_section = re.search(
            r'(?:experience|work history|employment)[\s:]+(.+?)(?:\n\n|\n[A-Z]{3,}|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if exp_section:
            exp_text = exp_section.group(1)

            # Split by common job title patterns or dates
            # This is a simplified version
            paragraphs = exp_text.split('\n\n')

            for para in paragraphs[:10]:  # Limit to 10 entries
                if len(para.strip()) > 20:
                    experience.append({
                        'description': para.strip()[:500],  # Limit length
                        'company': '',  # Could be enhanced with NER
                        'duration': self._extract_duration(para),
                    })

        return experience

    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []

        # Find certifications section
        cert_section = re.search(
            r'(?:certifications?|licenses?)[\s:]+(.+?)(?:\n\n|\n[A-Z]{3,})',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if cert_section:
            cert_text = cert_section.group(1)
            lines = [line.strip() for line in cert_text.split('\n') if line.strip()]
            certifications = lines[:10]  # Limit to 10

        return certifications

    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract professional summary"""
        # Find summary section
        summary_section = re.search(
            r'(?:summary|profile|objective|about)[\s:]+(.+?)(?:\n\n|\n[A-Z]{3,})',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if summary_section:
            summary = summary_section.group(1).strip()
            return summary[:500]  # Limit length

        return None

    def _extract_year(self, text: str) -> Optional[str]:
        """Extract year from text"""
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        return year_match.group(0) if year_match else None

    def _extract_duration(self, text: str) -> Optional[str]:
        """Extract duration/date range from text"""
        # Look for patterns like "2020 - 2023" or "Jan 2020 - Present"
        duration_match = re.search(
            r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}).*?(?:to|[-–—]|present).*?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4}|present))',
            text,
            re.IGNORECASE
        )
        return duration_match.group(1).strip() if duration_match else None
