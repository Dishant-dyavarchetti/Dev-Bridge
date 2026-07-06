# Understanding & Reasoning Layer

# DevBridge

**File:** `understanding-agents.md`

**Version:** 1.0

**Status:** Draft

**Last Updated:** 30 June 2026

---

# 1. Purpose

The Understanding & Reasoning Layer transforms structured knowledge into personalized mentorship.

Unlike the Knowledge Extraction Layer, which extracts deterministic information from repository artifacts, the Understanding & Reasoning Layer performs contextual reasoning using Large Language Models (LLMs).

The primary objective of this layer is to help developers understand unfamiliar repositories, navigate contribution workflows, and confidently participate in open-source projects.

This layer represents the intelligence of DevBridge.

---

# 2. Separation of Responsibilities

DevBridge separates deterministic processing from AI reasoning.

```text
Repository
     │
     ▼
Knowledge Extraction Layer
(Deterministic)
     │
     ▼
Knowledge Objects
     │
     ▼
DevBridgeState
     │
     ▼
Understanding & Reasoning Layer
(LLM)
     │
     ▼
Response Composer
     │
     ▼
User
```

This separation ensures:

- AI focuses on reasoning instead of parsing files.
- Extracted knowledge is reusable across multiple agents.
- Every reasoning decision is grounded in structured evidence.

---

# 3. Design Principles

Every reasoning agent follows these principles.

- Single Responsibility Principle
- Consume Knowledge Objects only
- Never parse raw repository artifacts
- Never directly communicate with other agents
- Read and update only its owned section of DevBridgeState
- Produce structured outputs
- Support evidence-based reasoning

---

# 4. Reasoning Agents

The DevBridge MVP consists of six specialized reasoning agents.

```
Planner Agent

Repository Discovery Agent

Repository Analysis Agent

Contribution Mentor Agent

Issue Recommendation Agent

Response Composer Agent
```

Each agent specializes in a specific mentoring responsibility.

---

# 5. Agent Specifications

---

## 5.1 Planner Agent

### Mission

Coordinate the complete mentorship workflow.

### Responsibilities

- Understand user intent.
- Select the appropriate workflow.
- Decide which agents should execute.
- Manage workflow execution.
- Route execution through GraphFlow.

### Knowledge Consumed

- UserState
- SessionState
- ProgressState

### State Updated

- IntentState

### Outputs

- Workflow execution plan

---

## 5.2 Repository Discovery Agent

### Mission

Help users discover suitable repositories.

### Responsibilities

- Recommend repositories.
- Match repositories with user interests.
- Match repositories with user experience.
- Explain recommendation rationale.

### Knowledge Consumed

- RepositoryKnowledge
- UserState
- ProgressState

### State Updated

- RepositoryState

### Outputs

- Ranked repository recommendations

---

## 5.3 Repository Analysis Agent

### Mission

Help users understand unfamiliar repositories.

### Responsibilities

- Explain repository purpose.
- Explain architecture.
- Explain project organization.
- Explain technologies.
- Explain setup process.
- Explain project entry points.

### Knowledge Consumed

- RepositoryKnowledge
- ReadmeKnowledge
- DependencyKnowledge
- ArchitectureKnowledge
- BuildKnowledge
- WorkflowKnowledge

### State Updated

- RepositoryState

### Outputs

- Repository explanation
- Architecture summary
- Technology overview
- Setup guidance

---

## 5.4 Contribution Mentor Agent

### Mission

Mentor developers throughout the contribution process.

### Responsibilities

- Explain contribution workflow.
- Explain Git practices.
- Explain repository-specific rules.
- Recommend next actions.
- Guide users through contribution milestones.

### Knowledge Consumed

- ContributionKnowledge
- DocumentationKnowledge
- RepositoryState
- ProgressState

### State Updated

- ContributionState

### Outputs

- Contribution roadmap
- Personalized mentoring guidance
- Recommended next step

---

## 5.5 Issue Recommendation Agent

### Mission

Recommend appropriate contribution opportunities.

### Responsibilities

- Recommend beginner-friendly issues.
- Match issues to user experience.
- Explain issue complexity.
- Explain implementation approach.
- Generate implementation guidance.

### Knowledge Consumed

- IssueKnowledge
- RepositoryState
- ProgressState

### State Updated

- IssueState

### Outputs

- Ranked issue recommendations
- Difficulty assessment
- Implementation roadmap

---

## 5.6 Response Composer Agent

### Mission

Generate a unified mentoring response.

### Responsibilities

- Read completed DevBridgeState.
- Combine outputs from all reasoning agents.
- Remove duplicated information.
- Organize the mentoring response.
- Produce the final response returned to the user.

### Knowledge Consumed

- RepositoryState
- ContributionState
- IssueState
- ProgressState

### State Updated

- ResponseState

### Outputs

- Final mentoring response

---

# 6. Reasoning Workflow

```text
Knowledge Objects
        │
        ▼
Planner Agent
        │
        ▼
Repository Discovery
        │
        ▼
Repository Analysis
        │
        ▼
Parallel Execution
 ┌──────────────┴──────────────┐
 ▼                             ▼
Contribution Mentor     Issue Recommendation
        │                      │
        └──────────┬───────────┘
                   ▼
          Response Composer
                   │
                   ▼
                User
```

---

# 7. Agent Response Contract

Every reasoning agent produces a structured response.

```text
Reasoning Result

├── Summary
├── Explanation
├── Recommendations
├── Evidence
├── Confidence
└── Next Actions
```

These responses are stored within the DevBridgeState and consumed by the Response Composer.

---

# 8. Evidence-Based Reasoning

Every explanation generated by a reasoning agent should be grounded in extracted knowledge.

Examples of evidence include:

- README.md
- CONTRIBUTING.md
- package.json
- pyproject.toml
- Dockerfile
- Repository metadata
- Issue metadata

Reasoning agents should avoid unsupported assumptions whenever possible.

---

# 9. Architectural Rules

1. Agents never parse raw repository artifacts.
2. Agents consume Knowledge Objects from the DevBridgeState.
3. Agents never communicate directly with one another.
4. Every agent updates only the state it owns.
5. Every reasoning result should include supporting evidence.
6. The Response Composer is solely responsible for generating the final user-facing response.

---

# 10. Future Evolution

The architecture is intentionally modular.

Future versions of DevBridge may decompose larger reasoning agents into smaller domain-specific mentors, such as:

- Architecture Mentor
- Documentation Mentor
- Tech Stack Mentor
- Learning Mentor

The current MVP keeps these responsibilities consolidated within the existing six-agent architecture to reduce implementation complexity while preserving a clear path for future expansion.

---

# 11. Design Philosophy

The Understanding & Reasoning Layer is designed to emulate an experienced engineering team.

Each agent contributes specialized expertise while remaining focused on a single domain of responsibility.

Rather than replacing the developer, DevBridge acts as a mentor—helping users understand unfamiliar codebases, learn open-source practices, and confidently make meaningful contributions.

This architecture emphasizes guidance, explainability, and collaboration over autonomous decision-making, ensuring that every recommendation is grounded in extracted knowledge and tailored to the user's experience level.
