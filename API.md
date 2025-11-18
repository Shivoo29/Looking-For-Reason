# JobHack API Documentation

Complete API reference for JobHack backend services.

**Base URL:** `https://api.jobhack.io/v1`

**Authentication:** Bearer token in `Authorization` header

---

## 🔐 Authentication

### POST /auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": "uuid",
  "token": "jwt_token"
}
```

### POST /auth/login
Login with existing credentials.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "success": true,
  "token": "jwt_token",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## 📄 Resume Management

### POST /resume/upload
Upload and parse a resume.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF, DOCX, or LaTeX)

**Response:**
```json
{
  "success": true,
  "resume_id": "uuid",
  "parsed_data": {
    "contact": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "linkedin": "https://linkedin.com/in/johndoe"
    },
    "experience": [...],
    "education": [...],
    "skills": [...]
  }
}
```

### GET /resume/{id}
Get resume details.

**Response:**
```json
{
  "id": "uuid",
  "title": "Software Engineer Resume",
  "content": {...},
  "ats_score": 85,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /resume/{id}/optimize
Optimize resume for a specific job description.

**Request:**
```json
{
  "job_description_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "optimized_resume_id": "uuid",
  "improvements": [
    "Added 12 relevant keywords",
    "Restructured experience bullets",
    "Improved ATS score from 72 to 89"
  ],
  "before_after": {
    "before_score": 72,
    "after_score": 89
  }
}
```

### POST /resume/{id}/generate-latex
Generate LaTeX/PDF version.

**Request:**
```json
{
  "template": "modern",  // modern, classic, minimal
  "options": {
    "font_size": 11,
    "margins": "normal"
  }
}
```

**Response:**
```json
{
  "success": true,
  "latex_source": "\\documentclass...",
  "pdf_url": "https://storage.jobhack.io/resumes/uuid.pdf"
}
```

---

## 💼 Job Applications

### POST /application/parse-jd
Parse a job description.

**Request:**
```json
{
  "url": "https://linkedin.com/jobs/...",
  "text": "Optional: raw JD text if URL not available"
}
```

**Response:**
```json
{
  "success": true,
  "jd_id": "uuid",
  "parsed_data": {
    "title": "Senior Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "required_skills": ["Python", "React", "AWS"],
    "experience_level": "senior",
    "keywords": ["python", "react", "kubernetes", ...],
    "salary_range": "$150k - $200k"
  }
}
```

### POST /application/submit
Submit a job application.

**Request:**
```json
{
  "resume_id": "uuid",
  "jd_id": "uuid",
  "cover_letter": "Optional custom cover letter",
  "auto_apply": true,
  "auto_outreach": true
}
```

**Response:**
```json
{
  "success": true,
  "application_id": "uuid",
  "status": "submitted",
  "ats_score": 87,
  "outreach_scheduled": true,
  "decision_makers_found": 3
}
```

### GET /application/{id}
Get application details.

**Response:**
```json
{
  "id": "uuid",
  "job_title": "Senior Software Engineer",
  "company": "Tech Corp",
  "status": "interviewing",
  "applied_at": "2024-01-01T00:00:00Z",
  "response_at": "2024-01-05T14:30:00Z",
  "ats_score": 87,
  "outreach_messages": [
    {
      "type": "email",
      "recipient": "hiring.manager@techcorp.com",
      "sent_at": "2024-01-02T10:00:00Z",
      "opened": true,
      "replied": true
    }
  ],
  "notes": "Great conversation with hiring manager..."
}
```

### GET /applications
List all applications with filters.

**Query Parameters:**
- `status`: pending, submitted, interviewing, rejected, offer
- `company`: Filter by company name
- `date_from`: ISO date
- `date_to`: ISO date
- `sort`: created_at, company, status
- `limit`: Number of results (default 50)
- `offset`: Pagination offset

**Response:**
```json
{
  "applications": [...],
  "total": 150,
  "page": 1,
  "pages": 3
}
```

### PATCH /application/{id}
Update application status or notes.

**Request:**
```json
{
  "status": "interviewing",
  "notes": "Phone screen scheduled for next Tuesday",
  "interview_date": "2024-01-15T10:00:00Z"
}
```

---

## 🎯 ATS Scoring

### POST /ats/score
Calculate ATS score for resume-JD pair.

**Request:**
```json
{
  "resume_id": "uuid",
  "jd_id": "uuid"
}
```

**Response:**
```json
{
  "total_score": 85,
  "breakdown": {
    "keyword_match": 88,
    "format_quality": 90,
    "section_completeness": 85,
    "skills_alignment": 82,
    "experience_relevance": 78
  },
  "suggestions": [
    "Add 'Kubernetes' keyword (appears 5x in JD)",
    "Quantify achievements in your bullets",
    "Include 'leadership' in your experience descriptions"
  ],
  "missing_keywords": ["kubernetes", "microservices", "ci/cd"]
}
```

---

## 🕵️ Outreach & Organization Graph

### POST /outreach/find-decision-makers
Find hiring managers and decision makers.

**Request:**
```json
{
  "company": "Tech Corp",
  "job_title": "Senior Software Engineer",
  "department": "Engineering"
}
```

**Response:**
```json
{
  "success": true,
  "decision_makers": [
    {
      "name": "Jane Smith",
      "title": "Engineering Manager",
      "email": "jane.smith@techcorp.com",
      "linkedin": "https://linkedin.com/in/janesmith",
      "relevance_score": 95,
      "department": "Engineering",
      "reports_to": "VP of Engineering"
    },
    ...
  ],
  "org_chart_url": "https://jobhack.io/org-graph/uuid"
}
```

### POST /outreach/generate-message
Generate personalized outreach message.

**Request:**
```json
{
  "recipient_id": "uuid",
  "application_id": "uuid",
  "message_type": "email",  // or "linkedin_dm"
  "tone": "professional"     // professional, casual, confident
}
```

**Response:**
```json
{
  "subject": "Re: Senior Software Engineer role at Tech Corp",
  "body": "Hi Jane,\n\nI noticed you're leading...",
  "call_to_action": "15-minute chat this week",
  "personalization_score": 92
}
```

### POST /outreach/send
Send email or LinkedIn DM.

**Request:**
```json
{
  "recipient_id": "uuid",
  "message_id": "uuid",
  "schedule_for": "2024-01-02T09:00:00Z",  // Optional: schedule for later
  "attach_resume": true
}
```

**Response:**
```json
{
  "success": true,
  "outreach_id": "uuid",
  "sent_at": "2024-01-02T09:00:00Z",
  "tracking_enabled": true
}
```

### GET /outreach/{id}/engagement
Get engagement metrics for sent message.

**Response:**
```json
{
  "id": "uuid",
  "sent_at": "2024-01-02T09:00:00Z",
  "opened": true,
  "open_count": 3,
  "first_opened_at": "2024-01-02T09:15:00Z",
  "clicked": true,
  "click_count": 1,
  "replied": true,
  "reply_at": "2024-01-02T14:30:00Z",
  "reply_content": "Thanks for reaching out! Let's schedule a call..."
}
```

---

## 📊 Analytics

### GET /analytics/overview
Get overview analytics for user.

**Query Parameters:**
- `date_from`: ISO date
- `date_to`: ISO date

**Response:**
```json
{
  "applications": {
    "total": 150,
    "pending": 20,
    "interviewing": 12,
    "offers": 3,
    "rejected": 45
  },
  "response_rate": 32.5,
  "interview_rate": 18.2,
  "offer_rate": 8.1,
  "avg_ats_score": 84.3,
  "avg_response_time_days": 5.2,
  "top_performing_resume": {
    "id": "uuid",
    "title": "Senior Engineer - Optimized",
    "response_rate": 45.2
  },
  "outreach_stats": {
    "emails_sent": 75,
    "open_rate": 62.3,
    "reply_rate": 28.1
  }
}
```

### GET /analytics/funnel
Get application funnel data.

**Response:**
```json
{
  "funnel": [
    { "stage": "Applied", "count": 150 },
    { "stage": "Viewed", "count": 98 },
    { "stage": "Response", "count": 48 },
    { "stage": "Phone Screen", "count": 27 },
    { "stage": "Interview", "count": 12 },
    { "stage": "Offer", "count": 3 }
  ],
  "conversion_rates": {
    "applied_to_response": 32.0,
    "response_to_interview": 25.0,
    "interview_to_offer": 25.0
  }
}
```

### GET /analytics/insights
Get AI-generated insights and recommendations.

**Response:**
```json
{
  "insights": [
    {
      "type": "performance",
      "severity": "info",
      "message": "Your response rate improved by 15% this week!",
      "action": null
    },
    {
      "type": "recommendation",
      "severity": "warning",
      "message": "Your ATS scores are below 75 for tech roles",
      "action": "Add more technical keywords like 'Docker', 'Kubernetes'"
    },
    {
      "type": "pattern",
      "severity": "info",
      "message": "You get 3x more responses when applying on Tuesdays",
      "action": "Schedule more applications for Tuesdays"
    }
  ],
  "top_recommendation": "Increase outreach volume - you're only reaching 30% of decision makers"
}
```

---

## 🧪 A/B Testing

### POST /ab-test/create
Create an A/B test for resumes or messages.

**Request:**
```json
{
  "type": "resume",  // or "message"
  "base_id": "uuid",
  "variants": [
    { "name": "Technical Focus", "modifications": {...} },
    { "name": "Leadership Focus", "modifications": {...} }
  ],
  "target_metric": "response_rate",
  "min_samples": 50
}
```

**Response:**
```json
{
  "success": true,
  "test_id": "uuid",
  "status": "active",
  "estimated_completion": "2024-02-01"
}
```

### GET /ab-test/{id}
Get A/B test results.

**Response:**
```json
{
  "id": "uuid",
  "status": "completed",
  "winner": "variant_1",
  "results": [
    {
      "variant": "control",
      "applications": 52,
      "responses": 16,
      "response_rate": 30.8
    },
    {
      "variant": "variant_1",
      "applications": 51,
      "responses": 23,
      "response_rate": 45.1,
      "lift": 46.4,
      "significance": 0.03
    }
  ],
  "recommendation": "Use Variant 1 - 46% lift with 97% confidence"
}
```

---

## 💰 Salary Intelligence

### POST /salary/insights
Get salary insights for a role.

**Request:**
```json
{
  "job_title": "Senior Software Engineer",
  "company": "Tech Corp",
  "location": "San Francisco, CA",
  "years_experience": 7
}
```

**Response:**
```json
{
  "base_salary": {
    "min": 150000,
    "median": 175000,
    "max": 220000,
    "percentile_75": 195000
  },
  "total_compensation": {
    "min": 200000,
    "median": 250000,
    "max": 350000
  },
  "breakdown": {
    "base": 175000,
    "bonus": 25000,
    "equity": 50000
  },
  "market_percentile": 65,
  "data_sources": ["Glassdoor", "Levels.fyi", "Blind"],
  "negotiation_tips": [
    "Your target should be $180k-$200k base",
    "Emphasize your AWS and Kubernetes experience",
    "Ask about signing bonus - common for this level"
  ]
}
```

---

## 🔧 Webhooks

### POST /webhooks/register
Register a webhook for events.

**Request:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["application.response", "outreach.reply", "interview.scheduled"],
  "secret": "your_webhook_secret"
}
```

**Webhook Payload Example:**
```json
{
  "event": "application.response",
  "timestamp": "2024-01-02T14:30:00Z",
  "data": {
    "application_id": "uuid",
    "company": "Tech Corp",
    "job_title": "Senior Software Engineer",
    "response_type": "interview_request"
  }
}
```

---

## ⚡ Rate Limits

- **Free Tier:** 100 requests/hour
- **Pro Tier:** 1,000 requests/hour
- **Enterprise:** 10,000 requests/hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1704196800
```

---

## 🚨 Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

**Error Response Format:**
```json
{
  "error": {
    "code": "INVALID_RESUME",
    "message": "Resume file is corrupted or invalid format",
    "details": {
      "supported_formats": ["PDF", "DOCX", "LaTeX"]
    }
  }
}
```

---

## 📚 SDKs

### JavaScript/TypeScript
```bash
npm install @jobhack/sdk
```

```typescript
import { JobHack } from '@jobhack/sdk';

const client = new JobHack({ apiKey: 'your_api_key' });

// Upload resume
const resume = await client.resume.upload('./resume.pdf');

// Parse JD and optimize
const jd = await client.application.parseJD('https://linkedin.com/jobs/...');
const optimized = await client.resume.optimize(resume.id, jd.id);

// Submit application
const app = await client.application.submit({
  resumeId: optimized.id,
  jdId: jd.id,
  autoApply: true,
});
```

### Python
```bash
pip install jobhack-sdk
```

```python
from jobhack import JobHack

client = JobHack(api_key='your_api_key')

# Upload resume
resume = client.resume.upload('./resume.pdf')

# Parse JD and optimize
jd = client.application.parse_jd(url='https://linkedin.com/jobs/...')
optimized = client.resume.optimize(resume.id, jd.id)

# Submit application
app = client.application.submit(
    resume_id=optimized.id,
    jd_id=jd.id,
    auto_apply=True
)
```

---

For more examples and detailed guides, visit [docs.jobhack.io](https://docs.jobhack.io)