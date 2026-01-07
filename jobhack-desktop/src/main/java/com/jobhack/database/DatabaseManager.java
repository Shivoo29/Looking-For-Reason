package com.jobhack.database;

import com.jobhack.config.AppConfig;
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;

import java.nio.file.Files;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Database Manager - Handles SQLite database connections and schema
 */
@Slf4j
public class DatabaseManager {

    private static DatabaseManager instance;
    private HikariDataSource dataSource;

    private DatabaseManager() {}

    public static DatabaseManager getInstance() {
        if (instance == null) {
            synchronized (DatabaseManager.class) {
                if (instance == null) {
                    instance = new DatabaseManager();
                }
            }
        }
        return instance;
    }

    public void initialize() {
        try {
            AppConfig config = AppConfig.getInstance();
            String dbPath = config.getDatabasePath().toString();

            // Create parent directory if needed
            Files.createDirectories(config.getDatabasePath().getParent());

            // Setup HikariCP connection pool
            HikariConfig hikariConfig = new HikariConfig();
            hikariConfig.setJdbcUrl("jdbc:sqlite:" + dbPath);
            hikariConfig.setMaximumPoolSize(10);
            hikariConfig.setConnectionTimeout(30000);

            dataSource = new HikariDataSource(hikariConfig);

            // Create schema
            createSchema();

            log.info("Database initialized at: {}", dbPath);
        } catch (Exception e) {
            log.error("Failed to initialize database", e);
            throw new RuntimeException(e);
        }
    }

    private void createSchema() throws SQLException {
        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {

            // Users table
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    linkedin_url TEXT,
                    github_username TEXT,
                    current_resume_path TEXT,
                    onboarding_completed BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """);

            // Essays table (onboarding responses)
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS essays (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    essay_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    word_count INTEGER,
                    embedding_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """);

            // GitHub repositories
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS github_repos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    repo_name TEXT NOT NULL,
                    repo_url TEXT NOT NULL,
                    description TEXT,
                    languages TEXT,
                    topics TEXT,
                    stars INTEGER DEFAULT 0,
                    forks INTEGER DEFAULT 0,
                    last_updated TIMESTAMP,
                    skills_extracted TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """);

            // Skills inventory
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    skill_name TEXT NOT NULL,
                    proficiency REAL DEFAULT 0.0,
                    projects TEXT,
                    lines_of_code INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE(user_id, skill_name)
                )
                """);

            // Job applications
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    job_url TEXT,
                    platform TEXT,
                    job_description TEXT,
                    application_type TEXT,
                    status TEXT DEFAULT 'PENDING',
                    ats_score INTEGER,
                    resume_path TEXT,
                    cover_letter_path TEXT,
                    applied_at TIMESTAMP,
                    confirmed_at TIMESTAMP,
                    rejection_reason TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """);

            // Resumes
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS resumes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    resume_type TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    format TEXT NOT NULL,
                    ats_score INTEGER,
                    tailored_for_job_id INTEGER,
                    projects_included TEXT,
                    keywords TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (tailored_for_job_id) REFERENCES applications(id)
                )
                """);

            // Contacts (HR, recruiters, hiring managers)
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    name TEXT NOT NULL,
                    title TEXT,
                    email TEXT,
                    linkedin_url TEXT,
                    confidence_score REAL DEFAULT 0.0,
                    found_via TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(company, email)
                )
                """);

            // Outreach emails
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS outreach_emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    contact_id INTEGER NOT NULL,
                    email_type TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    body TEXT NOT NULL,
                    sent_at TIMESTAMP,
                    opened_at TIMESTAMP,
                    replied_at TIMESTAMP,
                    reply_sentiment TEXT,
                    follow_up_sent BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (application_id) REFERENCES applications(id),
                    FOREIGN KEY (contact_id) REFERENCES contacts(id)
                )
                """);

            // Activity log (for dashboard feed)
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """);

            // API credentials (encrypted)
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT UNIQUE NOT NULL,
                    encrypted_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """);

            // Application checkpoints (for crash recovery)
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS application_checkpoints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    application_id INTEGER NOT NULL,
                    page_number INTEGER NOT NULL,
                    form_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (application_id) REFERENCES applications(id)
                )
                """);

            log.info("Database schema created successfully");
        }
    }

    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }

    public void shutdown() {
        if (dataSource != null && !dataSource.isClosed()) {
            dataSource.close();
            log.info("Database connection pool closed");
        }
    }
}
