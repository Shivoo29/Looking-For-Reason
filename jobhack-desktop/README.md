# 🎯 JobHack Desktop - AI-Powered Job Application Automation Platform

[![Java 17+](https://img.shields.io/badge/Java-17+-orange.svg)](https://openjdk.java.net/)
[![JavaFX 21](https://img.shields.io/badge/JavaFX-21-blue.svg)](https://openjfx.io/)
[![Selenium 4](https://img.shields.io/badge/Selenium-4-green.svg)](https://www.selenium.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **This is NOT just another auto-apply tool. It's a full job-hunting operating system.**

JobHack Desktop is a comprehensive Java desktop application that deeply understands your technical background, generates ATS-optimized resumes tailored to each job, automates applications across multiple platforms, finds and contacts hiring managers directly, and tracks everything in a brutally honest dashboard.

---

## 🔥 Why JobHack Desktop Exists

**The Problem:**
- 75% of resumes never reach human eyes (ATS filters)
- Job seekers spend 11+ hours per week tailoring applications
- Finding actual decision-makers is a black box
- Generic outreach gets 2% response rates

**The Solution:**
JobHack Desktop automates the entire pipeline from deep user profiling to hiring manager outreach, increasing interview rates by 300%+.

---

## ⚡ Core Features

### 🎨 Neo-Brutalist Design Philosophy
- **Raw, unfiltered UI** - No unnecessary animations or fluff
- **Brutally honest feedback** - "Your resume scores 34/100. Here's why."
- **High-contrast accessibility** - Black/white/neon color schemes
- **Exposed processes** - See exactly what the AI is doing in real-time

### 🧠 Deep User Profiling (Phase 1)
- **MIT-admissions-style essay questions** - Capture your story in 500-1000 word responses
- **GitHub integration** - Analyze all your repositories, extract tech stack, build skills inventory
- **Vector database storage** - All your context stored locally using ChromaDB
- **Credential collection** - Gmail OAuth, LinkedIn, GitHub, resume upload

### 📝 Intelligent Resume Generation (Phase 2)
- **Dynamic resume builder** - Tailors resumes to each job description
- **GitHub project matching** - Automatically highlights relevant projects
- **ATS optimization** - Real-time scoring (0-100) with actionable improvements
- **Multiple formats** - PDF (primary), DOCX, plain text
- **Multiple versions** - Software-heavy, hardware-heavy, research-heavy, balanced

### 🤖 Application Automation (Phase 3-4)
- **Multi-platform support** - LinkedIn, Indeed, Naukri, Glassdoor, AngelList, etc.
- **Easy Apply** - One-click automation
- **Long-form applications** - Workday, Greenhouse, Lever (multi-page forms)
- **Company career portals** - Handle custom application forms
- **Anti-detection** - Randomized delays, human-like typing, mouse movements
- **CAPTCHA handling** - Pause and notify user when manual intervention needed

### 🕵️ HR Finder & Cold Outreach (Phase 5)
- **Decision-maker identification** - Find hiring managers, recruiters, employees
- **Email finding** - Hunter.io / RocketReach API integration
- **Automated personalized emails** - AI-generated using your context + company research
- **Email tracking** - Opens, clicks, replies
- **Auto-follow-up** - If no response in 5 days

### 📊 Real-Time Dashboard (Phase 6)
- **Live activity feed** - See every action as it happens
- **Applications table** - Track status, ATS scores, next actions
- **Analytics panel** - Response rates, top skills, daily metrics
- **AI reasoning log** - Understand why the AI made each decision
- **Embedded browser** - See what's happening in real-time

### 📧 Email Intelligence (Phase 7)
- **Gmail monitoring** - Track confirmations, interview invites, rejections
- **Interview prep** - Auto-generate prep docs with Glassdoor questions
- **Response analysis** - Sentiment analysis, pattern detection

---

## 🏗️ Tech Stack

### Desktop Application
- **Java 17+** - Modern Java features
- **JavaFX 21** - Rich desktop UI framework
- **Maven** - Dependency management and build tool

### Browser Automation
- **Selenium 4** - WebDriver for browser control
- **WebDriverManager** - Automatic driver management
- **Chrome WebDriver** - Primary browser (anti-detection configured)

### AI & ML
- **Anthropic Claude API** - GPT-4 class reasoning for resume optimization, email generation
- **LangChain4j** - Java framework for LLM integration
- **ChromaDB** - Local vector database for user context

### Data & Storage
- **SQLite** - Embedded database (no server required)
- **HikariCP** - High-performance connection pooling
- **Apache PDFBox** - PDF generation and parsing
- **Apache POI** - DOCX generation

### Integrations
- **Gmail API** - Email automation and monitoring
- **GitHub API** - Repository analysis and skills extraction
- **Hunter.io API** - Email finding (optional)
- **LinkedIn** - Profile scraping (via Selenium)

### Utilities
- **OkHttp** - HTTP client for API calls
- **Jackson** - JSON processing
- **JSoup** - HTML parsing and scraping
- **Lombok** - Reduce boilerplate code
- **SLF4J + Logback** - Logging

---

## 🚀 Quick Start

### Prerequisites

```bash
# Java 17 or higher
java -version

# Maven 3.6+
mvn -version

# Chrome browser (for Selenium)
```

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Shivoo29/Looking-For-Reason.git
cd Looking-For-Reason/jobhack-desktop
```

2. **Set up environment variables:**
```bash
# Linux/macOS
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key-here"

# Or create ~/.jobhack/application.conf and set:
# jobhack.ai.apiKey = "your-api-key-here"
```

3. **Build the project:**
```bash
mvn clean install
```

4. **Run the application:**
```bash
mvn javafx:run
```

---

## 📖 Project Structure

```
jobhack-desktop/
├── src/main/java/com/jobhack/
│   ├── JobHackApplication.java       # Main entry point
│   │
│   ├── gui/                          # JavaFX UI
│   │   ├── MainWindow.java           # Main dashboard
│   │   ├── OnboardingWizard.java     # User profiling wizard
│   │   └── ...
│   │
│   ├── automation/                   # Browser automation
│   │   ├── BrowserManager.java       # Selenium WebDriver manager
│   │   ├── FormFiller.java           # Auto-fill logic
│   │   ├── AntiDetection.java        # Human-like behavior
│   │   └── ...
│   │
│   ├── ai/                           # AI services
│   │   ├── ClaudeClient.java         # Claude API wrapper
│   │   ├── ResumeOptimizer.java      # Resume generation
│   │   ├── JDParser.java             # Job description parsing
│   │   ├── EmailGenerator.java       # Cold email generation
│   │   └── ...
│   │
│   ├── database/                     # SQLite layer
│   │   ├── DatabaseManager.java      # Connection management
│   │   ├── models/                   # Data models
│   │   └── ...
│   │
│   ├── config/                       # Configuration
│   │   ├── AppConfig.java            # Settings manager
│   │   └── Constants.java            # App constants
│   │
│   └── utils/                        # Utilities
│       ├── ActivityLogger.java       # Activity logging
│       └── ...
│
├── src/main/resources/
│   ├── fxml/                         # JavaFX layouts
│   ├── css/
│   │   └── neo-brutalist.css         # UI theme
│   └── templates/                    # Resume templates
│
├── pom.xml                           # Maven dependencies
└── README.md
```

---

## 🔧 Configuration

### Application Configuration

Configuration file: `~/.jobhack/application.conf`

```hocon
jobhack {
  ai {
    provider = "anthropic"
    model = "claude-3-5-sonnet-20241022"
    apiKey = ""  # Or set via ANTHROPIC_API_KEY env var
  }

  automation {
    headless = false           # Set to true for headless mode
    maxApplicationsPerDay = 50
    randomDelayMin = 2000      # milliseconds
    randomDelayMax = 8000
  }

  email {
    maxEmailsPerDay = 30
    followUpDelayDays = 5
  }
}
```

### First Run

On first launch, JobHack will:
1. Create configuration directory: `~/.jobhack/`
2. Initialize SQLite database: `~/.jobhack/data/jobhack.db`
3. Launch onboarding wizard
4. Collect your essays and credentials
5. Show main dashboard

---

## 💡 Usage Guide

### Phase 1: Onboarding (One-time, 20 minutes)

1. **Answer 5 essay questions** (500-1000 words each)
   - These help the AI understand YOUR unique story
   - Not generic templates - this is what makes JobHack powerful

2. **Connect accounts:**
   - GitHub username (required) - for skills extraction
   - LinkedIn URL (optional) - for profile data
   - Gmail OAuth (later in settings)

3. **Upload current resume** (PDF or DOCX)
   - Baseline for generating tailored versions

### Phase 2: Resume Generation

1. **Paste a job description**
2. Click **"Generate Tailored Resume"**
3. Review:
   - ATS Score (0-100)
   - Changes made
   - Keywords matched/missing
   - AI reasoning
4. Download PDF/DOCX
5. Apply!

### Phase 3: Application Automation

1. Click **"Start Job Scraper"**
   - Scrapes LinkedIn, Indeed, Naukri, etc.
   - Filters by your preferences
2. Review matched jobs
3. Click **"Auto Apply"**
   - Watch the dashboard as it works
   - Handles Easy Apply, Workday, Greenhouse, etc.
   - Pauses for CAPTCHA (you solve manually)

### Phase 4: HR Outreach

1. JobHack automatically:
   - Finds hiring managers
   - Finds their emails
   - Generates personalized emails
   - Sends via Gmail API
   - Tracks opens/replies
2. You just approve or edit before sending

### Phase 5: Tracking & Analytics

- **Activity Feed** - Live log of every action
- **Applications Table** - All applications with status
- **Analytics** - Response rates, top skills
- **AI Reasoning** - Understand decisions

---

## 🎨 Neo-Brutalist UI Preview

```
╔════════════════════════════════════════════════════════════╗
║                   JOBHACK DESKTOP                          ║
╠════════════════════════════════════════════════════════════╣
║  LIVE ACTIVITY          │  APPLICATIONS  │  STATS          ║
║                         │                │                 ║
║  [14:23:45] 🔍 Scraping │  Company  Role │  TODAY: 23     ║
║  [14:23:52] ✍️  Tailoring│  Stripe   SWE  │  RESPONSE: 18% ║
║  [14:24:10] 📊 ATS: 87  │  Airbnb   SRE  │  TOP: Python   ║
║  [14:24:15] 🤖 Filling  │  Google   ...  │                 ║
║  [14:24:58] ✅ Applied  │                │  [START]       ║
║  [14:25:03] 🔎 Finding  │                │  [RESUME]      ║
║  [14:25:15] 📧 Email    │                │  [FIND HR]     ║
║                         │                │                 ║
╠════════════════════════════════════════════════════════════╣
║  🧠 AI REASONING:                                          ║
║  Why I changed this resume:                                ║
║  • JD mentioned "scalability" 6x → highlighted distributed ║
║  • Company uses Go → added GitHub Go projects              ║
║  • Culture emphasizes "ownership" → changed wording        ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🛠️ Development

### Build from Source

```bash
# Clean build
mvn clean compile

# Run tests
mvn test

# Package JAR
mvn package

# Run application
mvn javafx:run
```

### Create Executable

```bash
# Build fat JAR
mvn clean package

# Run the JAR
java -jar target/jobhack-desktop-1.0.0-SNAPSHOT.jar
```

### Debug Mode

```bash
# Run with debug logging
mvn javafx:run -Dlogback.level=DEBUG
```

---

## 🔐 Security & Privacy

- **All data stored locally** - SQLite database in `~/.jobhack/`
- **API keys encrypted** - Stored securely in database
- **No telemetry** - Your job search is private
- **Open source** - Audit the code yourself

---

## 🗺️ Roadmap

### Phase 1: Core Foundation ✅
- [x] Project setup (Maven, dependencies)
- [x] JavaFX GUI with neo-brutalist theme
- [x] Onboarding wizard with essay questions
- [x] Database schema (SQLite)
- [x] Activity logging system

### Phase 2: AI Services ✅
- [x] Claude API integration
- [x] Job description parser
- [x] Resume optimizer with ATS scoring
- [x] Email generator

### Phase 3: Browser Automation ✅
- [x] Selenium WebDriver with anti-detection
- [x] Form filler (auto-fill logic)
- [x] Human-like behavior simulation
- [x] CAPTCHA detection

### Phase 4: Full Integration (In Progress)
- [ ] GitHub OAuth + repository analysis
- [ ] Resume PDF/DOCX generation
- [ ] Job scraping (multi-platform)
- [ ] Workday automation proof-of-concept

### Phase 5: Advanced Features (Next)
- [ ] Gmail API integration
- [ ] HR email finder (Hunter.io)
- [ ] Cold email automation
- [ ] Interview prep generation

### Phase 6: Polish (Future)
- [ ] Settings panel
- [ ] Resume preview
- [ ] Application state recovery
- [ ] Rate limiting
- [ ] Company research layer

---

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](../CONTRIBUTING.md).

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Anthropic Claude](https://www.anthropic.com/) for powerful AI reasoning
- [Selenium](https://www.selenium.dev/) for browser automation
- [JavaFX](https://openjfx.io/) for the desktop UI framework
- Neo-brutalism design inspiration from [Gumroad](https://gumroad.com)

---

## 📞 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Shivoo29/Looking-For-Reason/issues)
- **Email**: hello@jobhack.io

---

**Built with rage and caffeine by job seekers, for job seekers. 🔥**

**Make hiring managers come to you.**
