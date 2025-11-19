from typing import Dict, Any, Optional
import logging
from anthropic import Anthropic
from openai import OpenAI

from app.config import settings

logger = logging.getLogger(__name__)


class OutreachGenerator:
    """Generate personalized outreach messages for LinkedIn and email"""

    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None

        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_email(
        self,
        contact_name: str,
        contact_title: str,
        company: str,
        position: str,
        resume_summary: str,
        job_keywords: list[str],
        contact_info: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """
        Generate personalized email outreach

        Returns:
            Dict with 'subject' and 'body'
        """

        if self.anthropic_client or self.openai_client:
            return self._generate_email_ai(
                contact_name, contact_title, company, position,
                resume_summary, job_keywords, contact_info
            )
        else:
            return self._generate_email_template(
                contact_name, contact_title, company, position,
                resume_summary, job_keywords
            )

    def generate_linkedin_message(
        self,
        contact_name: str,
        contact_title: str,
        company: str,
        position: str,
        resume_summary: str,
        mutual_connections: int = 0
    ) -> str:
        """
        Generate personalized LinkedIn connection request or DM

        Returns:
            Message text (must be under 300 characters for connection request)
        """

        if self.anthropic_client or self.openai_client:
            return self._generate_linkedin_ai(
                contact_name, contact_title, company, position,
                resume_summary, mutual_connections
            )
        else:
            return self._generate_linkedin_template(
                contact_name, contact_title, company, position
            )

    def _generate_email_ai(
        self,
        contact_name: str,
        contact_title: str,
        company: str,
        position: str,
        resume_summary: str,
        job_keywords: list[str],
        contact_info: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """Generate email using AI"""

        # Build context about the contact
        contact_context = ""
        if contact_info:
            if contact_info.get('department'):
                contact_context += f"\n- They work in the {contact_info['department']} department"
            if contact_info.get('linkedin_url'):
                contact_context += f"\n- I found them on LinkedIn"

        prompt = f"""Write a professional, personalized cold outreach email for a job application.

**CONTEXT:**
- Recipient: {contact_name}, {contact_title} at {company}
- Position: {position}
- My Background: {resume_summary}
- Job Keywords: {', '.join(job_keywords[:5])}
{contact_context}

**REQUIREMENTS:**
1. Subject line: Catchy but professional (under 50 characters)
2. Body: 150-200 words
3. Personalized opening referencing their role
4. Briefly mention 1-2 relevant achievements
5. Show genuine interest in company/role
6. Clear call-to-action
7. Professional closing
8. Tone: Confident but not arrogant, enthusiastic but not desperate

**STYLE:**
- Direct and to-the-point (hiring managers are busy)
- No fluff or unnecessary pleasantries
- Highlight value I can bring
- Make it easy to say "yes" to a conversation

Generate the email in this format:
SUBJECT: [subject line]

BODY:
[email body]

Now write the email:"""

        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are an expert at writing cold outreach emails that get responses."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1024,
                )
                content = response.choices[0].message.content

            # Parse response
            parts = content.split('BODY:')
            if len(parts) == 2:
                subject_part = parts[0].replace('SUBJECT:', '').strip()
                body = parts[1].strip()
                return {
                    'subject': subject_part,
                    'body': body
                }
            else:
                # Fallback parsing
                lines = content.split('\n')
                subject = lines[0].replace('SUBJECT:', '').strip()
                body = '\n'.join(lines[2:]).strip()
                return {'subject': subject, 'body': body}

        except Exception as e:
            logger.error(f"Error generating email with AI: {e}")
            return self._generate_email_template(
                contact_name, contact_title, company, position,
                resume_summary, job_keywords
            )

    def _generate_linkedin_ai(
        self,
        contact_name: str,
        contact_title: str,
        company: str,
        position: str,
        resume_summary: str,
        mutual_connections: int
    ) -> str:
        """Generate LinkedIn message using AI"""

        mutual_context = f"We have {mutual_connections} mutual connections." if mutual_connections > 0 else ""

        prompt = f"""Write a short, personalized LinkedIn connection request or direct message.

**CONTEXT:**
- Recipient: {contact_name}, {contact_title} at {company}
- Position I'm interested in: {position}
- My Background: {resume_summary}
{mutual_context}

**REQUIREMENTS:**
1. Under 300 characters (LinkedIn connection limit)
2. Personalized opening
3. Brief mention of why I'm reaching out
4. Friendly, professional tone
5. No hard sell - just starting a conversation

**STYLE:**
- Conversational, not formal
- Show you've done your research
- Make it about mutual benefit, not just asking for help

Write the message:"""

        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}]
                )
                message = response.content[0].text.strip()
            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are an expert at writing LinkedIn messages that get accepted."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=512,
                )
                message = response.choices[0].message.content.strip()

            # Ensure it's under 300 characters
            if len(message) > 300:
                message = message[:297] + "..."

            return message

        except Exception as e:
            logger.error(f"Error generating LinkedIn message with AI: {e}")
            return self._generate_linkedin_template(
                contact_name, contact_title, company, position
            )

    def _generate_email_template(
        self,
        contact_name: str,
        contact_title: str,
        company: str,
        position: str,
        resume_summary: str,
        job_keywords: list[str]
    ) -> Dict[str, str]:
        """Template-based email generation"""

        subject = f"Interested in {position} role at {company}"

        body = f"""Hi {contact_name.split()[0]},

I hope this email finds you well. I noticed the {position} opening at {company} and was immediately drawn to the opportunity.

With my background in {', '.join(job_keywords[:3])}, I believe I could bring significant value to your team. {resume_summary[:100]}

I'd love to learn more about the role and discuss how my experience aligns with {company}'s needs. Would you be open to a brief conversation?

Thank you for your time and consideration.

Best regards"""

        return {'subject': subject, 'body': body}

    def _generate_linkedin_template(
        self,
        contact_name: str,
        contact_title: str,
        company: str,
        position: str
    ) -> str:
        """Template-based LinkedIn message generation"""

        first_name = contact_name.split()[0]

        message = f"""Hi {first_name}, I saw the {position} role at {company} and was impressed by your team's work. I'd love to connect and learn more about the opportunity. Thanks!"""

        # Ensure under 300 chars
        if len(message) > 300:
            message = f"Hi {first_name}, interested in the {position} role at {company}. Would love to connect!"

        return message

    def generate_follow_up(
        self,
        original_message: str,
        days_since: int,
        contact_name: str,
        message_type: str = 'email'
    ) -> str:
        """Generate follow-up message"""

        first_name = contact_name.split()[0]

        if message_type == 'email':
            if days_since <= 5:
                return f"""Hi {first_name},

I wanted to follow up on my email from a few days ago. I'm still very interested in the opportunity and would love to chat if you have 15 minutes.

Let me know if now is a good time or if there's a better time to connect.

Thanks!"""
            else:
                return f"""Hi {first_name},

I hope you're doing well. I wanted to circle back on my previous email about the role.

I've been following {contact_name.split()[-1] if len(contact_name.split()) > 1 else "your company"}'s recent work and remain very interested in contributing to the team.

Would you be open to a quick call to discuss?

Best regards"""

        else:  # LinkedIn
            return f"Hi {first_name}, following up on my previous message. Still very interested in connecting. Let me know if you'd like to chat!"
