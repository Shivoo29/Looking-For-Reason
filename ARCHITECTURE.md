# Architecture Blueprint

This document outlines the proposed technical architecture for **Looking-For-Reason (LFR)**. The design is based on a modular, scalable microservices approach to accommodate the phased rollout and future complexity.

---

## 1. High-Level Overview

The system is composed of three main parts:
1.  **Frontend**: A Next.js web application that serves as the user interface.
2.  **Backend**: A collection of independent microservices, each responsible for a specific domain of business logic.
3.  **Data Stores**: A primary relational database for user data and a vector database for AI-powered search and analysis.

```
+-----------------+      +------------------+      +----------------------+
|                 |      |                  |      |                      |
| Browser         |----->|   API Gateway    |----->|   Backend Services   |
| (Next.js App)   |      | (Node.js/Express)|      | (Node.js / Python)   |
|                 |      |                  |      |                      |
+-----------------+      +------------------+      +----------+-----------+
                                                              |
                                                              |
                                     +------------------------+------------------------+
                                     |                                                 |
                             +-------+--------+                                +--------+-------+
                             |                |                                |                |
                             |  PostgreSQL DB |                                | Vector DB      |
                             | (Users, Apps)  |                                | (Embeddings)   |
                             |                |                                |                |
                             +----------------+                                +----------------+
```

---

## 2. Frontend

-   **Framework**: **Next.js (React)**. Chosen for its powerful features including server-side rendering (SSR) for a fast initial load, static site generation (SSG) for marketing pages, and a robust ecosystem.
-   **Styling**: **Plain CSS Modules or a lightweight CSS-in-JS library like `Stitches`**. The Neo-Brutalist aesthetic does not require a heavy component library like Material-UI or Bootstrap. The focus will be on custom styles that are fast, functional, and easy to maintain.
-   **State Management**: **React Context/Hooks** for simple state. For more complex, cross-component state, **Zustand** is recommended for its simplicity and minimal boilerplate.
-   **Deployment**: **Vercel** is the natural choice for Next.js applications, providing seamless CI/CD and hosting.

---

## 3. Backend (Microservices)

The backend will be a set of containerized services communicating via a central API Gateway. This allows for independent development, deployment, and scaling.

-   **API Gateway**:
    -   **Tech**: **Node.js with Express.js or Fastify**.
    -   **Responsibility**: Acts as the single entry point for the frontend. It handles request validation, authentication, and routing to the appropriate microservice.

-   **`users-service`**:
    -   **Tech**: **Node.js/Fastify**.
    -   **Responsibility**: Manages user accounts, authentication (JWT/OAuth), and profile information.

-   **`ingestion-service`**:
    -   **Tech**: **Python with FastAPI**. Python is ideal for its rich ecosystem of NLP and document parsing libraries.
    -   **Responsibility**: Handles parsing of uploaded resumes (PDF, DOCX, text) and extraction of text from JDs.

-   **`analysis-service`**:
    -   **Tech**: **Python with FastAPI**.
    -   **Responsibility**: The core AI engine. It takes parsed resume/JD text, performs keyword extraction, runs the gap analysis, and orchestrates the rewrite logic. It will interface with the Vector DB to find semantically similar phrases.

-   **`outreach-service`**:
    -   **Tech**: **Python with FastAPI**.
    -   **Responsibility**: Manages contact identification by integrating with third-party scraping APIs. It also contains the logic for drafting personalized outreach messages using LLMs.

-   **`application-service`**:
    -   **Tech**: **Node.js/Fastify**.
    -   **Responsibility**: Handles CRUD operations for the application tracker/dashboard.

-   **Containerization**: All backend services will be containerized using **Docker** and managed with **Docker Compose** for local development. For production, a container orchestration platform like **Kubernetes (EKS, GKE)** or a simpler service like **AWS Fargate** is recommended.

---

## 4. Data Stores

-   **Primary Database**: **PostgreSQL**. A robust, open-source relational database perfect for storing structured data like user information, application statuses, and other metadata.
-   **Vector Database**: **ChromaDB, Weaviate, or Pinecone**. Essential for the AI/NLP components. It will store vector embeddings of skills, job titles, and resume bullet points to enable fast, semantic similarity searches, which is far more powerful than simple keyword matching.

---

## 5. AI & NLP Strategy

-   **Parsing**: For Phase 1, use established Python libraries (`pypdf2`, `python-docx`, `spaCy` for entity recognition).
-   **Keyword Extraction**: Use `spaCy` or a similar library for Named Entity Recognition (NER) to identify skills, technologies, and job titles.
-   **Semantic Rewrite**:
    1.  Embed the user's resume sentences and the JD's required skills into vectors using a sentence-transformer model (e.g., from Hugging Face).
    2.  Store these embeddings in the Vector DB.
    3.  When rewriting, for a missing keyword, find the most semantically similar sentence in the user's resume and use an LLM to intelligently merge the keyword into it.
-   **Message Drafting**: Use a powerful, instruction-tuned LLM (e.g., GPT-4, Claude) via an API. The quality of the prompt will be critical and will include context from the user's resume, the JD, and the target's profile.
