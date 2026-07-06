# Orchestration Layer

# DevBridge

**File:** `orchestration.md`

**Version:** 1.0

**Status:** Draft

**Last Updated:** 30 June 2026

---

# 1. Purpose

The Orchestration Layer coordinates the execution of the DevBridge mentorship workflow.

It is responsible for deciding **when** each reasoning agent executes, **which** tools are invoked, and **how** information flows through the shared `DevBridgeState`.

The Orchestration Layer does **not** perform AI reasoning.

Instead, it manages workflow execution using GraphFlow while delegating reasoning to specialized AI agents.

---

# 2. Responsibilities

The Orchestration Layer is responsible for:

- Initializing workflow execution
- Loading previous user progress
- Creating and managing the DevBridgeState
- Executing conditional branches
- Coordinating parallel execution
- Synchronizing parallel outputs
- Handling failures and retries
- Persisting user progress
- Returning the final response

---

# 3. Architectural Principles

The orchestration workflow follows these principles.

- Separation of orchestration and reasoning
- Shared DevBridgeState
- Stateless AI agents
- Deterministic workflow execution
- Support for resumable sessions
- Parallel execution where appropriate
- Extensible workflow graph

---

# 4. GraphFlow Overview

```text
                    START
                      │
                      ▼
             Initialize Session
                      │
                      ▼
              Load User Progress
                      │
                      ▼
               Planner Agent
                      │
              Intent Decision
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
Repository Provided?         Repository Discovery
         │                         │
         └────────────┬────────────┘
                      ▼
          Repository Analysis Agent
                      │
                      ▼
            Repository Context Ready
                      │
                      ▼
             Parallel Execution
          ┌───────────┴───────────┐
          ▼                       ▼
Contribution Mentor      Issue Recommendation
          │                       │
          └───────────┬───────────┘
                      ▼
               Merge Results
                      │
                      ▼
          Response Composer Agent
                      │
                      ▼
          Persist User Progress
                      │
                      ▼
                     END
```

---

# 5. Workflow Nodes

## Start Node

### Responsibility

Initialize workflow execution.

### Actions

- Receive user request.
- Create workflow context.
- Initialize runtime.

---

## Session Initialization

### Responsibility

Determine whether an existing mentoring session exists.

### Actions

- Load previous progress.
- Restore previous session if available.
- Create a new session otherwise.

---

## Planner Node

### Responsibility

Interpret user intent.

### Actions

- Read UserState.
- Read ProgressState.
- Produce IntentState.
- Determine execution path.

---

## Conditional Node

### Responsibility

Choose the appropriate workflow branch.

Possible decisions include:

- Repository already provided
- Repository discovery required
- Resume previous mentoring session

---

## Repository Discovery Node

Executed only when the user has not selected a repository.

Produces:

- Repository recommendations

---

## Repository Analysis Node

Analyzes repository knowledge objects and updates RepositoryState.

---

## Parallel Execution Node

Launches independent reasoning agents simultaneously.

Parallel branches:

- Contribution Mentor Agent
- Issue Recommendation Agent

Both branches operate on the same DevBridgeState but update different sections.

---

## Merge Node

Synchronizes outputs from parallel execution.

Responsibilities:

- Wait for all branches.
- Validate state consistency.
- Merge updated state.
- Continue workflow execution.

---

## Response Composer Node

Generates the final mentoring response.

Consumes:

- RepositoryState
- ContributionState
- IssueState
- ProgressState

Produces:

- ResponseState

---

## Persistence Node

Persist updated mentoring progress.

Actions:

- Save ProgressState.
- Save repository selection.
- Save completed stages.

---

## End Node

Return the final response to the client.

---

# 6. DevBridgeState Lifecycle

```text
User Request
      │
      ▼
Initialize DevBridgeState
      │
      ▼
Planner Updates IntentState
      │
      ▼
RepositoryState Updated
      │
      ▼
ContributionState Updated
      │
      ▼
IssueState Updated
      │
      ▼
ResponseState Generated
      │
      ▼
Persist ProgressState
      │
      ▼
Workflow Complete
```

---

# 7. Parallel Execution

The orchestration layer executes independent reasoning agents concurrently whenever possible.

Current parallel execution:

```text
RepositoryState
      │
      ▼
Parallel Node
 ┌──────────────┴──────────────┐
 ▼                             ▼
Contribution Mentor      Issue Recommendation
 │                             │
 └──────────────┬──────────────┘
                ▼
           Merge Node
```

Parallel execution reduces overall workflow latency while maintaining clear ownership of state.

---

# 8. State Synchronization

Every workflow node receives the same `DevBridgeState`.

Each reasoning agent updates only the state it owns.

The Merge Node validates and synchronizes these updates before continuing execution.

No agent may overwrite another agent's state.

---

# 9. Error Handling

The Orchestration Layer is responsible for handling execution failures.

Possible failure scenarios include:

- GitHub API unavailable
- Repository not found
- Missing documentation
- Network timeout
- Tool execution failure

Strategies include:

- Retry deterministic tool execution.
- Skip optional workflow branches.
- Continue with partial knowledge when safe.
- Surface meaningful errors to the Response Composer.

---

# 10. Session Resume

If a previous mentoring session exists, the orchestration layer restores the user's progress before executing additional reasoning.

The restored state includes:

- Selected repository
- Current mentoring stage
- Completed milestones
- Previous recommendations

This enables long-running mentoring sessions across multiple conversations.

---

# 11. Response Generation Flow

```text
RepositoryState
ContributionState
IssueState
ProgressState
        │
        ▼
Response Composer
        │
        ▼
ResponseState
        │
        ▼
Frontend
```

The Response Composer is the only component responsible for generating the final user-facing response.

---

# 12. Orchestration Rules

1. The Orchestration Layer never performs AI reasoning.
2. AI agents never orchestrate workflow execution.
3. Every workflow step receives the shared DevBridgeState.
4. Parallel branches may update different state sections simultaneously.
5. Workflow execution is deterministic.
6. User progress is persisted only after successful workflow completion.
7. The orchestration layer coordinates execution but never interprets repository knowledge.

---

# 13. Future Enhancements

The orchestration design supports future extensions without redesigning the workflow.

Potential enhancements include:

- Dynamic agent selection
- Multi-repository workflows
- Multi-step contribution plans
- Human approval checkpoints
- Background long-running tasks
- Streaming intermediate updates
- A2A integration for external specialist agents
- Distributed GraphFlow execution

---

# 14. Design Philosophy

The Orchestration Layer acts as the project manager of the DevBridge platform.

It coordinates specialized reasoning agents, deterministic extraction tools, and persistent services while maintaining a consistent workflow through the shared DevBridgeState.

By separating orchestration from reasoning, DevBridge remains modular, extensible, and easier to test, while providing users with a seamless mentoring experience from repository discovery to successful open-source contribution.
