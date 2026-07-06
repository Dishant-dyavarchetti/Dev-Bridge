# Execution Component Matrix

# DevBridge

**Version:** 2.0

**Status:** Draft

**Last Updated:** 29 June 2026

---

# 1. Purpose

This document defines every execution component within the DevBridge runtime.

It specifies:

- Component category
- Responsibilities
- State interaction
- AI reasoning requirements
- Tool usage
- Service dependencies

This document serves as the implementation contract for the DevBridge GraphFlow runtime.

---

# 2. Architectural Component Types

DevBridge consists of five architectural component types.

| Component Type     | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| **State Model**    | The shared data contract exchanged between every execution component.  |
| **GraphFlow Node** | Controls workflow execution and orchestration.                         |
| **AI Agent**       | Performs reasoning using an LLM.                                       |
| **Tool**           | Executes deterministic operations and interacts with external systems. |
| **Service**        | Manages infrastructure, persistence, and runtime resources.            |

---

# 3. Execution Component Matrix

| Component                      | Type           | Primary Responsibility                                         | Reads State                                                   | Writes State      | Uses LLM | Uses Tools                   | Uses Services         |
| ------------------------------ | -------------- | -------------------------------------------------------------- | ------------------------------------------------------------- | ----------------- | -------- | ---------------------------- | --------------------- |
| **DevBridgeState**             | State Model    | Shared workflow state exchanged across the runtime             | N/A                                                           | N/A               | ❌       | ❌                           | ❌                    |
| **Start Node**                 | GraphFlow Node | Initialize workflow execution                                  | ❌                                                            | SessionState      | ❌       | ❌                           | ❌                    |
| **Planner Agent**              | AI Agent       | Understand user intent and orchestrate execution               | UserState, SessionState, ProgressState                        | IntentState       | ✅       | ❌                           | ❌                    |
| **Existing Session Check**     | GraphFlow Node | Determine whether the user has an active mentoring session     | ProgressState                                                 | ❌                | ❌       | ❌                           | User Progress Service |
| **Resume Progress**            | Service        | Load previous mentoring progress                               | ProgressState                                                 | SessionState      | ❌       | Database                     | ✅                    |
| **Repository Provided Check**  | GraphFlow Node | Determine whether repository discovery is required             | IntentState                                                   | ❌                | ❌       | ❌                           | ❌                    |
| **Repository Discovery Agent** | AI Agent       | Recommend repositories matching the user's interests           | UserState, ProgressState                                      | RepositoryState   | ✅       | GitHub Search Tool           | ❌                    |
| **Repository Analysis Agent**  | AI Agent       | Analyze and understand repository structure                    | RepositoryState                                               | RepositoryState   | ✅       | Repository Tool, GitHub Tool | ❌                    |
| **Repository Context Ready**   | GraphFlow Node | Synchronize repository information before parallel execution   | RepositoryState                                               | RuntimeState      | ❌       | ❌                           | ❌                    |
| **Parallel Execution Node**    | GraphFlow Node | Execute independent branches concurrently                      | RepositoryState                                               | RuntimeState      | ❌       | ❌                           | ❌                    |
| **Contribution Mentor Agent**  | AI Agent       | Generate repository-specific contribution guidance             | RepositoryState, ProgressState                                | ContributionState | ✅       | Contribution Tool            | ❌                    |
| **Issue Recommendation Agent** | AI Agent       | Recommend suitable beginner-friendly issues                    | RepositoryState, ProgressState                                | IssueState        | ✅       | GitHub Issue Tool            | ❌                    |
| **Merge Node**                 | GraphFlow Node | Synchronize outputs from parallel branches                     | RepositoryState, ContributionState, IssueState                | RuntimeState      | ❌       | ❌                           | ❌                    |
| **Response Composer Agent**    | AI Agent       | Produce the final mentoring response using the completed state | RepositoryState, ContributionState, IssueState, ProgressState | ResponseState     | ✅       | ❌                           | ❌                    |
| **Update User Progress**       | Service        | Persist mentoring progress after workflow completion           | ProgressState, ResponseState                                  | ProgressState     | ❌       | Database                     | ✅                    |
| **End Node**                   | GraphFlow Node | Complete workflow execution                                    | ResponseState                                                 | ❌                | ❌       | ❌                           | ❌                    |

---

# 4. State Ownership Matrix

Each section of the DevBridge State has exactly one owner.

| State Section         | Owner                      | Read Access                                                  |
| --------------------- | -------------------------- | ------------------------------------------------------------ |
| **UserState**         | User Progress Service      | All AI Agents                                                |
| **SessionState**      | GraphFlow Runtime          | All AI Agents                                                |
| **IntentState**       | Planner Agent              | GraphFlow Runtime                                            |
| **RepositoryState**   | Repository Analysis Agent  | Contribution Mentor, Issue Recommendation, Response Composer |
| **ContributionState** | Contribution Mentor Agent  | Response Composer                                            |
| **IssueState**        | Issue Recommendation Agent | Response Composer                                            |
| **ProgressState**     | User Progress Service      | All AI Agents                                                |
| **RuntimeState**      | GraphFlow Runtime          | GraphFlow Runtime                                            |
| **ResponseState**     | Response Composer Agent    | Frontend                                                     |

Each state section has a **single writer** but may have **multiple readers**.

---

# 5. Component Interaction Rules

The following rules govern every execution component within DevBridge.

### Rule 1

Every execution component receives the same **DevBridgeState** instance.

---

### Rule 2

Each component may only modify the state that it owns.

---

### Rule 3

AI agents never communicate directly with one another.

All information exchange occurs through the shared **DevBridgeState**.

---

### Rule 4

GraphFlow nodes orchestrate execution but never perform AI reasoning.

---

### Rule 5

Tools perform deterministic operations only.

They never invoke AI models.

---

### Rule 6

Services manage infrastructure, persistence, and runtime resources.

They never perform AI reasoning.

---

### Rule 7

The Response Composer Agent is the only AI agent responsible for producing the final user-facing response.

---

# 6. Runtime Architecture

```text
                   DevBridge Runtime

                           │

                   DevBridgeState
                           │

        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼

 GraphFlow Nodes      AI Agents         Services

        │                  │                  │

        └──────────────┬───┴──────────────────┘
                       │
                       ▼

                     Tools

                       │

                       ▼

              External Systems
```

---

# 7. Execution Lifecycle

```text
START

↓

Initialize DevBridgeState

↓

Planner Agent

↓

GraphFlow Decision

↓

AI Agent

↓

Tool Execution

↓

Update DevBridgeState

↓

GraphFlow Decision

↓

Next AI Agent

↓

Response Composer Agent

↓

Persist User Progress

↓

END
```

---

# 8. Design Philosophy

DevBridge follows a layered execution architecture.

- **State Model** acts as the shared contract between all runtime components.
- **GraphFlow Nodes** orchestrate workflow execution.
- **AI Agents** perform reasoning and generate structured knowledge.
- **Tools** provide deterministic capabilities and external integrations.
- **Services** manage infrastructure, persistence, and runtime resources.

Each component has a single responsibility and communicates exclusively through the shared **DevBridgeState**.

This architecture promotes modularity, extensibility, maintainability, and framework independence while providing a clear separation between orchestration, reasoning, external capabilities, and persistent state.
