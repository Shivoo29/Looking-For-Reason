package com.jobhack.config;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;

/**
 * Application Configuration Manager
 * Handles all app settings, API keys, and user preferences
 */
@Slf4j
@Getter
public class AppConfig {

    private static AppConfig instance;
    private final Config config;
    private final Path configDir;
    private final Path dataDir;
    private final Path logsDir;
    private final Properties userPrefs;

    private AppConfig() {
        // Setup directories
        String userHome = System.getProperty("user.home");
        this.configDir = Paths.get(userHome, ".jobhack");
        this.dataDir = configDir.resolve("data");
        this.logsDir = configDir.resolve("logs");

        createDirectories();

        // Load configuration
        File configFile = configDir.resolve("application.conf").toFile();
        if (!configFile.exists()) {
            createDefaultConfig(configFile);
        }

        this.config = ConfigFactory.parseFile(configFile)
                .withFallback(ConfigFactory.load());

        // Load user preferences
        this.userPrefs = new Properties();
        loadUserPreferences();

        log.info("Configuration loaded from: {}", configDir);
    }

    public static AppConfig getInstance() {
        if (instance == null) {
            synchronized (AppConfig.class) {
                if (instance == null) {
                    instance = new AppConfig();
                }
            }
        }
        return instance;
    }

    private void createDirectories() {
        try {
            Files.createDirectories(configDir);
            Files.createDirectories(dataDir);
            Files.createDirectories(logsDir);
            Files.createDirectories(dataDir.resolve("resumes"));
            Files.createDirectories(dataDir.resolve("chromadb"));
            log.info("Created configuration directories at: {}", configDir);
        } catch (IOException e) {
            log.error("Failed to create configuration directories", e);
            throw new RuntimeException(e);
        }
    }

    private void createDefaultConfig(File configFile) {
        String defaultConfig = """
            jobhack {
              # Application Settings
              app {
                name = "JobHack Desktop"
                version = "1.0.0"
                firstRun = true
              }

              # AI Configuration
              ai {
                provider = "anthropic"  # anthropic or openai
                model = "claude-3-5-sonnet-20241022"
                apiKey = ""  # Set via environment variable: ANTHROPIC_API_KEY
                maxTokens = 4096
                temperature = 0.7
              }

              # Vector Database
              vectordb {
                type = "chroma"
                host = "localhost"
                port = 8000
                collectionName = "jobhack_user_context"
              }

              # Browser Automation
              automation {
                headless = false
                antiDetection = true
                randomDelayMin = 2000  # milliseconds
                randomDelayMax = 8000
                typingSpeedWpm = 65
                maxApplicationsPerDay = 50
                pauseAfterApplications = 10
                pauseDurationMin = 5  # minutes
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
                platforms = ["linkedin", "indeed", "naukri", "glassdoor", "angellist"]
                maxJobsPerPlatform = 100
                updateIntervalMinutes = 30
              }

              # Analytics
              analytics {
                enableTracking = true
                dashboardUpdateInterval = 5000  # milliseconds
              }

              # Database
              database {
                path = "data/jobhack.db"
                maxConnections = 10
              }

              # Logging
              logging {
                level = "INFO"
                maxFileSize = "10MB"
                maxHistory = 30
              }
            }
            """;

        try {
            Files.writeString(configFile.toPath(), defaultConfig);
            log.info("Created default configuration file: {}", configFile);
        } catch (IOException e) {
            log.error("Failed to create default configuration", e);
            throw new RuntimeException(e);
        }
    }

    private void loadUserPreferences() {
        File prefsFile = configDir.resolve("user.properties").toFile();
        if (prefsFile.exists()) {
            try {
                userPrefs.load(Files.newInputStream(prefsFile.toPath()));
            } catch (IOException e) {
                log.warn("Failed to load user preferences", e);
            }
        }
    }

    public void saveUserPreference(String key, String value) {
        userPrefs.setProperty(key, value);
        File prefsFile = configDir.resolve("user.properties").toFile();
        try (FileWriter writer = new FileWriter(prefsFile)) {
            userPrefs.store(writer, "JobHack User Preferences");
        } catch (IOException e) {
            log.error("Failed to save user preferences", e);
        }
    }

    public String getUserPreference(String key, String defaultValue) {
        return userPrefs.getProperty(key, defaultValue);
    }

    // Convenience methods
    public boolean isFirstRun() {
        return config.getBoolean("jobhack.app.firstRun");
    }

    public void setFirstRun(boolean firstRun) {
        saveUserPreference("firstRun", String.valueOf(firstRun));
    }

    public String getAnthropicApiKey() {
        String envKey = System.getenv("ANTHROPIC_API_KEY");
        if (envKey != null && !envKey.isEmpty()) {
            return envKey;
        }
        return config.getString("jobhack.ai.apiKey");
    }

    public String getAiModel() {
        return config.getString("jobhack.ai.model");
    }

    public int getMaxApplicationsPerDay() {
        return config.getInt("jobhack.automation.maxApplicationsPerDay");
    }

    public boolean isHeadless() {
        return config.getBoolean("jobhack.automation.headless");
    }

    public Path getDatabasePath() {
        return configDir.resolve(config.getString("jobhack.database.path"));
    }

    public Path getChromaDbPath() {
        return dataDir.resolve("chromadb");
    }

    public Path getResumesPath() {
        return dataDir.resolve("resumes");
    }
}
