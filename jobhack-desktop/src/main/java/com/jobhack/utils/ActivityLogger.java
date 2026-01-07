package com.jobhack.utils;

import com.jobhack.database.DatabaseManager;
import lombok.extern.slf4j.Slf4j;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * Activity Logger - Logs all application activities for the dashboard feed
 */
@Slf4j
public class ActivityLogger {

    private static ActivityLogger instance;
    private final List<Consumer<String>> listeners = new ArrayList<>();
    private final DatabaseManager databaseManager;

    public enum LogLevel {
        INFO("🔍"),
        SUCCESS("✅"),
        WARNING("⚠️"),
        ERROR("❌"),
        AI("🧠");

        private final String emoji;

        LogLevel(String emoji) {
            this.emoji = emoji;
        }

        public String getEmoji() {
            return emoji;
        }
    }

    private ActivityLogger() {
        this.databaseManager = DatabaseManager.getInstance();
    }

    public static ActivityLogger getInstance() {
        if (instance == null) {
            synchronized (ActivityLogger.class) {
                if (instance == null) {
                    instance = new ActivityLogger();
                }
            }
        }
        return instance;
    }

    /**
     * Log an activity
     */
    public void log(String message, LogLevel level) {
        log(message, level, null);
    }

    /**
     * Log an activity with details
     */
    public void log(String message, LogLevel level, String details) {
        String timestamp = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
        String formatted = String.format("[%s] %s %s", timestamp, level.getEmoji(), message);

        // Log to console
        switch (level) {
            case ERROR -> log.error(message);
            case WARNING -> log.warn(message);
            default -> log.info(message);
        }

        // Store in database
        try (Connection conn = databaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "INSERT INTO activity_log (log_level, message, details) VALUES (?, ?, ?)")) {

            stmt.setString(1, level.name());
            stmt.setString(2, message);
            stmt.setString(3, details);
            stmt.executeUpdate();

        } catch (Exception e) {
            log.error("Failed to store activity log", e);
        }

        // Notify listeners (for GUI updates)
        notifyListeners(formatted);
    }

    /**
     * Add a listener for activity updates (used by GUI)
     */
    public void addListener(Consumer<String> listener) {
        listeners.add(listener);
    }

    /**
     * Remove a listener
     */
    public void removeListener(Consumer<String> listener) {
        listeners.remove(listener);
    }

    private void notifyListeners(String formattedMessage) {
        listeners.forEach(listener -> listener.accept(formattedMessage));
    }

    /**
     * Retrieve recent activity logs
     */
    public List<String> getRecentLogs(int limit) {
        List<String> logs = new ArrayList<>();

        try (Connection conn = databaseManager.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "SELECT log_level, message, timestamp FROM activity_log ORDER BY timestamp DESC LIMIT ?")) {

            stmt.setInt(1, limit);
            var rs = stmt.executeQuery();

            while (rs.next()) {
                String level = rs.getString("log_level");
                String message = rs.getString("message");
                String timestamp = rs.getString("timestamp");

                LogLevel logLevel = LogLevel.valueOf(level);
                String formatted = String.format("[%s] %s %s",
                    timestamp.substring(11, 19), // Extract HH:mm:ss
                    logLevel.getEmoji(),
                    message);

                logs.add(formatted);
            }

        } catch (Exception e) {
            log.error("Failed to retrieve activity logs", e);
        }

        return logs;
    }
}
