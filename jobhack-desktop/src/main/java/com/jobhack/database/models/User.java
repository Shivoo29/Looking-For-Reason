package com.jobhack.database.models;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private String email;
    private String phone;
    private String linkedinUrl;
    private String githubUsername;
    private String currentResumePath;
    private boolean onboardingCompleted;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
