package com.jobhack;

import com.jobhack.config.AppConfig;
import com.jobhack.database.DatabaseManager;
import com.jobhack.gui.MainWindow;
import com.jobhack.gui.OnboardingWizard;
import javafx.application.Application;
import javafx.stage.Stage;
import lombok.extern.slf4j.Slf4j;

/**
 * JobHack Desktop Application
 * AI-Powered Job Application Automation Platform
 *
 * This is NOT just another auto-apply tool. It's a full job-hunting operating system.
 */
@Slf4j
public class JobHackApplication extends Application {

    private AppConfig config;
    private DatabaseManager databaseManager;

    public static void main(String[] args) {
        log.info("╔════════════════════════════════════════════════════════════╗");
        log.info("║                      JOBHACK DESKTOP                       ║");
        log.info("║        AI-Powered Job Application Automation Platform      ║");
        log.info("║                    Brutally Effective.                     ║");
        log.info("╚════════════════════════════════════════════════════════════╝");

        launch(args);
    }

    @Override
    public void init() throws Exception {
        log.info("Initializing JobHack...");

        // Load configuration
        config = AppConfig.getInstance();
        log.info("✓ Configuration loaded");

        // Initialize database
        databaseManager = DatabaseManager.getInstance();
        databaseManager.initialize();
        log.info("✓ Database initialized");

        // Additional initialization
        log.info("✓ Initialization complete");
    }

    @Override
    public void start(Stage primaryStage) {
        try {
            log.info("Starting GUI...");

            // Check if user needs onboarding
            if (config.isFirstRun()) {
                log.info("First run detected - launching onboarding wizard");
                OnboardingWizard wizard = new OnboardingWizard();
                wizard.show(primaryStage, () -> {
                    // After onboarding, show main window
                    config.setFirstRun(false);
                    showMainWindow(primaryStage);
                });
            } else {
                // Show main window directly
                showMainWindow(primaryStage);
            }

        } catch (Exception e) {
            log.error("Failed to start application", e);
            System.exit(1);
        }
    }

    private void showMainWindow(Stage stage) {
        MainWindow mainWindow = new MainWindow();
        mainWindow.show(stage);
        log.info("✓ Main window displayed");
    }

    @Override
    public void stop() throws Exception {
        log.info("Shutting down JobHack...");

        // Cleanup resources
        if (databaseManager != null) {
            databaseManager.shutdown();
        }

        log.info("✓ Shutdown complete");
    }
}
