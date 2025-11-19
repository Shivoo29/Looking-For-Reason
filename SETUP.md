# JobHack - Complete Setup Guide

This guide will walk you through setting up the complete JobHack platform on your local machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Frontend Setup](#frontend-setup)
4. [Backend Setup](#backend-setup)
5. [Database Setup](#database-setup)
6. [Chrome Extension Setup](#chrome-extension-setup)
7. [Configuration](#configuration)
8. [Running the Application](#running-the-application)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Node.js** >= 18.0.0 ([Download](https://nodejs.org/))
- **Python** >= 3.11 ([Download](https://www.python.org/))
- **PostgreSQL** >= 15 ([Download](https://www.postgresql.org/))
- **Git** ([Download](https://git-scm.com/))

### Optional (for full functionality)
- **Redis** >= 7.0 ([Download](https://redis.io/))
- **pdflatex** (for LaTeX resume generation)

### API Keys Required

You'll need API keys for:
- **Anthropic Claude** or **OpenAI GPT-4** (for AI features)
- **Clerk** or **NextAuth** (for authentication)
- **Stripe** (for payments)
- **SendGrid** or **Resend** (for email outreach)

---

## Quick Start

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

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
cd ..
./scripts/setup-database.sh

# Start the application
./scripts/start-dev.sh
```

---

## Frontend Setup

### 1. Navigate to frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

Create a `.env.local` file:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_APP_NAME=JobHack
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
CLERK_SECRET_KEY=sk_test_your_key_here

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
```

### 4. Run development server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

---

## Backend Setup

### 1. Navigate to backend directory

```bash
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Server
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_ORIGINS=http://localhost:3000

# Database
DATABASE_URL=postgresql://jobhack_user:password@localhost:5432/jobhack_db

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Services
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here

# Email
SENDGRID_API_KEY=SG.your-key-here
FROM_EMAIL=noreply@jobhack.io

# Stripe
STRIPE_SECRET_KEY=sk_test_your-key-here

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
```

### 5. Run the server

```bash
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/api/docs`

---

## Database Setup

### 1. Install PostgreSQL

Follow the installation instructions for your operating system from [PostgreSQL Downloads](https://www.postgresql.org/download/).

### 2. Create database and user

```bash
# Start PostgreSQL service
sudo service postgresql start  # Linux
# or
brew services start postgresql  # macOS

# Access PostgreSQL shell
psql postgres

# In PostgreSQL shell:
CREATE DATABASE jobhack_db;
CREATE USER jobhack_user WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE jobhack_db TO jobhack_user;
\q
```

### 3. Run migrations

The database tables will be created automatically when you start the backend server for the first time.

Alternatively, you can create them manually:

```bash
cd backend
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

---

## Chrome Extension Setup

### 1. Build the extension

The extension files are already in the `chrome-extension` directory.

### 2. Load extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` directory from this project
5. The JobHack extension should now appear in your extensions list

### 3. Configure extension

1. Click the JobHack extension icon
2. Log in with your JobHack credentials
3. Select your default resume
4. The extension is now ready to use!

---

## Configuration

### AI Services

The platform supports both Anthropic Claude and OpenAI GPT-4. Configure at least one:

**Anthropic Claude (Recommended):**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**OpenAI GPT-4:**
```env
OPENAI_API_KEY=sk-your-key-here
```

### Email Service

For outreach features, configure an email service:

**SendGrid:**
```env
SENDGRID_API_KEY=SG.your-key-here
FROM_EMAIL=noreply@jobhack.io
```

**Resend:**
```env
RESEND_API_KEY=re_your-key-here
FROM_EMAIL=noreply@jobhack.io
```

### File Storage

By default, files are stored locally. For production, use S3:

```env
STORAGE_TYPE=s3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=jobhack-files
AWS_REGION=us-east-1
```

---

## Running the Application

### Development Mode

**Option 1: Manual Start**

Terminal 1 - Frontend:
```bash
cd frontend
npm run dev
```

Terminal 2 - Backend:
```bash
cd backend
source venv/bin/activate
python main.py
```

Terminal 3 - Database (if not running as service):
```bash
sudo service postgresql start
```

**Option 2: Using Scripts**

```bash
# From project root
./scripts/start-dev.sh
```

### Production Mode

```bash
# Build frontend
cd frontend
npm run build
npm start

# Run backend with production settings
cd backend
ENVIRONMENT=production uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Testing the Setup

### 1. Test Backend API

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Test Frontend

Open `http://localhost:3000` in your browser. You should see the JobHack landing page.

### 3. Test Full Flow

1. Register a new account at `http://localhost:3000/sign-up`
2. Upload a resume
3. Create a job description
4. Generate an optimized resume
5. Create an application
6. Generate outreach message

---

## Troubleshooting

### Frontend Issues

**Issue: `npm install` fails**
- Solution: Update Node.js to version 18 or higher
- Check: `node --version`

**Issue: Port 3000 already in use**
- Solution: Kill the process or use a different port
```bash
lsof -ti:3000 | xargs kill  # macOS/Linux
npm run dev -- --port 3001   # Use different port
```

### Backend Issues

**Issue: Database connection fails**
- Check PostgreSQL is running: `sudo service postgresql status`
- Verify connection string in `.env`
- Test connection: `psql $DATABASE_URL`

**Issue: Import errors**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Issue: Port 8000 already in use**
```bash
lsof -ti:8000 | xargs kill  # Kill process
# or
uvicorn main:app --port 8001  # Use different port
```

### AI Service Issues

**Issue: "No AI API keys configured"**
- Add either `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` to `.env`
- Restart the backend server

**Issue: AI requests failing**
- Verify API key is valid
- Check API quota/limits
- Review error logs in backend terminal

### Database Issues

**Issue: Tables not created**
```bash
cd backend
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

**Issue: Permission denied**
```bash
# Grant permissions in PostgreSQL
psql jobhack_db
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO jobhack_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO jobhack_user;
```

### Chrome Extension Issues

**Issue: Extension not loading**
- Ensure all files are in `chrome-extension` directory
- Check for JavaScript errors in Chrome console
- Reload extension in `chrome://extensions/`

**Issue: Cannot connect to API**
- Verify backend is running at `http://localhost:8000`
- Check CORS settings in `backend/main.py`
- Ensure `http://localhost:3000` is in `ALLOWED_ORIGINS`

---

## Next Steps

After successful setup:

1. **Explore the Documentation**
   - [API Documentation](API.md)
   - [Architecture Overview](ARCHITECTURE.md)
   - [Project Summary](Project_summary.md)

2. **Customize the Platform**
   - Modify neo-brutalist design in `frontend/tailwind.config.js`
   - Add custom ATS scoring rules in `backend/app/services/ats_scorer.py`
   - Create custom resume templates

3. **Deploy to Production**
   - Frontend: Deploy to Vercel
   - Backend: Deploy to Railway or AWS
   - Database: Use managed PostgreSQL (RDS, Supabase, etc.)

4. **Add Integrations**
   - LinkedIn API for org graph
   - More job boards for auto-apply
   - Analytics platforms (PostHog, Mixpanel)

---

## Support

If you encounter issues not covered here:

1. Check existing issues: [GitHub Issues](https://github.com/yourusername/jobhack/issues)
2. Review logs in backend terminal
3. Check browser console for frontend errors
4. Join our Discord community

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

**Built with rage and caffeine. Good luck with your job search! 🔥**
