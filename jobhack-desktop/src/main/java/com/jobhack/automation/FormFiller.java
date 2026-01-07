package com.jobhack.automation;

import com.jobhack.database.models.User;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;

import java.util.List;
import java.util.Map;

/**
 * Form Filler
 * Intelligently fills web forms using user data
 */
@Slf4j
public class FormFiller {

    private final WebDriver driver;
    private final AntiDetection antiDetection;

    public FormFiller(WebDriver driver) {
        this.driver = driver;
        this.antiDetection = new AntiDetection(driver);
    }

    /**
     * Fill a text input field
     */
    public void fillTextField(WebElement element, String value) {
        if (value == null || value.isEmpty()) {
            return;
        }

        try {
            element.clear();
            antiDetection.typeHumanLike(element, value);
            log.debug("Filled text field with: {}", value);
        } catch (Exception e) {
            log.error("Failed to fill text field", e);
        }
    }

    /**
     * Fill dropdown/select field
     */
    public void fillDropdown(WebElement element, String value) {
        if (value == null || value.isEmpty()) {
            return;
        }

        try {
            Select select = new Select(element);

            // Try to select by visible text first
            try {
                select.selectByVisibleText(value);
                log.debug("Selected dropdown option: {}", value);
                return;
            } catch (Exception e) {
                // Try partial match
                List<WebElement> options = select.getOptions();
                for (WebElement option : options) {
                    if (option.getText().toLowerCase().contains(value.toLowerCase())) {
                        option.click();
                        log.debug("Selected dropdown option (partial match): {}", option.getText());
                        return;
                    }
                }
            }

            log.warn("Could not find matching option for: {}", value);
        } catch (Exception e) {
            log.error("Failed to fill dropdown", e);
        }
    }

    /**
     * Fill checkbox
     */
    public void fillCheckbox(WebElement element, boolean check) {
        try {
            if (element.isSelected() != check) {
                antiDetection.clickHumanLike(element);
                log.debug("Set checkbox to: {}", check);
            }
        } catch (Exception e) {
            log.error("Failed to fill checkbox", e);
        }
    }

    /**
     * Auto-fill form based on field detection
     */
    public void autoFillForm(Map<String, String> userData) {
        log.info("Auto-filling form with user data");

        List<WebElement> inputs = driver.findElements(By.tagName("input"));
        List<WebElement> textareas = driver.findElements(By.tagName("textarea"));
        List<WebElement> selects = driver.findElements(By.tagName("select"));

        // Fill text inputs
        for (WebElement input : inputs) {
            try {
                String type = input.getAttribute("type");
                String name = input.getAttribute("name");
                String id = input.getAttribute("id");
                String placeholder = input.getAttribute("placeholder");
                String label = findLabelForInput(input);

                String fieldIdentifier = (name + " " + id + " " + placeholder + " " + label).toLowerCase();

                if ("text".equals(type) || "email".equals(type) || type == null) {
                    if (fieldIdentifier.contains("name") && !fieldIdentifier.contains("company")) {
                        fillTextField(input, userData.get("name"));
                    } else if (fieldIdentifier.contains("email")) {
                        fillTextField(input, userData.get("email"));
                    } else if (fieldIdentifier.contains("phone")) {
                        fillTextField(input, userData.get("phone"));
                    } else if (fieldIdentifier.contains("linkedin")) {
                        fillTextField(input, userData.get("linkedin"));
                    } else if (fieldIdentifier.contains("github")) {
                        fillTextField(input, userData.get("github"));
                    }
                }
            } catch (Exception e) {
                log.debug("Skipping input field due to error: {}", e.getMessage());
            }
        }

        // Fill textareas (usually for longer responses)
        for (WebElement textarea : textareas) {
            try {
                String name = textarea.getAttribute("name");
                String id = textarea.getAttribute("id");
                String label = findLabelForInput(textarea);

                String fieldIdentifier = (name + " " + id + " " + label).toLowerCase();

                // These would typically be filled using AI-generated content
                log.debug("Found textarea: {}", fieldIdentifier);
            } catch (Exception e) {
                log.debug("Skipping textarea due to error: {}", e.getMessage());
            }
        }

        log.info("Form auto-fill completed");
    }

    /**
     * Find label text for an input element
     */
    private String findLabelForInput(WebElement input) {
        try {
            String id = input.getAttribute("id");
            if (id != null && !id.isEmpty()) {
                List<WebElement> labels = driver.findElements(By.cssSelector("label[for='" + id + "']"));
                if (!labels.isEmpty()) {
                    return labels.get(0).getText();
                }
            }

            // Look for parent label
            WebElement parent = input.findElement(By.xpath(".."));
            if ("label".equalsIgnoreCase(parent.getTagName())) {
                return parent.getText();
            }
        } catch (Exception e) {
            // Ignore
        }

        return "";
    }

    /**
     * Detect if element is visible and interactable
     */
    public boolean isInteractable(WebElement element) {
        try {
            return element.isDisplayed() && element.isEnabled();
        } catch (Exception e) {
            return false;
        }
    }
}
