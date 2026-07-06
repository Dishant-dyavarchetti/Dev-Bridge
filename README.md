# DevBridge

DevBridge is an AI-powered mentoring platform designed to bridge the gap between beginner Python developers and open-source contributions. It assists developers in discovering suitable open-source repositories, understanding repository architecture, setting up their local environments, navigating contribution guidelines, and finding beginner-friendly issues to work on.

> [!NOTE]
> The Next.js web frontend is currently under construction and will be integrated with this backend AI service upon deployment.

---

## 🌟 Key Features

* **Multi-Agent Orchestration**: Outfitted with 6 specialized reasoning agents (Planner, Discovery, Analysis, Contribution, Issue Recommendation, and Response Composer) running on Google ADK.
* **Graph-Driven Workflow**: Uses a dynamic state-graph orchestrator to route user queries sequentially through discovery, analysis, parallel contribution parsing, and issue curation before composing responses.
* **Secure Model Setup**: Centralized safety filters enabled across all agents to block harmful content (hate speech, harassment, etc.).
* **Quota-Friendly Execution**: Automatic 5x exponential backoff retries to handle transient 503/429 server spikes on the AI Studio free tier.
* **Gemma 4 & Gemini Integration**: Safe toggle options in `.env` to run intensive text tasks on the high-quota `gemma-4-31b-it` model or fall back to `gemini-2.5-flash` natively.
* **Database Caching & Persistence**: Connected to a serverless Neon PostgreSQL database for persistent state and caching capabilities.

---

## 🏗️ System Architecture

```text
                        ┌──────────────────────┐
                        │      Frontend        │
                        │   (Next.js Web App)  │
                        └──────────┬───────────┘
                                   │
                           User Requests
                                   │
                                   ▼
                   ┌─────────────────────────────────┐
                   │      DevBridge Backend          │
                   │  (Google ADK Application)       │
                   └──────────┬──────────────────────┘
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
   Agent Layer         Shared Tool Layer     User Progress Layer
  (Planner, Discovery, (GitHub APIs, DB       (Mentorship stage
   Analysis, Response)  Cache, Sandbox)        & learning roadmap)
```

---

## 📂 Project Structure

```text
├── design/                     # Architectural and PRD documents
│   ├── agent-architecture.md   # Agent specification details
│   ├── security-architecture.md# Security, injection defense, and isolation design
│   └── system-architecture.md  # Component layout and data flows
│
└── devbridge-agent/            # Core backend agent code
    ├── app/
    │   ├── agents/             # Agent definitions & security configurations
    │   ├── models/             # Pydantic schemas for state & outputs
    │   └── workflow/           # State graph nodes & builder
    └── tests/                  # Integration and unit tests
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.12+
* [uv](https://github.com/astral-sh/uv) (recommended Python package manager)

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   cd devbridge-agent
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   uv sync
   ```

### Configuration
Create a `.env` file at the root of `devbridge-agent/` and set up the following environment variables:

```env
# GitHub Token (for repository code inspection)
GITHUB_TOKEN="your_github_pat_here"

# Google AI Studio API Key (for LLM reasoning)
GOOGLE_API_KEY="your_ai_studio_key_here"

# Database Connection (Neon Postgres connection string)
DATABASE_URL="postgresql://[USER]:[PASSWORD]@[NEON_HOST]/neondb?sslmode=require"

# Safe Gemma 4 Response Toggle (Set to True to use gemma-4-31b-it)
USE_GEMMA_FOR_RESPONSE=False
```

### Running Locally
To launch the interactive developer playground and trace workspace:
```bash
agents-cli playground
```
This starts the playground on `http://127.0.0.1:8080` where you can chat with the mentoring agent and view the step-by-step state-graph executions.

### Running Tests
To run the integration test suite:
```bash
uv run pytest tests/integration
```

---

## 🐳 Container Deployment

DevBridge includes a production-ready `Dockerfile` at the root of `devbridge-agent/`. You can build and run it using Docker:

```bash
# Build the Docker image
docker build -t devbridge-agent .

# Run the container locally
docker run -p 8080:8080 --env-file .env devbridge-agent
```
It is optimized for instant deployment to free-tier cloud containers (such as **Hugging Face Spaces**, **Render**, or **Railway**).

---

## 🔮 Future Expansion
* **IDE Extension**: We plan to develop an IDE extension (e.g., VS Code or Cursor) so that developers can get real-time mentoring, codebase explanations, and execution instructions for contributing to open-source repositories directly within their active workspace.
