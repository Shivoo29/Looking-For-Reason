package com.jobhack.gui;

import com.jobhack.config.Constants;
import com.jobhack.database.DatabaseManager;
import com.jobhack.database.models.User;
import com.jobhack.utils.ActivityLogger;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import lombok.extern.slf4j.Slf4j;

import java.io.File;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

/**
 * Onboarding Wizard - Deep User Profiling
 * Collects MIT-admissions-style essay responses and credentials
 */
@Slf4j
public class OnboardingWizard {

    private final DatabaseManager databaseManager;
    private final ActivityLogger activityLogger;
    private int currentStep = 0;
    private final List<String> essayResponses = new ArrayList<>();

    // User data
    private String userName;
    private String userEmail;
    private String userPhone;
    private String linkedinUrl;
    private String githubUsername;
    private String resumePath;

    public OnboardingWizard() {
        this.databaseManager = DatabaseManager.getInstance();
        this.activityLogger = ActivityLogger.getInstance();

        // Initialize essay responses
        for (int i = 0; i < Constants.ONBOARDING_QUESTIONS.length; i++) {
            essayResponses.add("");
        }
    }

    public void show(Stage stage, Runnable onComplete) {
        stage.setTitle("JobHack Onboarding - Deep Profiling");

        VBox root = createWelcomeScreen(() -> {
            showNextStep(stage, onComplete);
        });

        Scene scene = new Scene(root, 1000, 700);
        scene.getStylesheets().add(
            getClass().getResource("/css/neo-brutalist.css").toExternalForm()
        );

        stage.setScene(scene);
        stage.show();
    }

    private VBox createWelcomeScreen(Runnable onNext) {
        VBox root = new VBox(30);
        root.setAlignment(Pos.CENTER);
        root.setPadding(new Insets(50));
        root.getStyleClass().add("root");

        Label title = new Label("WELCOME TO JOBHACK");
        title.getStyleClass().add("header");
        title.setStyle("-fx-font-size: 36px;");

        Label subtitle = new Label("This is NOT just another auto-apply tool.");
        subtitle.getStyleClass().add("label");
        subtitle.setStyle("-fx-font-size: 18px;");

        Label description = new Label(
            "JobHack is a full job-hunting operating system that will:\n\n" +
            "• Deeply understand your technical background and career goals\n" +
            "• Generate ATS-optimized resumes tailored to each job\n" +
            "• Automate applications across multiple platforms\n" +
            "• Find and contact hiring managers directly\n" +
            "• Track everything in a brutally honest dashboard\n\n" +
            "To do this effectively, we need to know YOU.\n" +
            "The next 20 minutes will be the most important investment in your job search."
        );
        description.getStyleClass().add("label");
        description.setWrapText(true);
        description.setMaxWidth(700);
        description.setStyle("-fx-font-size: 14px; -fx-text-alignment: center;");

        Button startBtn = new Button("LET'S BEGIN");
        startBtn.getStyleClass().add("button-primary");
        startBtn.setStyle("-fx-font-size: 18px; -fx-padding: 15px 40px;");
        startBtn.setOnAction(e -> onNext.run());

        root.getChildren().addAll(title, subtitle, description, startBtn);
        return root;
    }

    private void showNextStep(Stage stage, Runnable onComplete) {
        currentStep++;

        if (currentStep == 1) {
            showBasicInfoStep(stage, onComplete);
        } else if (currentStep >= 2 && currentStep <= 6) {
            showEssayStep(stage, currentStep - 2, onComplete);
        } else if (currentStep == 7) {
            showCredentialsStep(stage, onComplete);
        } else if (currentStep == 8) {
            showResumeUploadStep(stage, onComplete);
        } else {
            completeOnboarding(stage, onComplete);
        }
    }

    private void showBasicInfoStep(Stage stage, Runnable onComplete) {
        VBox root = createStepContainer("STEP 1/8: BASIC INFORMATION");

        GridPane form = new GridPane();
        form.setHgap(15);
        form.setVgap(15);
        form.setPadding(new Insets(20));
        form.setMaxWidth(600);

        // Name
        Label nameLabel = new Label("Full Name:*");
        nameLabel.getStyleClass().add("label");
        TextField nameField = new TextField();
        nameField.getStyleClass().add("text-field");

        // Email
        Label emailLabel = new Label("Email:*");
        emailLabel.getStyleClass().add("label");
        TextField emailField = new TextField();
        emailField.getStyleClass().add("text-field");

        // Phone
        Label phoneLabel = new Label("Phone:");
        phoneLabel.getStyleClass().add("label");
        TextField phoneField = new TextField();
        phoneField.getStyleClass().add("text-field");

        form.add(nameLabel, 0, 0);
        form.add(nameField, 1, 0);
        form.add(emailLabel, 0, 1);
        form.add(emailField, 1, 1);
        form.add(phoneLabel, 0, 2);
        form.add(phoneField, 1, 2);

        Button nextBtn = createNextButton(() -> {
            if (nameField.getText().isEmpty() || emailField.getText().isEmpty()) {
                showAlert("Please fill in required fields (marked with *)");
                return;
            }

            userName = nameField.getText();
            userEmail = emailField.getText();
            userPhone = phoneField.getText();

            showNextStep(stage, onComplete);
        });

        root.getChildren().addAll(form, nextBtn);
        stage.getScene().setRoot(root);
    }

    private void showEssayStep(Stage stage, int essayIndex, Runnable onComplete) {
        VBox root = createStepContainer(String.format("STEP %d/8: ESSAY QUESTION", essayIndex + 2));

        Label instruction = new Label("Take your time. Write 500-1000 words. This helps us understand YOU.");
        instruction.getStyleClass().add("label-info");
        instruction.setStyle("-fx-font-size: 14px;");
        instruction.setWrapText(true);

        Label question = new Label(Constants.ONBOARDING_QUESTIONS[essayIndex]);
        question.getStyleClass().add("sub-header");
        question.setWrapText(true);
        question.setMaxWidth(900);
        question.setStyle("-fx-font-size: 16px; -fx-padding: 20px 0;");

        TextArea essayArea = new TextArea();
        essayArea.getStyleClass().add("text-area");
        essayArea.setWrapText(true);
        essayArea.setPrefRowCount(15);
        essayArea.setText(essayResponses.get(essayIndex));

        // Word count
        Label wordCountLabel = new Label("Words: 0");
        wordCountLabel.getStyleClass().add("label");
        essayArea.textProperty().addListener((obs, old, newText) -> {
            int wordCount = newText.trim().isEmpty() ? 0 : newText.trim().split("\\s+").length;
            wordCountLabel.setText("Words: " + wordCount);
            if (wordCount < 500) {
                wordCountLabel.setStyle("-fx-text-fill: #FF0000;");
            } else if (wordCount > 1000) {
                wordCountLabel.setStyle("-fx-text-fill: #FFFF00;");
            } else {
                wordCountLabel.setStyle("-fx-text-fill: #00FF00;");
            }
        });

        HBox buttons = new HBox(15);
        buttons.setAlignment(Pos.CENTER);

        Button backBtn = createBackButton(() -> {
            essayResponses.set(essayIndex, essayArea.getText());
            currentStep -= 2;
            showNextStep(stage, onComplete);
        });

        Button nextBtn = createNextButton(() -> {
            int wordCount = essayArea.getText().trim().isEmpty() ? 0 :
                essayArea.getText().trim().split("\\s+").length;

            if (wordCount < 500) {
                showAlert("Please write at least 500 words. This is crucial for personalization.");
                return;
            }

            essayResponses.set(essayIndex, essayArea.getText());
            showNextStep(stage, onComplete);
        });

        buttons.getChildren().addAll(backBtn, nextBtn);

        root.getChildren().addAll(instruction, question, essayArea, wordCountLabel, buttons);
        stage.getScene().setRoot(root);
    }

    private void showCredentialsStep(Stage stage, Runnable onComplete) {
        VBox root = createStepContainer("STEP 7/8: CONNECT ACCOUNTS");

        Label instruction = new Label("Connect your accounts for deep integration:");
        instruction.getStyleClass().add("label");
        instruction.setStyle("-fx-font-size: 16px;");

        GridPane form = new GridPane();
        form.setHgap(15);
        form.setVgap(15);
        form.setPadding(new Insets(20));
        form.setMaxWidth(600);

        // LinkedIn
        Label linkedinLabel = new Label("LinkedIn URL:");
        linkedinLabel.getStyleClass().add("label");
        TextField linkedinField = new TextField();
        linkedinField.getStyleClass().add("text-field");
        linkedinField.setPromptText("https://linkedin.com/in/yourprofile");

        // GitHub
        Label githubLabel = new Label("GitHub Username:*");
        githubLabel.getStyleClass().add("label");
        TextField githubField = new TextField();
        githubField.getStyleClass().add("text-field");
        githubField.setPromptText("yourusername");

        form.add(linkedinLabel, 0, 0);
        form.add(linkedinField, 1, 0);
        form.add(githubLabel, 0, 1);
        form.add(githubField, 1, 1);

        Label note = new Label(
            "Note: Gmail OAuth will be configured later in settings.\n" +
            "GitHub is required for skills extraction and project analysis."
        );
        note.getStyleClass().add("label-info");
        note.setWrapText(true);
        note.setStyle("-fx-font-size: 12px;");

        HBox buttons = new HBox(15);
        buttons.setAlignment(Pos.CENTER);

        Button backBtn = createBackButton(() -> {
            currentStep -= 2;
            showNextStep(stage, onComplete);
        });

        Button nextBtn = createNextButton(() -> {
            if (githubField.getText().isEmpty()) {
                showAlert("GitHub username is required for skills extraction");
                return;
            }

            linkedinUrl = linkedinField.getText();
            githubUsername = githubField.getText();

            showNextStep(stage, onComplete);
        });

        buttons.getChildren().addAll(backBtn, nextBtn);

        root.getChildren().addAll(instruction, form, note, buttons);
        stage.getScene().setRoot(root);
    }

    private void showResumeUploadStep(Stage stage, Runnable onComplete) {
        VBox root = createStepContainer("STEP 8/8: UPLOAD CURRENT RESUME");

        Label instruction = new Label("Upload your current resume (PDF or DOCX):");
        instruction.getStyleClass().add("label");
        instruction.setStyle("-fx-font-size: 16px;");

        Label selectedFile = new Label("No file selected");
        selectedFile.getStyleClass().add("label-info");

        Button uploadBtn = new Button("CHOOSE FILE");
        uploadBtn.getStyleClass().add("button");
        uploadBtn.setOnAction(e -> {
            FileChooser fileChooser = new FileChooser();
            fileChooser.setTitle("Select Resume");
            fileChooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("PDF Files", "*.pdf"),
                new FileChooser.ExtensionFilter("Word Documents", "*.docx")
            );

            File file = fileChooser.showOpenDialog(stage);
            if (file != null) {
                resumePath = file.getAbsolutePath();
                selectedFile.setText("Selected: " + file.getName());
            }
        });

        Label note = new Label(
            "We'll parse your resume to extract your experience, education, and skills.\n" +
            "This will be used as the baseline for generating tailored resumes."
        );
        note.getStyleClass().add("label-info");
        note.setWrapText(true);
        note.setStyle("-fx-font-size: 12px;");

        HBox buttons = new HBox(15);
        buttons.setAlignment(Pos.CENTER);

        Button backBtn = createBackButton(() -> {
            currentStep -= 2;
            showNextStep(stage, onComplete);
        });

        Button finishBtn = new Button("COMPLETE ONBOARDING");
        finishBtn.getStyleClass().add("button-primary");
        finishBtn.setStyle("-fx-font-size: 16px; -fx-padding: 15px 30px;");
        finishBtn.setOnAction(e -> {
            showNextStep(stage, onComplete);
        });

        buttons.getChildren().addAll(backBtn, finishBtn);

        root.getChildren().addAll(instruction, uploadBtn, selectedFile, note, buttons);
        stage.getScene().setRoot(root);
    }

    private void completeOnboarding(Stage stage, Runnable onComplete) {
        // Save to database
        try {
            saveUserData();
            saveEssays();

            activityLogger.log("Onboarding completed successfully", ActivityLogger.LogLevel.SUCCESS);
            log.info("User onboarding completed: {}", userEmail);

            // Close wizard and run completion callback
            stage.close();
            onComplete.run();

        } catch (Exception e) {
            log.error("Failed to complete onboarding", e);
            showAlert("Error saving data: " + e.getMessage());
        }
    }

    private void saveUserData() throws Exception {
        try (Connection conn = databaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "INSERT INTO users (name, email, phone, linkedin_url, github_username, current_resume_path, onboarding_completed) " +
                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                 PreparedStatement.RETURN_GENERATED_KEYS)) {

            stmt.setString(1, userName);
            stmt.setString(2, userEmail);
            stmt.setString(3, userPhone);
            stmt.setString(4, linkedinUrl);
            stmt.setString(5, githubUsername);
            stmt.setString(6, resumePath);
            stmt.setBoolean(7, true);

            stmt.executeUpdate();

            // Get generated user ID
            ResultSet rs = stmt.getGeneratedKeys();
            if (rs.next()) {
                long userId = rs.getLong(1);
                log.info("User created with ID: {}", userId);
            }
        }
    }

    private void saveEssays() throws Exception {
        // Get user ID
        Long userId = getUserId();

        try (Connection conn = databaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "INSERT INTO essays (user_id, essay_type, content, word_count) VALUES (?, ?, ?, ?)")) {

            for (int i = 0; i < essayResponses.size(); i++) {
                String essay = essayResponses.get(i);
                int wordCount = essay.trim().isEmpty() ? 0 : essay.trim().split("\\s+").length;

                stmt.setLong(1, userId);
                stmt.setString(2, Constants.ESSAY_TYPES[i]);
                stmt.setString(3, essay);
                stmt.setInt(4, wordCount);

                stmt.executeUpdate();
            }

            log.info("Saved {} essays for user {}", essayResponses.size(), userId);
        }
    }

    private Long getUserId() throws Exception {
        try (Connection conn = databaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement("SELECT id FROM users WHERE email = ?")) {

            stmt.setString(1, userEmail);
            ResultSet rs = stmt.executeQuery();

            if (rs.next()) {
                return rs.getLong("id");
            }
        }
        throw new Exception("User not found");
    }

    private VBox createStepContainer(String title) {
        VBox root = new VBox(20);
        root.setAlignment(Pos.TOP_CENTER);
        root.setPadding(new Insets(30));
        root.getStyleClass().add("root");

        Label header = new Label(title);
        header.getStyleClass().add("header");

        root.getChildren().add(header);
        return root;
    }

    private Button createNextButton(Runnable action) {
        Button btn = new Button("NEXT →");
        btn.getStyleClass().add("button-primary");
        btn.setStyle("-fx-font-size: 16px; -fx-padding: 12px 30px;");
        btn.setOnAction(e -> action.run());
        return btn;
    }

    private Button createBackButton(Runnable action) {
        Button btn = new Button("← BACK");
        btn.getStyleClass().add("button");
        btn.setStyle("-fx-font-size: 16px; -fx-padding: 12px 30px;");
        btn.setOnAction(e -> action.run());
        return btn;
    }

    private void showAlert(String message) {
        Alert alert = new Alert(Alert.AlertType.WARNING);
        alert.setTitle("JobHack");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}
