package com.jobhack.ai;

import com.fasterxml.jackson.databind.JsonNode;
import com.jobhack.utils.ActivityLogger;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Resume Optimizer
 * Uses Claude to generate ATS-optimized resumes tailored to specific job descriptions
 */
@Slf4j
public class ResumeOptimizer {

    private final ClaudeClient claudeClient;
    private final ActivityLogger activityLogger;

    public ResumeOptimizer() {
        this.claudeClient = new ClaudeClient();
        this.activityLogger = ActivityLogger.getInstance();
    }

    /**
     * Optimize resume for a specific job description
     */
    public OptimizedResume optimize(String jobDescription, String currentResume,
                                   String githubProjects, String essayContext) throws IOException {

        activityLogger.log("Analyzing job description and optimizing resume", ActivityLogger.LogLevel.AI);

        String prompt = String.format("""
            You are an expert resume writer specializing in ATS optimization.

            Job Description:
            %s

            Candidate's Current Resume:
            %s

            Candidate's GitHub Projects:
            %s

            Candidate's Background (from essays):
            %s

            Task:
            1. Analyze which GitHub projects best match this job description
            2. Reorder resume sections to highlight most relevant experience
            3. Rewrite bullet points to include job description keywords naturally
            4. Add technical skills mentioned in JD but missing from resume (if candidate has them)
            5. Ensure ATS-friendly formatting (no tables, images, or complex layouts)
            6. Match the tone and language used in the job description

            Return a JSON object with:
            {
              "resume_markdown": "Full optimized resume in markdown format with proper sections",
              "ats_score": 85,
              "changes_made": [
                "Added 'Docker' to skills section (mentioned 5x in JD)",
                "Moved 'Microservices Project' to top (matches JD architecture)",
                "Changed 'worked on' → 'architected' (leadership keyword)",
                "Highlighted distributed systems experience",
                "Added quantifiable metrics (2000+ hours saved)"
              ],
              "keywords_matched": ["Docker", "Kubernetes", "Python", "microservices"],
              "keywords_missing": ["Terraform", "CI/CD"],
              "projects_included": ["project1", "project2"],
              "suggestions": [
                "Consider adding Terraform to your skillset (mentioned 3x in JD)",
                "Quantify impact in bullet points where possible"
              ]
            }

            Return ONLY valid JSON.
            """, jobDescription, currentResume, githubProjects, essayContext);

        try {
            JsonNode response = claudeClient.generateJson(prompt);
            OptimizedResume optimized = parseToOptimizedResume(response);

            activityLogger.log(
                String.format("Resume optimized - ATS Score: %d/100", optimized.getAtsScore()),
                ActivityLogger.LogLevel.SUCCESS
            );

            // Log changes to reasoning panel
            StringBuilder reasoning = new StringBuilder("🧠 Why I changed this resume:\n\n");
            optimized.getChangesMade().forEach(change -> reasoning.append("• ").append(change).append("\n"));
            log.info("Resume optimization reasoning: {}", reasoning);

            return optimized;

        } catch (Exception e) {
            log.error("Failed to optimize resume", e);
            activityLogger.log("Resume optimization failed: " + e.getMessage(), ActivityLogger.LogLevel.ERROR);
            throw new IOException("Failed to optimize resume: " + e.getMessage(), e);
        }
    }

    private OptimizedResume parseToOptimizedResume(JsonNode json) {
        OptimizedResume resume = new OptimizedResume();

        if (json.has("resume_markdown")) {
            resume.setResumeMarkdown(json.get("resume_markdown").asText());
        }

        if (json.has("ats_score")) {
            resume.setAtsScore(json.get("ats_score").asInt());
        }

        resume.setChangesMade(jsonArrayToList(json.get("changes_made")));
        resume.setKeywordsMatched(jsonArrayToList(json.get("keywords_matched")));
        resume.setKeywordsMissing(jsonArrayToList(json.get("keywords_missing")));
        resume.setProjectsIncluded(jsonArrayToList(json.get("projects_included")));
        resume.setSuggestions(jsonArrayToList(json.get("suggestions")));

        return resume;
    }

    /**
     * Calculate ATS score for an existing resume against a job description
     */
    public int calculateATSScore(String resume, String jobDescription) throws IOException {
        String prompt = String.format("""
            Calculate the ATS (Applicant Tracking System) score for this resume against the job description.

            Job Description:
            %s

            Resume:
            %s

            Score from 0-100 based on:
            - Keyword matches (40 points)
            - Relevant experience (30 points)
            - Format compliance (15 points)
            - Skills alignment (15 points)

            Return JSON: {"score": 85, "reasoning": "explanation"}
            """, jobDescription, resume);

        try {
            JsonNode response = claudeClient.generateJson(prompt);
            return response.get("score").asInt();
        } catch (Exception e) {
            log.error("Failed to calculate ATS score", e);
            return 0;
        }
    }

    private List<String> jsonArrayToList(JsonNode arrayNode) {
        List<String> list = new ArrayList<>();
        if (arrayNode != null && arrayNode.isArray()) {
            arrayNode.forEach(node -> list.add(node.asText()));
        }
        return list;
    }

    @Data
    public static class OptimizedResume {
        private String resumeMarkdown;
        private int atsScore;
        private List<String> changesMade = new ArrayList<>();
        private List<String> keywordsMatched = new ArrayList<>();
        private List<String> keywordsMissing = new ArrayList<>();
        private List<String> projectsIncluded = new ArrayList<>();
        private List<String> suggestions = new ArrayList<>();
    }
}
