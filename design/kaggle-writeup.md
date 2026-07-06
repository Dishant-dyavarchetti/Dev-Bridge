# Kaggle Capstone Project Writeup: DevBridge

This document contains the official project description and writeup details for the DevBridge submission in the AI Agent Software Competition.

---

## 1. Project Title & Subtitle
* **Title**: DevBridge
* **Subtitle**: An autonomous multi-agent mentoring system guiding beginner Python developers from repository discovery to their first open-source contribution.

---

## 2. Project Description

### Overview
Contributing to open-source software is one of the best ways for developers to grow, yet the barrier to entry is notoriously steep for beginners. New contributors are often overwhelmed by complex directory structures, undocumented setup procedures, confusing contribution guidelines, and the difficulty of finding issues suitable for their current skill level.

**DevBridge** is an autonomous developer mentoring system that acts as a personalized guide, bridging the gap between beginner Python developers and open-source contributions. By parsing repository structures, analyzing contribution documentation, and curating actual GitHub issues, DevBridge compiles a unified, step-by-step onboarding roadmap tailored to the developer's exact background.

---

### Why Agents? (The Multi-Agent Architecture)
Onboarding requires multi-step reasoning, external API data retrieval, and stateful decision-making. Single LLM prompt calls fail due to token context-window congestion and lack of structured validation. 

DevBridge leverages **Google’s Agent Development Kit (ADK 2.0)** to coordinate **six (6) specialized agents** through a structured state-graph:
1. **The Planner**: Classifies the user's intent and manages routing paths in the orchestration graph.
2. **The Discovery Agent**: Matches the user's Python skills with ideal open-source repositories.
3. **The Analysis Agent**: Crawls the chosen codebase to detect structures, languages, and frameworks.
4. **The Contribution Agent**: Scans guideline documentation (`CONTRIBUTING.md`, `README.md`) to extract environment setup steps, dependencies, and pull request procedures.
5. **The Issue Recommendation Agent**: Curates open GitHub issues matching tags like `good first issue` or `beginner-friendly`.
6. **The Response Composer**: Fuses all the collected data into a unified, rich Markdown guide.

* **Parallel Workflow Execution**: The contribution parsing and issue curation nodes run in parallel, fanning in to a Merge node to minimize processing latency.

---

### Design Decisions: Why We Avoided Agent-to-Agent (A2A) Protocols
During architectural design, we explicitly chose **not** to use the Agent-to-Agent (A2A) message-passing protocol. 
* **Stateful Centralization over Conversational Drift**: A2A relies on conversational messaging back and forth between agents, which can lead to loop conditions, hallucination drift, and high latency. For DevBridge's structured, deterministic workflow, a state-graph topology was far more appropriate.
* **The `DevBridgeState` Pydantic Object**: Instead of agents communicating directly, all agents read from and manipulate a single, unified state object (`DevBridgeState`).
* **Enhanced Auditing & Tool Tracking**: Operating on a single, shared state object allows us to track, validate, and serialize exactly what tools were used, what APIs were called, and what data changes occurred at every step of the graph execution. This provides absolute auditability and type-safety.

---

### The Build: Tools & Technologies
The development of DevBridge was powered by modern, professional agentic engineering tools:
* **Google ADK (2.0)**: The core framework used to build stateful workflows, instantiate agents, and coordinate execution.
* **GitHub REST API & `GITHUB_TOKEN`**: Integrated to authenticate and crawl open-source repository structures, read files, and extract active issues.
* **`agents-cli`**: Used for project scaffolding (`agents-cli scaffold`), automated evaluation datasets testing, and local interactive execution using `agents-cli playground`.
* **Python `pytest`**: Wired with integration tests to validate routing and Pydantic outputs.
* **Neon DB (Serverless Postgres)**: Connected as a serverless database backend to handle state cache and metadata storage.
* **Docker Containerization**: Packaging the Python FastAPI backend into a production-ready container optimized for free-tier hosting platforms like Hugging Face Spaces.

---

### Key Technical Highlights & Implementation

* **Safe Gemma 4 & Gemini Routing Toggle**: To balance intelligence and rate limits, DevBridge supports an environment-level toggle (`USE_GEMMA_FOR_RESPONSE`). While sub-tasks run on the fast `gemini-2.5-flash-lite`, the final, token-intensive markdown guide is composed using **`gemma-4-31b-it`** (running schema-free to bypass API limitations).
* **Robust Security Controls**: Implements strict command-injection defenses at the gateway, XML prompt boundaries, strict Google GenAI safety filters, and Pydantic output schema validation to prevent LLM manipulation.
* **Auto-Retry Resilience**: Configured with built-in `HttpRetryOptions` (5x exponential backoff) to handle transient 503 load errors and 429 rate limit spikes on the AI Studio free tier.
* **Database Integration**: Fully connected to a serverless **Neon PostgreSQL database** to persist session histories and cache codebase insights.
* **Containerized Deployability**: Bundled with a production-ready `Dockerfile` optimized for hosting on free-tier container platforms like Hugging Face Spaces.

---

### Future Expansion
The next phase of DevBridge is the development of an **IDE Extension (VS Code / Cursor)**. This will bring mentoring advice, codebase explanations, and terminal execution steps directly into the developer's local workspace, ensuring they never have to leave their editor to make their first pull request.
