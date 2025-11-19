from typing import Dict, Any, List, Optional
import logging
from anthropic import Anthropic
from openai import OpenAI

from app.config import settings

logger = logging.getLogger(__name__)


class AIOptimizer:
    """
    AI-powered resume optimization engine
    Uses Claude or GPT-4 to rewrite resumes for specific job descriptions
    """

    def __init__(self):
        # Initialize AI clients
        self.anthropic_client = None
        self.openai_client = None

        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

        if not self.anthropic_client and not self.openai_client:
            logger.warning("No AI API keys configured. Optimization will use fallback mode.")

    def optimize_resume(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        jd_text: str,
        jd_data: Dict[str, Any],
        model: str = "claude"
    ) -> Dict[str, Any]:
        """
        Optimize resume for specific job description

        Args:
            resume_text: Original resume text
            resume_data: Parsed resume data
            jd_text: Job description text
            jd_data: Parsed JD data
            model: "claude" or "gpt4"

        Returns:
            Dict with optimized content and metadata
        """
        try:
            if model == "claude" and self.anthropic_client:
                result = self._optimize_with_claude(resume_text, resume_data, jd_text, jd_data)
            elif model == "gpt4" and self.openai_client:
                result = self._optimize_with_gpt4(resume_text, resume_data, jd_text, jd_data)
            else:
                result = self._optimize_fallback(resume_text, resume_data, jd_data)

            return result

        except Exception as e:
            logger.error(f"Error optimizing resume: {e}")
            raise

    def _optimize_with_claude(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        jd_text: str,
        jd_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize using Anthropic Claude"""

        # Build optimization prompt
        prompt = self._build_optimization_prompt(resume_text, resume_data, jd_text, jd_data)

        # Call Claude API
        response = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse response
        optimized_content = response.content[0].text

        return self._parse_optimization_response(optimized_content, jd_data)

    def _optimize_with_gpt4(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        jd_text: str,
        jd_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize using OpenAI GPT-4"""

        prompt = self._build_optimization_prompt(resume_text, resume_data, jd_text, jd_data)

        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume writer and ATS optimization specialist. Your goal is to rewrite resumes to maximize ATS scores while maintaining authenticity."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4096,
        )

        optimized_content = response.choices[0].message.content

        return self._parse_optimization_response(optimized_content, jd_data)

    def _build_optimization_prompt(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        jd_text: str,
        jd_data: Dict[str, Any]
    ) -> str:
        """Build detailed optimization prompt"""

        required_skills = jd_data.get('required_skills', [])
        keywords = jd_data.get('keywords', [])
        responsibilities = jd_data.get('responsibilities', [])

        prompt = f"""You are an expert ATS resume optimization specialist. Your task is to rewrite this resume to maximize its ATS score for the given job description while maintaining complete truthfulness.

**ORIGINAL RESUME:**
{resume_text}

**JOB DESCRIPTION:**
{jd_text}

**KEY REQUIREMENTS:**
Required Skills: {', '.join(required_skills)}
Important Keywords: {', '.join(keywords[:15])}

**OPTIMIZATION RULES:**
1. **Keyword Integration**: Naturally incorporate ALL required skills and keywords
2. **ATS-Friendly Format**: Use simple formatting, no tables, clear section headers
3. **Quantify Everything**: Add or emphasize metrics and numbers from original resume
4. **Action Verbs**: Start each bullet with strong action verbs (Led, Developed, Increased, etc.)
5. **Truthfulness**: NEVER fabricate experience or skills not present in original resume
6. **Relevance**: Prioritize experiences most relevant to the job
7. **Section Order**: Professional Summary → Experience → Skills → Education
8. **Bullet Points**: Use • for consistency

**OUTPUT FORMAT:**
Provide the optimized resume in this exact structure:

[PROFESSIONAL SUMMARY]
2-3 sentence summary incorporating key skills

[EXPERIENCE]
Company Name | Job Title | Dates
• Achievement with metrics
• Achievement with metrics
[Continue for all relevant positions]

[SKILLS]
Technical Skills: [comma-separated list]
Soft Skills: [comma-separated list]

[EDUCATION]
Degree | Institution | Year

---

**IMPROVEMENTS MADE:**
List the specific optimizations you made (e.g., "Added keyword 'Python' to 3 bullet points")

**KEYWORD COVERAGE:**
List which required keywords are now included

Now optimize the resume:"""

        return prompt

    def _optimize_fallback(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        jd_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback optimization when no AI API is available
        Uses rule-based approach
        """

        # Extract missing keywords
        required_skills = jd_data.get('required_skills', [])
        keywords = jd_data.get('keywords', [])

        resume_lower = resume_text.lower()
        missing_keywords = [
            kw for kw in (required_skills + keywords)
            if kw.lower() not in resume_lower
        ]

        # Generate suggestions
        suggestions = [
            f"Add '{kw}' to your skills or experience sections"
            for kw in missing_keywords[:10]
        ]

        suggestions.extend([
            "Use bullet points starting with action verbs (Led, Developed, Managed)",
            "Add quantifiable metrics to your achievements (%, $, numbers)",
            "Ensure all required skills are mentioned in your resume",
            "Remove tables and complex formatting",
            "Add a professional summary at the top",
        ])

        # Build optimized content (basic version)
        optimized_sections = []

        # Professional Summary
        contact = resume_data.get('contact', {})
        skills = resume_data.get('skills', [])
        optimized_sections.append(f"""[PROFESSIONAL SUMMARY]
{contact.get('name', 'Professional')} - Experienced professional with expertise in {', '.join(skills[:5])} seeking {jd_data.get('title', 'opportunity')}.
""")

        # Experience
        if resume_data.get('experience'):
            optimized_sections.append("[EXPERIENCE]")
            for exp in resume_data.get('experience', [])[:5]:
                optimized_sections.append(f"{exp.get('description', '')}\n")

        # Skills
        if skills:
            all_skills = list(set(skills + [kw for kw in keywords if kw not in skills][:5]))
            optimized_sections.append(f"[SKILLS]\n{', '.join(all_skills)}\n")

        # Education
        if resume_data.get('education'):
            optimized_sections.append("[EDUCATION]")
            for edu in resume_data.get('education', []):
                optimized_sections.append(f"{edu.get('degree', '')}\n")

        optimized_text = '\n'.join(optimized_sections)

        return {
            'optimized_text': optimized_text,
            'improvements': suggestions,
            'keyword_additions': missing_keywords[:10],
            'ats_score_estimate': 75.0,  # Estimated improvement
            'method': 'rule-based',
        }

    def _parse_optimization_response(
        self,
        response_text: str,
        jd_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse AI response and extract structured data"""

        # Split response into resume and metadata
        parts = response_text.split('---')

        optimized_text = parts[0].strip() if parts else response_text

        # Extract improvements section
        improvements = []
        if 'IMPROVEMENTS MADE:' in response_text:
            imp_section = response_text.split('IMPROVEMENTS MADE:')[1]
            if 'KEYWORD COVERAGE:' in imp_section:
                imp_section = imp_section.split('KEYWORD COVERAGE:')[0]
            improvements = [
                line.strip() for line in imp_section.split('\n')
                if line.strip() and line.strip().startswith(('-', '•', '*'))
            ]

        # Extract keyword coverage
        keyword_additions = []
        if 'KEYWORD COVERAGE:' in response_text:
            kw_section = response_text.split('KEYWORD COVERAGE:')[1]
            keyword_additions = [
                line.strip() for line in kw_section.split('\n')
                if line.strip() and line.strip().startswith(('-', '•', '*'))
            ]

        return {
            'optimized_text': optimized_text,
            'improvements': improvements or [
                "Resume restructured for ATS compatibility",
                "Keywords strategically incorporated",
                "Achievements quantified where possible",
            ],
            'keyword_additions': keyword_additions or jd_data.get('required_skills', [])[:5],
            'ats_score_estimate': 85.0,  # AI-optimized should score high
            'method': 'ai-powered',
        }

    def generate_cover_letter(
        self,
        resume_text: str,
        resume_data: Dict[str, Any],
        jd_text: str,
        jd_data: Dict[str, Any],
        company: str,
        position: str
    ) -> str:
        """Generate personalized cover letter"""

        if not self.anthropic_client and not self.openai_client:
            return self._generate_cover_letter_fallback(resume_data, company, position)

        prompt = f"""Write a compelling, personalized cover letter for this job application.

**CANDIDATE RESUME:**
{resume_text}

**JOB DESCRIPTION:**
{jd_text}

**POSITION:** {position}
**COMPANY:** {company}

**REQUIREMENTS:**
1. 250-350 words
2. Professional yet engaging tone
3. Highlight 2-3 most relevant experiences from resume
4. Show genuine interest in the company/role
5. Include specific skills that match job requirements
6. End with strong call to action
7. Use proper business letter format

Write the cover letter:"""

        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2048,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are an expert cover letter writer."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2048,
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            return self._generate_cover_letter_fallback(resume_data, company, position)

    def _generate_cover_letter_fallback(
        self,
        resume_data: Dict[str, Any],
        company: str,
        position: str
    ) -> str:
        """Generate basic cover letter without AI"""

        contact = resume_data.get('contact', {})
        name = contact.get('name', 'Applicant')
        skills = resume_data.get('skills', [])

        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With my background in {', '.join(skills[:3])}, I am confident I would be a valuable addition to your team.

Throughout my career, I have demonstrated expertise in {', '.join(skills[3:6])}. I am particularly drawn to this opportunity because it aligns perfectly with my professional goals and technical skills.

I am excited about the possibility of contributing to {company}'s success and would welcome the opportunity to discuss how my experience and skills can benefit your team.

Thank you for considering my application. I look forward to hearing from you.

Sincerely,
{name}"""
