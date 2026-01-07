package com.jobhack.ai;

import com.jobhack.config.Constants;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;

/**
 * Email Generator
 * Generates personalized cold outreach emails using Claude
 */
@Slf4j
public class EmailGenerator {

    private final ClaudeClient claudeClient;

    public EmailGenerator() {
        this.claudeClient = new ClaudeClient();
    }

    /**
     * Generate personalized email for hiring manager
     */
    public GeneratedEmail generateHiringManagerEmail(
        String recipientName,
        String recipientTitle,
        String company,
        String role,
        String jobDescription,
        String userContext,
        String companyResearch) throws IOException {

        String prompt = String.format("""
            Generate a personalized cold email to a hiring manager.

            Recipient: %s (%s at %s)
            Role Applied To: %s

            Job Description Summary:
            %s

            Candidate Context:
            %s

            Company Research:
            %s

            Email should:
            - Be 150-200 words
            - Reference specific candidate projects relevant to the role
            - Mention recent company news/achievements
            - Be conversational, not salesy
            - Include clear call-to-action (15-min call)
            - Show genuine interest in the company's mission

            Return JSON:
            {
              "subject": "Email subject line",
              "body": "Email body",
              "tone": "professional/friendly/technical"
            }
            """, recipientName, recipientTitle, company, role, jobDescription, userContext, companyResearch);

        try {
            var response = claudeClient.generateJson(prompt);
            GeneratedEmail email = new GeneratedEmail();
            email.setSubject(response.get("subject").asText());
            email.setBody(response.get("body").asText());
            email.setTone(response.get("tone").asText());
            email.setType(Constants.EMAIL_TO_HIRING_MANAGER);
            return email;
        } catch (Exception e) {
            log.error("Failed to generate hiring manager email", e);
            throw new IOException("Failed to generate email: " + e.getMessage(), e);
        }
    }

    /**
     * Generate referral request email
     */
    public GeneratedEmail generateReferralEmail(
        String recipientName,
        String company,
        String role,
        String mutualConnection,
        String userContext) throws IOException {

        String prompt = String.format("""
            Generate a referral request email to an employee at the target company.

            Recipient: %s (works at %s)
            Role Interested In: %s
            Mutual Connection: %s

            Candidate Context:
            %s

            Email should:
            - Be brief (100-150 words)
            - Mention mutual connection if applicable
            - Express genuine interest in the company
            - Politely request referral
            - Offer to share resume/portfolio

            Return JSON with subject and body.
            """, recipientName, company, role, mutualConnection, userContext);

        try {
            var response = claudeClient.generateJson(prompt);
            GeneratedEmail email = new GeneratedEmail();
            email.setSubject(response.get("subject").asText());
            email.setBody(response.get("body").asText());
            email.setType(Constants.EMAIL_REFERRAL_REQUEST);
            return email;
        } catch (Exception e) {
            log.error("Failed to generate referral email", e);
            throw new IOException("Failed to generate email: " + e.getMessage(), e);
        }
    }

    /**
     * Generate follow-up email
     */
    public GeneratedEmail generateFollowUpEmail(
        String recipientName,
        String company,
        String originalEmailDate,
        String userContext) throws IOException {

        String prompt = String.format("""
            Generate a follow-up email (original email sent %s).

            Recipient: %s at %s

            Candidate Context:
            %s

            Follow-up should:
            - Be brief (75-100 words)
            - Reference original email
            - Add value (new relevant project, insight)
            - Remain polite and professional
            - Suggest specific times for call

            Return JSON with subject and body.
            """, originalEmailDate, recipientName, company, userContext);

        try {
            var response = claudeClient.generateJson(prompt);
            GeneratedEmail email = new GeneratedEmail();
            email.setSubject(response.get("subject").asText());
            email.setBody(response.get("body").asText());
            email.setType(Constants.EMAIL_FOLLOW_UP);
            return email;
        } catch (Exception e) {
            log.error("Failed to generate follow-up email", e);
            throw new IOException("Failed to generate email: " + e.getMessage(), e);
        }
    }

    @Data
    public static class GeneratedEmail {
        private String subject;
        private String body;
        private String tone;
        private String type;
    }
}
