package com.jobhack.automation;

import com.jobhack.config.AppConfig;
import com.jobhack.config.Constants;
import io.github.bonigarcia.wdm.WebDriverManager;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * Browser Manager
 * Manages Selenium WebDriver with anti-detection features
 */
@Slf4j
public class BrowserManager {

    private static BrowserManager instance;
    private WebDriver driver;
    private final AppConfig config;
    private final Random random;
    private int currentUserAgentIndex = 0;

    private BrowserManager() {
        this.config = AppConfig.getInstance();
        this.random = new Random();
    }

    public static BrowserManager getInstance() {
        if (instance == null) {
            synchronized (BrowserManager.class) {
                if (instance == null) {
                    instance = new BrowserManager();
                }
            }
        }
        return instance;
    }

    /**
     * Initialize browser with anti-detection measures
     */
    public void initialize() {
        if (driver != null) {
            log.warn("Browser already initialized");
            return;
        }

        log.info("Initializing browser with anti-detection features...");

        // Setup ChromeDriver
        WebDriverManager.chromedriver().setup();

        ChromeOptions options = new ChromeOptions();

        // Anti-detection measures
        options.addArguments("--disable-blink-features=AutomationControlled");
        options.setExperimentalOption("excludeSwitches", new String[]{"enable-automation"});
        options.setExperimentalOption("useAutomationExtension", false);

        // Set user agent (rotate through list)
        String userAgent = Constants.USER_AGENTS[currentUserAgentIndex];
        options.addArguments("user-agent=" + userAgent);
        currentUserAgentIndex = (currentUserAgentIndex + 1) % Constants.USER_AGENTS.length;
        log.info("Using user agent: {}", userAgent);

        // Window size randomization
        int width = 1920 + random.nextInt(100) - 50;
        int height = 1080 + random.nextInt(100) - 50;
        options.addArguments(String.format("--window-size=%d,%d", width, height));

        // Additional options
        if (config.isHeadless()) {
            options.addArguments("--headless=new");
        }

        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-gpu");
        options.addArguments("--disable-notifications");
        options.addArguments("--disable-popup-blocking");

        // Disable image loading for faster scraping (optional)
        Map<String, Object> prefs = new HashMap<>();
        // prefs.put("profile.managed_default_content_settings.images", 2);
        options.setExperimentalOption("prefs", prefs);

        driver = new ChromeDriver(options);

        // Execute CDP commands to hide webdriver property
        Map<String, Object> params = new HashMap<>();
        params.put("source", """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """);

        try {
            ((ChromeDriver) driver).executeCdpCommand("Page.addScriptToEvaluateOnNewDocument", params);
        } catch (Exception e) {
            log.warn("Could not execute CDP command: {}", e.getMessage());
        }

        log.info("Browser initialized successfully");
    }

    /**
     * Get the WebDriver instance
     */
    public WebDriver getDriver() {
        if (driver == null) {
            initialize();
        }
        return driver;
    }

    /**
     * Navigate to URL with random delay
     */
    public void navigateTo(String url) {
        log.info("Navigating to: {}", url);
        randomDelay();
        getDriver().get(url);
    }

    /**
     * Random delay to mimic human behavior
     */
    public void randomDelay() {
        int minDelay = config.getConfig().getInt("jobhack.automation.randomDelayMin");
        int maxDelay = config.getConfig().getInt("jobhack.automation.randomDelayMax");
        int delay = minDelay + random.nextInt(maxDelay - minDelay);

        try {
            Thread.sleep(delay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.warn("Delay interrupted", e);
        }
    }

    /**
     * Short random delay (for between actions)
     */
    public void shortDelay() {
        int delay = 500 + random.nextInt(1500); // 0.5-2 seconds
        try {
            Thread.sleep(delay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Clear cookies and cache
     */
    public void clearCookies() {
        if (driver != null) {
            driver.manage().deleteAllCookies();
            log.info("Cookies cleared");
        }
    }

    /**
     * Restart browser (for long-running sessions)
     */
    public void restart() {
        log.info("Restarting browser...");
        shutdown();
        initialize();
    }

    /**
     * Shutdown browser
     */
    public void shutdown() {
        if (driver != null) {
            try {
                driver.quit();
                log.info("Browser shut down successfully");
            } catch (Exception e) {
                log.error("Error shutting down browser", e);
            } finally {
                driver = null;
            }
        }
    }

    /**
     * Check if browser is running
     */
    public boolean isRunning() {
        return driver != null;
    }
}
