package com.jobhack.config;

/**
 * Application Constants
 */
public class Constants {

    // Application
    public static final String APP_NAME = "JobHack Desktop";
    public static final String APP_VERSION = "1.0.0";

    // Essay Questions for Onboarding
    public static final String[] ONBOARDING_QUESTIONS = {
        "Describe a technical challenge where you failed. What did you learn? (500-1000 words)",
        "What problems do you want to solve in your next role and why? (500-1000 words)",
        "Walk through your proudest technical achievement in detail (500-1000 words)",
        "Describe your ideal work environment and team culture (500-1000 words)",
        "What are your career goals for the next 2-5 years? (500-1000 words)"
    };

    public static final String[] ESSAY_TYPES = {
        "failure_story",
        "problem_solving",
        "achievement",
        "work_culture",
        "career_goals"
    };

    // Job Application Statuses
    public static final String STATUS_PENDING = "PENDING";
    public static final String STATUS_IN_PROGRESS = "IN_PROGRESS";
    public static final String STATUS_COMPLETED = "COMPLETED";
    public static final String STATUS_CONFIRMED = "CONFIRMED";
    public static final String STATUS_INTERVIEW = "INTERVIEW";
    public static final String STATUS_REJECTED = "REJECTED";
    public static final String STATUS_OFFER = "OFFER";

    // ATS Score Thresholds
    public static final int ATS_SCORE_EXCELLENT = 85;
    public static final int ATS_SCORE_GOOD = 70;
    public static final int ATS_SCORE_FAIR = 50;

    // Job Platforms
    public static final String[] JOB_PLATFORMS = {
        "LinkedIn",
        "Indeed",
        "Naukri.com",
        "Glassdoor",
        "AngelList",
        "Wellfound",
        "Instahyre",
        "Monster"
    };

    // Application Types
    public static final String APP_TYPE_EASY_APPLY = "EASY_APPLY";
    public static final String APP_TYPE_WORKDAY = "WORKDAY";
    public static final String APP_TYPE_GREENHOUSE = "GREENHOUSE";
    public static final String APP_TYPE_LEVER = "LEVER";
    public static final String APP_TYPE_CUSTOM = "CUSTOM";

    // Resume Formats
    public static final String RESUME_FORMAT_PDF = "PDF";
    public static final String RESUME_FORMAT_DOCX = "DOCX";
    public static final String RESUME_FORMAT_TXT = "TXT";

    // Resume Types
    public static final String RESUME_TYPE_SOFTWARE = "SOFTWARE_HEAVY";
    public static final String RESUME_TYPE_HARDWARE = "HARDWARE_HEAVY";
    public static final String RESUME_TYPE_RESEARCH = "RESEARCH_HEAVY";
    public static final String RESUME_TYPE_BALANCED = "BALANCED";

    // Email Templates
    public static final String EMAIL_TO_HIRING_MANAGER = "HIRING_MANAGER";
    public static final String EMAIL_TO_RECRUITER = "RECRUITER";
    public static final String EMAIL_REFERRAL_REQUEST = "REFERRAL_REQUEST";
    public static final String EMAIL_FOLLOW_UP = "FOLLOW_UP";

    // API Endpoints
    public static final String HUNTER_IO_API = "https://api.hunter.io/v2";
    public static final String GITHUB_API = "https://api.github.com";
    public static final String LINKEDIN_API = "https://api.linkedin.com/v2";

    // UI Colors (Neo-Brutalist Theme)
    public static final String COLOR_BACKGROUND = "#000000";
    public static final String COLOR_FOREGROUND = "#FFFFFF";
    public static final String COLOR_ACCENT = "#00FF00";
    public static final String COLOR_WARNING = "#FFFF00";
    public static final String COLOR_ERROR = "#FF0000";
    public static final String COLOR_SUCCESS = "#00FF00";
    public static final String COLOR_INFO = "#00FFFF";

    // Logging
    public static final String LOG_FORMAT = "[%s] %s %s";

    // Browser User Agents (for rotation)
    public static final String[] USER_AGENTS = {
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    };

    private Constants() {
        // Prevent instantiation
    }
}
