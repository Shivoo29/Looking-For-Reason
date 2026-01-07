package com.jobhack.automation;

import com.jobhack.config.AppConfig;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Point;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;

import java.util.Random;

/**
 * Anti-Detection Features
 * Human-like behavior simulation to avoid bot detection
 */
@Slf4j
public class AntiDetection {

    private final WebDriver driver;
    private final Random random;
    private final AppConfig config;
    private final Actions actions;

    public AntiDetection(WebDriver driver) {
        this.driver = driver;
        this.random = new Random();
        this.config = AppConfig.getInstance();
        this.actions = new Actions(driver);
    }

    /**
     * Type text with human-like speed and occasional typos
     */
    public void typeHumanLike(WebElement element, String text) {
        log.debug("Typing text: {}", text);

        element.click();
        shortDelay();

        // Get configured WPM (words per minute)
        int wpm = config.getConfig().getInt("jobhack.automation.typingSpeedWpm");
        int avgCharDelay = (60 * 1000) / (wpm * 5); // Assuming avg 5 chars per word

        for (char c : text.toCharArray()) {
            // Simulate occasional thinking pauses
            if (random.nextDouble() < 0.05) { // 5% chance
                delay(300, 1000); // Longer pause
            }

            element.sendKeys(String.valueOf(c));

            // Variable typing speed
            int charDelay = avgCharDelay + random.nextInt(50) - 25;
            try {
                Thread.sleep(Math.max(50, charDelay));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        shortDelay();
    }

    /**
     * Click with mouse movement simulation
     */
    public void clickHumanLike(WebElement element) {
        log.debug("Clicking element: {}", element.getTagName());

        // Move to element with slight randomness
        Point location = element.getLocation();
        int xOffset = random.nextInt(element.getSize().getWidth()) - element.getSize().getWidth() / 2;
        int yOffset = random.nextInt(element.getSize().getHeight()) - element.getSize().getHeight() / 2;

        actions.moveToElement(element, xOffset, yOffset).perform();
        shortDelay();

        element.click();
        shortDelay();
    }

    /**
     * Scroll page gradually (human-like)
     */
    public void scrollGradually(int targetY) {
        JavascriptExecutor js = (JavascriptExecutor) driver;
        Long currentY = (Long) js.executeScript("return window.pageYOffset;");

        int steps = 10 + random.nextInt(10);
        int stepSize = (int) ((targetY - currentY) / steps);

        for (int i = 0; i < steps; i++) {
            long scrollTo = currentY + (stepSize * i);
            js.executeScript("window.scrollTo(0, " + scrollTo + ");");
            delay(50, 150);
        }

        js.executeScript("window.scrollTo(0, " + targetY + ");");
    }

    /**
     * Random mouse movements (looks human)
     */
    public void randomMouseMovement() {
        int moves = 2 + random.nextInt(4);
        for (int i = 0; i < moves; i++) {
            int x = random.nextInt(200) - 100;
            int y = random.nextInt(200) - 100;
            actions.moveByOffset(x, y).perform();
            delay(100, 300);
        }
    }

    /**
     * Read content (simulate reading time based on text length)
     */
    public void simulateReading(String text) {
        // Average reading speed: 250 words per minute
        int wordCount = text.split("\\s+").length;
        int readingTimeMs = (wordCount * 60 * 1000) / 250;

        // Add randomness (people read at different speeds)
        readingTimeMs = (int) (readingTimeMs * (0.8 + random.nextDouble() * 0.4));

        // Cap at reasonable max (30 seconds)
        readingTimeMs = Math.min(readingTimeMs, 30000);

        log.debug("Simulating reading time: {} ms for {} words", readingTimeMs, wordCount);

        try {
            Thread.sleep(readingTimeMs);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Detect if CAPTCHA is present
     */
    public boolean isCaptchaPresent() {
        JavascriptExecutor js = (JavascriptExecutor) driver;

        // Check for common CAPTCHA indicators
        String[] captchaSelectors = {
            "iframe[src*='recaptcha']",
            "iframe[src*='hcaptcha']",
            ".g-recaptcha",
            "#captcha",
            "[class*='captcha']"
        };

        for (String selector : captchaSelectors) {
            try {
                Object result = js.executeScript(
                    "return document.querySelector('" + selector + "') !== null;"
                );
                if (Boolean.TRUE.equals(result)) {
                    log.warn("CAPTCHA detected: {}", selector);
                    return true;
                }
            } catch (Exception e) {
                // Ignore
            }
        }

        return false;
    }

    /**
     * Wait for CAPTCHA to be solved manually
     */
    public void waitForCaptchaSolution(int maxWaitSeconds) {
        log.warn("Waiting for CAPTCHA to be solved manually...");

        int waited = 0;
        while (isCaptchaPresent() && waited < maxWaitSeconds) {
            try {
                Thread.sleep(2000);
                waited += 2;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        if (!isCaptchaPresent()) {
            log.info("CAPTCHA solved!");
        } else {
            log.warn("CAPTCHA still present after {} seconds", waited);
        }
    }

    /**
     * Random delay
     */
    private void delay(int minMs, int maxMs) {
        int delay = minMs + random.nextInt(maxMs - minMs);
        try {
            Thread.sleep(delay);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Short delay
     */
    private void shortDelay() {
        delay(200, 800);
    }
}
