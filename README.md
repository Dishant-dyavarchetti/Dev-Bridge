# DevBridge - Open-Source Mentoring Agent System

DevBridge is an AI-powered developer mentoring platform that bridges the gap between beginner Python developers and open-source contributions. It helps developers discover suitable open-source repositories, understand unfamiliar project architectures, set up local environments, navigate contribution guidelines, and recommend beginner-friendly issues to work on.

> [!NOTE]
> The Next.js web frontend is currently under construction and will be integrated with this backend AI service upon deployment.

---

## Concepts Demonstration Usecases in Project

To meet the final evaluation criteria, here is where each key concept covered in the course is applied and demonstrated:

| Key Concept                          | Implementation / Demonstration Location | Description                                                                                                                                                                                                               |
| :----------------------------------- | :-------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Agent / Multi-Agent System (ADK)** | **Code**                                | Built using Google ADK with 6 specialized agents coordinated via a state graph orchestrator.                                                                                                                              |
| **Security Features**                | **Code & Design**                       | Implemented strict input sanitization, XML prompt boundaries, safety filters (`HarmCategory`), and a [Security Architecture design document](file:///home/dishant/dishant_dev/DevBridge/design/security-architecture.md). |
| **Deployability**                    | **Code & Docker**                       | Fully containerized with a production-ready `Dockerfile` and configured to run on free-tier serverless environments.                                                                                                      |
| **Agent Skills (Agents CLI)**        | **Code & CLI**                          | Developed and verified locally using `agents-cli playground` and the ADK test runner.                                                                                                                                     |
| **Antigravity**                      | **Video**                               | Demonstrated in the project submission video.                                                                                                                                                                             |
| **MCP Server**                       | **Code**                                | Configured to support lazy-loaded MCP servers for extended capabilities.                                                                                                                                                  |

---

## 1. The Pitch: Problem, Solution & Value

### The Problem

Entering the world of open-source software can be highly intimidating for beginner developers. They face several friction points:

- **Overwhelming Codebases**: Unfamiliar architectures make it hard to know where to look.
- **Environment Setup Roadblocks**: Complicated local installation guides, dependency mismatches, and build failures.
- **Finding the Right Issue**: Sifting through hundreds of issues to find ones tagged with `good first issue` or `beginner-friendly` that match their current skill set.

### The Solution: Why Agents?

Standard LLMs fall short because open-source onboarding requires multi-step reasoning, API data aggregation, and persistent context tracking.
DevBridge uses a **stateful multi-agent system** where specialized agents collaborate:

- **Orchestrated Parallelism**: The contribution guideline parsing and issue recommendation analysis run in parallel, fanning in to compose a unified guide.
- **Context Continuity**: Using a shared `devbridge_state` to pass validated outputs between specialized nodes.

---

## 2. Technical Architecture & Implementation

### Workflow Graph

The system is built on a Google ADK state-graph orchestrator:

```text
               START
                 │
                 ▼
          ┌──────────────┐
          │ PlannerNode  │
          └──────┬───────┘
                 ├─────────────────────────┐
      (DISCOVER_REPOSITORIES)      (OTHER INTENTS)
                 │                         │
                 ▼                         ▼
         ┌──────────────┐          ┌──────────────┐
         │DiscoveryNode │ ────────►│ AnalysisNode │
         └──────────────┘          └──────┬───────┘
                                           │
                                ┌──────────┴──────────┐
                                ▼                     ▼
                        ┌──────────────┐      ┌──────────────┐
                        │ Contribution │      │  IssueNode   │
                        │     Node     │      │              │
                        └──────────┬───┘      └──────┬───────┘
                                   │                 │
                                   └──────────┬──────┘
                                              ▼
                                       ┌──────────────┐
                                       │  MergeNode   │
                                       └──────┬───────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ ResponseNode │
                                       └──────┬───────┘
                                              │
                                              ▼
                                             END
```

### Specialized Agents (ADK)

1. **`PlannerAgent`**: Classifies user requests and manages routing logic.
2. **`DiscoveryAgent`**: Matches the user's Python skills with ideal open-source projects.
3. **`AnalysisAgent`**: Inspects codebase file structures and detects frameworks.
4. **`ContributionAgent`**: Outlines setup, dependencies, and PR processes.
5. **`IssueRecommendationAgent`**: Curates issues based on labels like `good first issue`.
6. **`ResponseComposerAgent`**: Compiles all outputs into a structured mentoring guide.

### Robust Safety & Quota Configurations

- **Input Sanitization**: Automatically strips shell commands and restricts prompt lengths to block command injections.
- **Safety Filters**: Configured with strict Google GenAI `SafetySetting` filters blocking harassment, hate speech, and dangerous content.
- **Auto-Retries**: Implements 5x exponential backoff retries via `HttpRetryOptions` to handle transient AI Studio free-tier traffic spikes.
- **Gemma 4 Toggle**: Includes a safe environment toggle (`USE_GEMMA_FOR_RESPONSE=True`) to route heavy text generation to `gemma-4-31b-it` (which has higher rate limits).

---

## Setup & Execution

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (for environment management)

### Local Installation

1. Clone the repository and navigate to `devbridge-agent/`:
   ```bash
   cd devbridge-agent
   ```
2. Build the local virtual environment and install dependencies:
   ```bash
   uv sync
   ```

### Configuration

Create a `.env` file at the root of `devbridge-agent/`:

```env
# GitHub Token (for codebase extraction)
GITHUB_TOKEN="your_github_pat"

# Google AI Studio API Key
GOOGLE_API_KEY="your_api_key"

# Database Connection (Neon Postgres)
DATABASE_URL="postgresql://[USER]:[PASSWORD]@[NEON_HOST]/neondb?sslmode=require"

# Safe Gemma 4 Response Toggle
USE_GEMMA_FOR_RESPONSE=False
```

### Running Locally

To launch the interactive developer playground and trace workspace:

```bash
agents-cli playground
```

This runs the local server at `http://127.0.0.1:8080`.

### Running Tests

To run the validation test suite:

```bash
uv run pytest tests/integration
```

---

## Deployment

The project contains a production-ready `Dockerfile` at the root of `devbridge-agent/` configured for serverless deployment (such as Hugging Face Spaces, Render, or GCP Cloud Run).

### Build & Run Container

```bash
# Build the Docker image
docker build -t devbridge-agent .

# Run the container locally
docker run -p 8080:8080 --env-file .env devbridge-agent
```

🚨 **Security Reminder**: Never hardcode your `GOOGLE_API_KEY` or `GITHUB_TOKEN` in the Dockerfile or codebase. Always feed them as runtime environment variables.

---

## Future Expansion

- **IDE Extension**: We plan to develop an IDE extension (e.g., VS Code or Cursor) so that developers can get real-time mentoring, codebase explanations, and execution instructions for contributing to open-source repositories directly within their active workspace.
