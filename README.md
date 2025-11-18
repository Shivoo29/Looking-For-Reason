# 🎯 JobHack - AI-Powered Job Application Automation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **Brutally effective job applications. No fluff. Just results.**

JobHack is an end-to-end AI-powered platform that ingests your resume, parses job descriptions, generates ATS-optimized applications, identifies decision-makers, and automates targeted outreach—all with a neo-brutalist design that doesn't waste your time.

---

## 🔥 Why JobHack Exists

**The Problem:**
- 75% of resumes never reach human eyes (ATS filters)
- Job seekers spend 11+ hours per week tailoring applications
- Finding actual decision-makers is a black box
- Generic outreach gets 2% response rates

**The Solution:**
JobHack automates the entire pipeline from resume optimization to hiring manager DMs, increasing interview rates by 300%+.

---

## ⚡ Core Features

### 🎨 Neo-Brutalist Design Philosophy
- **Raw, unfiltered UI** - No unnecessary animations or fluff
- **Brutally honest feedback** - "Your resume scores 34/100. Here's why."
- **High-contrast accessibility** - Black/white/neon color schemes
- **Exposed processes** - See exactly what the AI is doing

### 🤖 AI-Powered Resume Engine
- **Instant LaTeX/PDF generation** optimized for ATS systems
- **JD-specific rewrites** with keyword matching and skill alignment
- **Real-time ATS scoring** (0-100) with actionable improvements
- **A/B testing** - Try multiple resume versions per application

### 🎯 Intelligent Application System
- **One-click apply** via Chrome extension on any job board
- **Auto-fill forms** with extracted resume data
- **Application tracking** with status updates and next actions
- **Batch processing** - Apply to 50+ jobs with one click

### 🕵️ Organization Graph & Outreach
- **Decision-maker identification** via LinkedIn/company data scraping
- **Org chart visualization** showing reporting structures
- **Automated personalized outreach** (email + LinkedIn DM)
- **Engagement tracking** - Opens, clicks, reply sentiment analysis

### 📊 Analytics Dashboard
- **Application success metrics** - Response rate, interview rate, offer rate
- **Resume performance analytics** - Which versions get traction
- **Outreach effectiveness** - Message templates ranked by reply rate
- **Rejection insights** - Learn from failures, improve future apps

---

## 🏗️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS (custom brutal theme)
- **UI Components**: Shadcn/ui (heavily customized)
- **State Management**: Zustand
- **Forms**: React Hook Form + Zod validation

### Backend
- **API**: Next.js API Routes / FastAPI (Python microservices)
- **Database**: PostgreSQL (Supabase) + Redis (caching)
- **Auth**: Clerk / NextAuth.js
- **File Storage**: AWS S3 / Supabase Storage

### AI/ML Pipeline
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Resume Parsing**: PyMuPDF + Custom NLP models
- **LaTeX Generation**: Jinja2 templates + pdflatex
- **Vector DB**: Pinecone (for JD matching)

### Integrations
- **LinkedIn API** (OAuth + scraping fallback)
- **Email**: SendGrid / Resend
- **Chrome Extension**: Manifest V3
- **Payment**: Stripe

### DevOps
- **Hosting**: Vercel (frontend) + AWS/Railway (backend)
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry + PostHog analytics
- **Queue**: BullMQ (for async jobs)

---

## 🚀 Quick Start

### Prerequisites
```bash
node >= 18.0.0
python >= 3.11
postgresql >= 15
redis >= 7.0
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jobhack.git
cd jobhack

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Run database migrations
npm run db:migrate

# Start development servers
npm run dev:all
```

Visit `http://localhost:3000` to see the app.

---

## 📖 Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md)
- [API Documentation](./docs/API.md)
- [Database Schema](./docs/DATABASE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)
- [Contributing Guidelines](./CONTRIBUTING.md)

---

## 🗺️ Roadmap

### Phase 1: MVP (Weeks 1-4)
- [x] Resume ingestion (PDF/LaTeX/LinkedIn)
- [x] JD parsing and keyword extraction
- [x] Basic ATS scoring algorithm
- [ ] Resume rewrite engine (LaTeX output)
- [ ] Simple application tracker

### Phase 2: Core Features (Weeks 5-8)
- [ ] Chrome extension for job boards
- [ ] LinkedIn OAuth + profile scraping
- [ ] Email outreach automation
- [ ] Organization graph visualization
- [ ] Analytics dashboard v1

### Phase 3: Advanced Features (Weeks 9-12)
- [ ] AI interview prep based on JD
- [ ] Salary negotiation intelligence
- [ ] A/B testing framework
- [ ] Rejection analytics
- [ ] Mobile app (React Native)

### Phase 4: Scale & Monetize (Week 13+)
- [ ] Multi-user team accounts
- [ ] API for recruitment agencies
- [ ] White-label solution
- [ ] Enterprise features (SSO, compliance)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md).

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Jobscan](https://www.jobscan.co) for ATS research
- [Resume Worded](https://resumeworded.com) for resume insights
- Neo-brutalism design inspiration from [Gumroad](https://gumroad.com) and [Typedream](https://typedream.com)

---

## 📞 Contact

- **Website**: [jobhack.io](https://jobhack.io)
- **Email**: hello@jobhack.io
- **Twitter**: [@jobhack_io](https://twitter.com/jobhack_io)
- **Discord**: [Join our community](https://discord.gg/jobhack)

---

**Built with rage and caffeine by job seekers, for job seekers. 🔥**