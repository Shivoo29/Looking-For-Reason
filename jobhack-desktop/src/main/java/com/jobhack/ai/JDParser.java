package com.jobhack.ai;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Job Description Parser
 * Extracts structured information from job descriptions using Claude
 */
@Slf4j
public class JDParser {

    private final ClaudeClient claudeClient;

    public JDParser() {
        this.claudeClient = new ClaudeClient();
    }

    /**
     * Parse job description and extract key information
     */
    public ParsedJD parse(String jobDescription) throws IOException {
        String prompt = String.format("""
            Analyze this job description and extract structured information.

            Job Description:
            %s

            Extract and return a JSON object with:
            {
              "required_skills": ["list", "of", "must-have", "skills"],
              "preferred_skills": ["list", "of", "nice-to-have", "skills"],
              "keywords": ["important", "keywords", "for", "ATS"],
              "tech_stack": ["technologies", "mentioned"],
              "experience_years": 3,
              "degree_required": "Bachelor's in Computer Science",
              "culture_signals": ["collaborative", "fast-paced", "etc"],
              "responsibilities": ["main", "job", "duties"],
              "company_size": "startup/midsize/enterprise",
              "remote_policy": "remote/hybrid/onsite"
            }

            Return ONLY valid JSON, no markdown formatting.
            """, jobDescription);

        try {
            JsonNode response = claudeClient.generateJson(prompt);
            return parseToParsedJD(response);
        } catch (Exception e) {
            log.error("Failed to parse job description", e);
            throw new IOException("Failed to parse job description: " + e.getMessage(), e);
        }
    }

    private ParsedJD parseToParsedJD(JsonNode json) {
        ParsedJD parsed = new ParsedJD();

        // Extract arrays
        parsed.setRequiredSkills(jsonArrayToList(json.get("required_skills")));
        parsed.setPreferredSkills(jsonArrayToList(json.get("preferred_skills")));
        parsed.setKeywords(jsonArrayToList(json.get("keywords")));
        parsed.setTechStack(jsonArrayToList(json.get("tech_stack")));
        parsed.setCultureSignals(jsonArrayToList(json.get("culture_signals")));
        parsed.setResponsibilities(jsonArrayToList(json.get("responsibilities")));

        // Extract scalars
        if (json.has("experience_years") && !json.get("experience_years").isNull()) {
            parsed.setExperienceYears(json.get("experience_years").asInt());
        }
        if (json.has("degree_required") && !json.get("degree_required").isNull()) {
            parsed.setDegreeRequired(json.get("degree_required").asText());
        }
        if (json.has("company_size") && !json.get("company_size").isNull()) {
            parsed.setCompanySize(json.get("company_size").asText());
        }
        if (json.has("remote_policy") && !json.get("remote_policy").isNull()) {
            parsed.setRemotePolicy(json.get("remote_policy").asText());
        }

        return parsed;
    }

    private List<String> jsonArrayToList(JsonNode arrayNode) {
        List<String> list = new ArrayList<>();
        if (arrayNode != null && arrayNode.isArray()) {
            arrayNode.forEach(node -> list.add(node.asText()));
        }
        return list;
    }

    @Data
    public static class ParsedJD {
        private List<String> requiredSkills = new ArrayList<>();
        private List<String> preferredSkills = new ArrayList<>();
        private List<String> keywords = new ArrayList<>();
        private List<String> techStack = new ArrayList<>();
        private List<String> cultureSignals = new ArrayList<>();
        private List<String> responsibilities = new ArrayList<>();
        private Integer experienceYears;
        private String degreeRequired;
        private String companySize;
        private String remotePolicy;
    }
}
