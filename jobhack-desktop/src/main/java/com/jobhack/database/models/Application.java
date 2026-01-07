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
public class Application {
    private Long id;
    private Long userId;
    private String company;
    private String role;
    private String jobUrl;
    private String platform;
    private String jobDescription;
    private String applicationType;
    private String status;
    private Integer atsScore;
    private String resumePath;
    private String coverLetterPath;
    private LocalDateTime appliedAt;
    private LocalDateTime confirmedAt;
    private String rejectionReason;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
