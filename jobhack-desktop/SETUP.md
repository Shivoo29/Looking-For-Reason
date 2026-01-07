# 🚀 JobHack Desktop - Setup Guide

This guide will help you set up and run JobHack Desktop for the first time.

---

## Prerequisites

### Required Software

1. **Java 17 or higher**
   ```bash
   # Check your Java version
   java -version

   # If not installed:
   # Ubuntu/Debian
   sudo apt install openjdk-17-jdk

   # macOS (using Homebrew)
   brew install openjdk@17

   # Windows
   # Download from https://adoptium.net/
   ```

2. **Maven 3.6+**
   ```bash
   # Check Maven version
   mvn -version

   # If not installed:
   # Ubuntu/Debian
   sudo apt install maven

   # macOS
   brew install maven

   # Windows
   # Download from https://maven.apache.org/
   ```

3. **Google Chrome**
   - Required for Selenium WebDriver
   - Download: https://www.google.com/chrome/

### Required API Keys

1. **Anthropic Claude API Key** (Required)
   - Sign up: https://console.anthropic.com/
   - Get API key from dashboard
   - Free tier available (limited requests)

2. **Hunter.io API Key** (Optional - for email finding)
   - Sign up: https://hunter.io/
   - Free tier: 25 searches/month

3. **GitHub Personal Access Token** (Optional - for enhanced repo access)
   - Generate: https://github.com/settings/tokens
   - Scopes needed: `repo`, `user`

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Shivoo29/Looking-For-Reason.git
cd Looking-For-Reason/jobhack-desktop
```

### 2. Set Up Environment Variables

#### Linux/macOS

Create `~/.bashrc` or `~/.zshrc` additions:

```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
export HUNTER_API_KEY="your-hunter-api-key-here"  # Optional
export GITHUB_TOKEN="your-github-token-here"       # Optional

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

#### Windows (PowerShell)

```powershell
# Set for current session
$env:ANTHROPIC_API_KEY="your-anthropic-api-key-here"
$env:HUNTER_API_KEY="your-hunter-api-key-here"
$env:GITHUB_TOKEN="your-github-token-here"

# Set permanently (run as Administrator)
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your-key", "User")
[System.Environment]::SetEnvironmentVariable("HUNTER_API_KEY", "your-key", "User")
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your-key", "User")
```

#### Alternatively: Configuration File

Create `~/.jobhack/application.conf`:

```hocon
jobhack {
  ai {
    apiKey = "your-anthropic-api-key-here"
  }
}
```

### 3. Build the Project

```bash
# Clean and compile
mvn clean compile

# Run tests (optional)
mvn test

# Package (creates executable JAR)
mvn package
```

### 4. Run the Application

```bash
# Run via Maven
mvn javafx:run

# Or run the JAR directly
java -jar target/jobhack-desktop-1.0.0-SNAPSHOT.jar
```

---

## First Run Setup

### Onboarding Wizard

When you first launch JobHack, you'll go through an onboarding process:

#### Step 1: Basic Information
- Full name
- Email address
- Phone number (optional)

#### Steps 2-6: Essay Questions (20 minutes total)

Answer 5 essay questions (500-1000 words each):

1. **Technical Failure Story**
   - Describe a technical challenge where you failed
   - What did you learn?
   - Be honest - this helps personalization

2. **Problem Solving Motivation**
   - What problems do you want to solve in your next role?
   - Why are these problems important to you?

3. **Proudest Achievement**
   - Walk through your proudest technical achievement
   - Include technical details, challenges, impact

4. **Work Environment Preferences**
   - Describe your ideal work environment
   - Team culture, collaboration style, etc.

5. **Career Goals**
   - What are your career goals for the next 2-5 years?
   - Short-term and long-term aspirations

**Why this matters:**
These essays are stored as vector embeddings and used to:
- Generate personalized resume bullet points
- Answer job application essay questions
- Write cold outreach emails
- Match you to relevant jobs

Take your time - quality here = better results later.

#### Step 7: Connect Accounts

- **LinkedIn URL** (optional)
  - Format: `https://linkedin.com/in/yourprofile`
  - Used for profile data extraction

- **GitHub Username** (required)
  - Format: `yourusername`
  - Used to analyze your repositories
  - Extract tech stack and skills
  - Match projects to job descriptions

#### Step 8: Upload Resume

- Upload your current resume (PDF or DOCX)
- Used as baseline for generating tailored versions
- Parsed to extract experience, education, skills

---

## Configuration

### Application Settings

After first run, you can edit `~/.jobhack/application.conf`:

```hocon
jobhack {
  # AI Configuration
  ai {
    provider = "anthropic"
    model = "claude-3-5-sonnet-20241022"
    apiKey = ""
    maxTokens = 4096
    temperature = 0.7
  }

  # Browser Automation
  automation {
    headless = false              # Set true for headless mode
    antiDetection = true
    randomDelayMin = 2000         # milliseconds
    randomDelayMax = 8000
    typingSpeedWpm = 65
    maxApplicationsPerDay = 50
    pauseAfterApplications = 10
    pauseDurationMin = 5          # minutes
    pauseDurationMax = 15
  }

  # Email Configuration
  email {
    provider = "gmail"
    maxEmailsPerDay = 30
    followUpDelayDays = 5
  }

  # Job Scraping
  scraper {
    platforms = [
      "linkedin",
      "indeed",
      "naukri",
      "glassdoor",
      "angellist"
    ]
    maxJobsPerPlatform = 100
    updateIntervalMinutes = 30
  }

  # Database
  database {
    path = "data/jobhack.db"
    maxConnections = 10
  }
}
```

### Directory Structure

JobHack creates the following directories:

```
~/.jobhack/
├── application.conf      # Configuration file
├── user.properties       # User preferences
├── data/
│   ├── jobhack.db       # SQLite database
│   ├── chromadb/        # Vector embeddings
│   └── resumes/         # Generated resumes
└── logs/
    └── jobhack_YYYY-MM-DD.log
```

---

## Troubleshooting

### Issue: "Anthropic API key not configured"

**Solution:**
1. Check environment variable: `echo $ANTHROPIC_API_KEY`
2. Or check config file: `~/.jobhack/application.conf`
3. Restart application after setting

### Issue: "Chrome WebDriver not found"

**Solution:**
```bash
# WebDriverManager should auto-download, but if it fails:

# Linux
sudo apt install chromium-chromedriver

# macOS
brew install chromedriver

# Windows
# Download from https://chromedriver.chromium.org/
```

### Issue: "JavaFX runtime components are missing"

**Solution:**
```bash
# Make sure you have JavaFX
# If using OpenJDK, JavaFX is separate:

# Ubuntu/Debian
sudo apt install openjfx

# macOS (included in JDK)

# Or use Maven to handle it (already configured in pom.xml)
```

### Issue: Application won't start

**Solution:**
```bash
# Check Java version (must be 17+)
java -version

# Clean and rebuild
mvn clean install

# Check logs
cat ~/.jobhack/logs/jobhack_*.log
```

### Issue: High CPU usage

**Cause:** Browser automation running continuously

**Solution:**
1. Check automation settings in config
2. Ensure `maxApplicationsPerDay` is reasonable
3. Set longer delays: `randomDelayMin`, `randomDelayMax`

---

## Performance Tips

### 1. Headless Mode

For faster automation (no GUI overhead):

```hocon
automation {
  headless = true
}
```

### 2. Reduce Logging

```hocon
logging {
  level = "WARN"  # Instead of INFO or DEBUG
}
```

### 3. Rate Limiting

Prevent account bans:

```hocon
automation {
  maxApplicationsPerDay = 30   # Lower is safer
  pauseAfterApplications = 5
}
```

---

## Next Steps

After setup:

1. **Test Resume Generation**
   - Paste a job description
   - Click "Generate Resume"
   - Review ATS score

2. **Test Job Scraper**
   - Click "Start Job Scraper"
   - Review matched jobs

3. **Test Application**
   - Start with LinkedIn Easy Apply
   - Watch the dashboard

4. **Configure Email Outreach**
   - Set up Gmail OAuth (in settings)
   - Test HR email finder

---

## Getting Help

- **Documentation**: See [README.md](README.md)
- **GitHub Issues**: https://github.com/Shivoo29/Looking-For-Reason/issues
- **Logs**: Check `~/.jobhack/logs/`

---

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Rotate API keys** periodically
4. **Check logs** for any exposure
5. **Backup your data**: `~/.jobhack/data/`

---

**You're all set! Let JobHack automate your job search. 🚀**
