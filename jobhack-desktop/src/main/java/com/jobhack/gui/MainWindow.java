package com.jobhack.gui;

import com.jobhack.database.models.Application;
import com.jobhack.utils.ActivityLogger;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.*;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import lombok.extern.slf4j.Slf4j;

import java.time.format.DateTimeFormatter;

/**
 * Main Dashboard Window
 * Neo-Brutalist UI showing real-time activity, applications, and analytics
 */
@Slf4j
public class MainWindow {

    private final ActivityLogger activityLogger;
    private final ListView<String> activityListView;
    private final TableView<Application> applicationsTable;
    private final TextArea reasoningLog;
    private final Label todayCountLabel;
    private final Label responseRateLabel;
    private final Label topSkillsLabel;
    private final WebView embeddedBrowser;

    public MainWindow() {
        this.activityLogger = ActivityLogger.getInstance();
        this.activityListView = new ListView<>();
        this.applicationsTable = new TableView<>();
        this.reasoningLog = new TextArea();
        this.todayCountLabel = new Label("TODAY: 0");
        this.responseRateLabel = new Label("RESPONSE: 0%");
        this.topSkillsLabel = new Label("TOP SKILLS: ...");
        this.embeddedBrowser = new WebView();

        setupActivityLogger();
    }

    public void show(Stage stage) {
        BorderPane root = new BorderPane();
        root.getStyleClass().add("root");

        // LEFT: Activity Feed
        VBox leftPanel = createActivityFeedPanel();
        leftPanel.setPrefWidth(300);

        // CENTER: Applications Table + Browser
        VBox centerPanel = createCenterPanel();

        // RIGHT: Analytics
        VBox rightPanel = createAnalyticsPanel();
        rightPanel.setPrefWidth(250);

        // BOTTOM: AI Reasoning Log
        VBox bottomPanel = createReasoningPanel();
        bottomPanel.setPrefHeight(150);

        // TOP: Menu Bar
        MenuBar menuBar = createMenuBar();

        root.setTop(menuBar);
        root.setLeft(leftPanel);
        root.setCenter(centerPanel);
        root.setRight(rightPanel);
        root.setBottom(bottomPanel);

        Scene scene = new Scene(root, 1600, 900);
        scene.getStylesheets().add(
            getClass().getResource("/css/neo-brutalist.css").toExternalForm()
        );

        stage.setTitle("JOBHACK DESKTOP - Brutally Effective Job Applications");
        stage.setScene(scene);
        stage.setMaximized(true);
        stage.show();

        log.info("Main window displayed");

        // Log welcome message
        activityLogger.log("JobHack Desktop initialized", ActivityLogger.LogLevel.SUCCESS);
        activityLogger.log("Ready to automate job applications", ActivityLogger.LogLevel.INFO);
    }

    private MenuBar createMenuBar() {
        MenuBar menuBar = new MenuBar();

        // File Menu
        Menu fileMenu = new Menu("File");
        MenuItem settingsItem = new MenuItem("Settings");
        MenuItem exitItem = new MenuItem("Exit");
        exitItem.setOnAction(e -> Platform.exit());
        fileMenu.getItems().addAll(settingsItem, new SeparatorMenuItem(), exitItem);

        // Tools Menu
        Menu toolsMenu = new Menu("Tools");
        MenuItem scraperItem = new MenuItem("Job Scraper");
        MenuItem resumeBuilderItem = new MenuItem("Resume Builder");
        MenuItem githubSyncItem = new MenuItem("Sync GitHub");
        MenuItem emailFinderItem = new MenuItem("HR Email Finder");
        toolsMenu.getItems().addAll(scraperItem, resumeBuilderItem, githubSyncItem, emailFinderItem);

        // Help Menu
        Menu helpMenu = new Menu("Help");
        MenuItem docsItem = new MenuItem("Documentation");
        MenuItem aboutItem = new MenuItem("About");
        helpMenu.getItems().addAll(docsItem, aboutItem);

        menuBar.getMenus().addAll(fileMenu, toolsMenu, helpMenu);
        return menuBar;
    }

    private VBox createActivityFeedPanel() {
        VBox panel = new VBox(10);
        panel.getStyleClass().add("activity-feed");
        panel.setPadding(new Insets(10));

        Label header = new Label("LIVE ACTIVITY");
        header.getStyleClass().add("header");

        activityListView.getStyleClass().add("list-view");
        activityListView.setPrefHeight(Double.MAX_VALUE);

        // Load recent logs
        ObservableList<String> items = FXCollections.observableArrayList(
            activityLogger.getRecentLogs(100)
        );
        activityListView.setItems(items);

        panel.getChildren().addAll(header, activityListView);
        VBox.setVgrow(activityListView, Priority.ALWAYS);

        return panel;
    }

    private VBox createCenterPanel() {
        VBox panel = new VBox(10);
        panel.setPadding(new Insets(10));

        // Applications Table
        Label header = new Label("APPLICATIONS");
        header.getStyleClass().add("header");

        setupApplicationsTable();
        applicationsTable.setPrefHeight(400);

        // Embedded Browser
        Label browserHeader = new Label("BROWSER");
        browserHeader.getStyleClass().add("sub-header");

        embeddedBrowser.setPrefHeight(Double.MAX_VALUE);
        embeddedBrowser.getEngine().load("https://www.linkedin.com/jobs");

        panel.getChildren().addAll(header, applicationsTable, browserHeader, embeddedBrowser);
        VBox.setVgrow(embeddedBrowser, Priority.ALWAYS);

        return panel;
    }

    private void setupApplicationsTable() {
        applicationsTable.getStyleClass().add("table-view");

        TableColumn<Application, String> companyCol = new TableColumn<>("Company");
        companyCol.setCellValueFactory(new PropertyValueFactory<>("company"));
        companyCol.setPrefWidth(150);

        TableColumn<Application, String> roleCol = new TableColumn<>("Role");
        roleCol.setCellValueFactory(new PropertyValueFactory<>("role"));
        roleCol.setPrefWidth(200);

        TableColumn<Application, String> statusCol = new TableColumn<>("Status");
        statusCol.setCellValueFactory(new PropertyValueFactory<>("status"));
        statusCol.setPrefWidth(120);

        TableColumn<Application, Integer> atsCol = new TableColumn<>("ATS Score");
        atsCol.setCellValueFactory(new PropertyValueFactory<>("atsScore"));
        atsCol.setPrefWidth(100);

        TableColumn<Application, String> appliedCol = new TableColumn<>("Applied");
        appliedCol.setCellValueFactory(data -> {
            if (data.getValue().getAppliedAt() != null) {
                String formatted = data.getValue().getAppliedAt()
                    .format(DateTimeFormatter.ofPattern("MM/dd HH:mm"));
                return new javafx.beans.property.SimpleStringProperty(formatted);
            }
            return new javafx.beans.property.SimpleStringProperty("-");
        });
        appliedCol.setPrefWidth(100);

        TableColumn<Application, Void> actionsCol = new TableColumn<>("Actions");
        actionsCol.setPrefWidth(150);
        actionsCol.setCellFactory(param -> new TableCell<>() {
            private final Button viewBtn = new Button("View");

            {
                viewBtn.getStyleClass().add("button");
                viewBtn.setOnAction(e -> {
                    Application app = getTableView().getItems().get(getIndex());
                    // Open application details
                    log.info("View application: {}", app.getCompany());
                });
            }

            @Override
            protected void updateItem(Void item, boolean empty) {
                super.updateItem(item, empty);
                if (empty) {
                    setGraphic(null);
                } else {
                    setGraphic(viewBtn);
                }
            }
        });

        applicationsTable.getColumns().addAll(companyCol, roleCol, statusCol, atsCol, appliedCol, actionsCol);

        // Sample data (will be replaced with real data)
        ObservableList<Application> sampleData = FXCollections.observableArrayList(
            Application.builder()
                .company("Stripe")
                .role("Backend Engineer")
                .status("PENDING")
                .atsScore(87)
                .build(),
            Application.builder()
                .company("Airbnb")
                .role("SRE")
                .status("COMPLETED")
                .atsScore(92)
                .build()
        );
        applicationsTable.setItems(sampleData);
    }

    private VBox createAnalyticsPanel() {
        VBox panel = new VBox(15);
        panel.getStyleClass().add("analytics-panel");
        panel.setPadding(new Insets(10));

        Label header = new Label("STATS");
        header.getStyleClass().add("header");

        // Stat cards
        VBox todayCard = createStatCard("0", "Applications Today", todayCountLabel);
        VBox responseCard = createStatCard("0%", "Response Rate", responseRateLabel);
        VBox skillsCard = createStatCard("...", "Top Skills", topSkillsLabel);

        // Quick Actions
        Label actionsHeader = new Label("QUICK ACTIONS");
        actionsHeader.getStyleClass().add("sub-header");

        Button startScraperBtn = new Button("Start Job Scraper");
        startScraperBtn.getStyleClass().add("button-primary");
        startScraperBtn.setMaxWidth(Double.MAX_VALUE);

        Button buildResumeBtn = new Button("Build Resume");
        buildResumeBtn.getStyleClass().add("button");
        buildResumeBtn.setMaxWidth(Double.MAX_VALUE);

        Button findHRBtn = new Button("Find HR Contacts");
        findHRBtn.getStyleClass().add("button");
        findHRBtn.setMaxWidth(Double.MAX_VALUE);

        panel.getChildren().addAll(
            header, todayCard, responseCard, skillsCard,
            actionsHeader, startScraperBtn, buildResumeBtn, findHRBtn
        );

        return panel;
    }

    private VBox createStatCard(String value, String label, Label valueLabel) {
        VBox card = new VBox(5);
        card.getStyleClass().add("stat-card");
        card.setAlignment(Pos.CENTER);

        valueLabel.setText(value);
        valueLabel.getStyleClass().add("stat-value");

        Label labelText = new Label(label);
        labelText.getStyleClass().add("stat-label");

        card.getChildren().addAll(valueLabel, labelText);
        return card;
    }

    private VBox createReasoningPanel() {
        VBox panel = new VBox(5);
        panel.getStyleClass().add("reasoning-panel");
        panel.setPadding(new Insets(10));

        Label header = new Label("AI REASONING");
        header.getStyleClass().add("header");

        reasoningLog.getStyleClass().add("reasoning-log");
        reasoningLog.setEditable(false);
        reasoningLog.setWrapText(true);
        reasoningLog.setText("🧠 AI reasoning will appear here...\n\n" +
            "Example:\n" +
            "Why I changed this resume:\n" +
            "• JD mentioned 'scalability' 6x → highlighted distributed systems projects\n" +
            "• Company uses Go → added GitHub Go projects\n" +
            "• Culture emphasizes 'ownership' → changed 'contributed to' → 'owned'");

        panel.getChildren().addAll(header, reasoningLog);
        VBox.setVgrow(reasoningLog, Priority.ALWAYS);

        return panel;
    }

    private void setupActivityLogger() {
        // Listen for new activity logs
        activityLogger.addListener(message -> Platform.runLater(() -> {
            ObservableList<String> items = activityListView.getItems();
            items.add(0, message);

            // Keep only last 100 items
            if (items.size() > 100) {
                items.remove(100);
            }
        }));
    }

    public void updateStats(int todayCount, double responseRate, String topSkills) {
        Platform.runLater(() -> {
            todayCountLabel.setText(String.valueOf(todayCount));
            responseRateLabel.setText(String.format("%.1f%%", responseRate));
            topSkillsLabel.setText(topSkills);
        });
    }

    public void addReasoningLog(String reasoning) {
        Platform.runLater(() -> {
            String currentText = reasoningLog.getText();
            reasoningLog.setText(reasoning + "\n\n" + currentText);
        });
    }
}
