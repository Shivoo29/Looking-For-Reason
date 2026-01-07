package com.jobhack.ai;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jobhack.config.AppConfig;
import lombok.extern.slf4j.Slf4j;
import okhttp3.*;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/**
 * Claude API Client
 * Wrapper for Anthropic's Claude API
 */
@Slf4j
public class ClaudeClient {

    private static final String API_URL = "https://api.anthropic.com/v1/messages";
    private static final String API_VERSION = "2023-06-01";

    private final OkHttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String apiKey;
    private final String model;

    public ClaudeClient() {
        AppConfig config = AppConfig.getInstance();
        this.apiKey = config.getAnthropicApiKey();
        this.model = config.getAiModel();

        this.httpClient = new OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(120, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build();

        this.objectMapper = new ObjectMapper();

        if (apiKey == null || apiKey.isEmpty()) {
            log.warn("Anthropic API key not configured. Set ANTHROPIC_API_KEY environment variable.");
        }
    }

    /**
     * Generate text using Claude API
     */
    public String generate(String prompt) throws IOException {
        return generate(prompt, 4096, 0.7);
    }

    /**
     * Generate text with custom parameters
     */
    public String generate(String prompt, int maxTokens, double temperature) throws IOException {
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalStateException("Anthropic API key not configured");
        }

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("model", model);
        requestBody.put("max_tokens", maxTokens);
        requestBody.put("temperature", temperature);
        requestBody.put("messages", new Object[]{
            Map.of("role", "user", "content", prompt)
        });

        String json = objectMapper.writeValueAsString(requestBody);

        Request request = new Request.Builder()
            .url(API_URL)
            .addHeader("x-api-key", apiKey)
            .addHeader("anthropic-version", API_VERSION)
            .addHeader("content-type", "application/json")
            .post(RequestBody.create(json, MediaType.parse("application/json")))
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                String errorBody = response.body() != null ? response.body().string() : "Unknown error";
                log.error("Claude API error: {} - {}", response.code(), errorBody);
                throw new IOException("Claude API error: " + response.code() + " - " + errorBody);
            }

            String responseBody = response.body().string();
            JsonNode jsonResponse = objectMapper.readTree(responseBody);

            // Extract text from response
            JsonNode contentArray = jsonResponse.get("content");
            if (contentArray != null && contentArray.isArray() && contentArray.size() > 0) {
                JsonNode firstContent = contentArray.get(0);
                if (firstContent.has("text")) {
                    return firstContent.get("text").asText();
                }
            }

            throw new IOException("Unexpected response format from Claude API");
        }
    }

    /**
     * Generate structured output (JSON)
     */
    public JsonNode generateJson(String prompt) throws IOException {
        String response = generate(prompt);

        // Try to extract JSON from response
        // Claude sometimes wraps JSON in markdown code blocks
        String jsonStr = response;
        if (response.contains("```json")) {
            int start = response.indexOf("```json") + 7;
            int end = response.lastIndexOf("```");
            if (end > start) {
                jsonStr = response.substring(start, end).trim();
            }
        } else if (response.contains("```")) {
            int start = response.indexOf("```") + 3;
            int end = response.lastIndexOf("```");
            if (end > start) {
                jsonStr = response.substring(start, end).trim();
            }
        }

        return objectMapper.readTree(jsonStr);
    }

    /**
     * Generate embeddings for text (for vector storage)
     * Note: Claude doesn't provide embeddings API directly
     * This is a placeholder - you might want to use a different model for embeddings
     */
    public double[] generateEmbedding(String text) {
        // TODO: Implement using a proper embedding model
        // Options: OpenAI embeddings, sentence-transformers via Python bridge, etc.
        log.warn("Embedding generation not yet implemented");
        return new double[0];
    }
}
