# Agent Architecture

# DevBridge

**Version:** 1.1

**Status:** Draft

**Last Updated:** 29 June 2026

---

# 1. Purpose

This document defines the AI agents that make up the DevBridge mentorship platform.

Each agent has a clearly defined responsibility and collaborates through workflow orchestration rather than direct communication.

The objective of this architecture is to keep every agent focused on a single domain of expertise while enabling the system to solve complex mentoring tasks in a modular and scalable manner.

---

# 2. Design Principles

The agent architecture follows the principles below:

- Single Responsibility Principle
- Planner-based orchestration
- Shared tool ecosystem
- Stateless reasoning
- Persistent user progress managed outside the agents
- Shared DevBridge State (Graph State)
- Modular and extensible design

---

# 3. Agent Overview

The DevBridge MVP consists of **six specialized AI agents** coordinated by the workflow engine.

```text
                                   User
                                     │
                                     ▼
                              Planner Agent
                                     │
                    Existing Session? (Condition)
                       ┌─────────────┴─────────────┐
                       │                           │
                      YES                         NO
                       │                           │
                       ▼                           ▼
             Resume User Progress          Repository Provided?
                  (Service)                (Condition)
                       │                 ┌──────────┴──────────┐
                       │                 │                     │
                       ▼                YES                   NO
                       │                 │                     │
                       │                 ▼                     ▼
                       │        Repository Analysis     Repository Discovery
                       │              Agent                 Agent
                       │                 │                     │
                       └─────────────────┴──────────────┬──────┘
                                                        ▼
                                             Repository Context Ready
                                                        │
                                                        ▼
                                                 Parallel Execution
                                             ┌──────────┴──────────┐
                                             ▼                     ▼
                              Contribution Mentor Agent   Issue Recommendation Agent
                                             │                     │
                                             └──────────┬──────────┘
                                                        ▼
                                             Response Composer Agent
                                                        │
                                                        ▼
                                            Update User Progress
                                                   (Service)
                                                        │
                                                        ▼
                                                       User
```

The **Planner Agent** is the entry point for every conversation.

Specialized agents never communicate directly with one another.

Instead, every agent reads from and writes to the shared **DevBridge State**, which is managed by the GraphFlow runtime.

---

# 4. Agent Specifications

## 4.1 Planner Agent

### Mission

Serve as the central coordinator for DevBridge.

### Responsibilities

- Understand user intent.
- Determine the appropriate workflow.
- Decide which specialized agents should execute.
- Coordinate GraphFlow execution.
- Manage conversation flow.

### Input

- User message
- Conversation context
- User progress

### Output

- Workflow execution plan
- Updated DevBridge State

---

## 4.2 Repository Discovery Agent

### Mission

Help users discover suitable open-source repositories.

### Responsibilities

- Recommend repositories based on user interests.
- Match repositories to experience level.
- Explain recommendation rationale.
- Suggest multiple contribution opportunities.

### Input

- User interests
- Programming language
- Experience level
- Contribution goals

### Output

- Ranked repository recommendations
- Recommendation explanations

---

## 4.3 Repository Analysis Agent

### Mission

Understand and explain an unfamiliar repository.

### Responsibilities

- Analyze repository structure.
- Explain project architecture.
- Identify technologies.
- Explain important folders.
- Identify project entry points.
- Summarize repository documentation.

### Input

- Repository

### Output

- Repository overview
- Architecture summary
- Technical insights

---

## 4.4 Contribution Mentor Agent

### Mission

Guide users through the repository's contribution process.

### Responsibilities

- Explain repository contribution rules.
- Interpret CONTRIBUTING documentation.
- Explain Git workflows.
- Guide repository setup.
- Explain repository-specific practices.
- Mentor users throughout the contribution journey.

### Input

- Repository
- User progress
- Conversation context

### Output

- Personalized contribution guide
- Repository setup instructions
- Contribution roadmap
- Recommended next action

---

## 4.5 Issue Recommendation Agent

### Mission

Recommend suitable issues for contribution.

### Responsibilities

- Analyze repository issues.
- Recommend beginner-friendly issues.
- Match issues to user experience.
- Estimate issue complexity.
- Generate an implementation roadmap.

### Input

- Repository
- User experience
- User goals

### Output

- Ranked issue recommendations
- Difficulty assessment
- Suggested implementation plan

---

## 4.6 Response Composer Agent

### Mission

Generate a unified mentoring response by combining the outputs of all completed agents.

### Responsibilities

- Read the completed DevBridge State.
- Combine repository analysis, contribution guidance, and issue recommendations.
- Remove duplicate information.
- Organize the response into a logical mentoring sequence.
- Produce the final response shown to the user.

### Input

- Repository analysis
- Contribution guidance
- Issue recommendations
- Conversation context
- User progress

### Output

- Final mentoring response

---

# 5. Agent Collaboration

The Planner Agent coordinates the complete mentoring workflow.

Execution sequence:

1. Receive user request.
2. Determine user intent.
3. Execute the required workflow.
4. Invoke specialized agents.
5. Each agent reads from and writes to the shared DevBridge State.
6. Wait for all required agent outputs.
7. Invoke the Response Composer Agent.
8. Persist user progress.
9. Return the final response.

Agents never invoke one another directly.

All collaboration occurs through the shared DevBridge State managed by the workflow engine.

---

# 6. Shared Capabilities

All agents access reusable platform capabilities through shared tools.

Examples include:

- Repository retrieval
- GitHub interaction
- Repository analysis
- Contribution parsing
- User progress retrieval
- Repository search

The implementation of these tools is defined separately in the Tools document.

---

# 7. Future Agents

The architecture supports additional specialized agents without redesigning the system.

Potential future agents include:

- Pull Request Review Agent
- Documentation Agent
- Security Advisor Agent
- Dependency Analysis Agent
- Community Recommendation Agent
- Organization Onboarding Agent
- Code Quality Agent
- Testing Assistant Agent

---

# 8. Guiding Philosophy

Each AI agent behaves like a specialist within an engineering organization.

- **Planner Agent** → Project Manager
- **Repository Discovery Agent** → Technical Recruiter
- **Repository Analysis Agent** → Software Architect
- **Contribution Mentor Agent** → Senior Open Source Mentor
- **Issue Recommendation Agent** → Technical Lead
- **Response Composer Agent** → Engineering Editor

The agents never communicate directly with one another.

Instead, every agent contributes structured knowledge to the shared **DevBridge State**, allowing the GraphFlow runtime to orchestrate the complete mentoring experience.

This design promotes modularity, scalability, testability, and clean separation of responsibilities.
