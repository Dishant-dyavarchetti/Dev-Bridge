# State Model

# DevBridge

**Version:** 1.0

**Status:** Draft

**Last Updated:** 29 June 2026

---

# 1. Purpose

The **DevBridge State** is the central data model shared across the entire DevBridge workflow.

Every GraphFlow node, AI agent, tool, and service interacts with the same state object.

The state serves as the single source of truth throughout the execution of a mentoring session.

This document defines the structure, ownership, and lifecycle of the DevBridge State.

---

# 2. Design Principles

The state model follows these principles:

- Single Source of Truth
- Strongly Typed
- Shared Across All Agents
- Immutable Ownership
- Separation of Runtime and Persistent Data
- Framework Independent

---

# 3. High-Level Structure

```text
DevBridgeState
│
├── UserState
├── SessionState
├── IntentState
├── RepositoryState
├── ContributionState
├── IssueState
├── ProgressState
├── RuntimeState
└── ResponseState
```

Each section has a clearly defined responsibility.

---

# 4. State Components

## 4.1 UserState

Represents the user's profile and preferences.

### Fields

- user_id
- github_username
- experience_level
- preferred_languages
- interests
- preferred_frameworks

### Ownership

Loaded by the User Progress Service.

Readable by every agent.

---

## 4.2 SessionState

Represents the current mentoring session.

### Fields

- session_id
- conversation_id
- current_stage
- current_repository
- current_issue
- started_at
- updated_at

### Ownership

Managed by the GraphFlow runtime.

---

## 4.3 IntentState

Stores the Planner Agent's interpretation of the user's request.

### Fields

- detected_intent
- workflow_type
- requires_repository_discovery
- requires_repository_analysis
- requires_issue_recommendation

### Ownership

Written only by the Planner Agent.

Read by the workflow engine.

---

## 4.4 RepositoryState

Contains repository-specific knowledge.

### Fields

- repository_name
- repository_url
- description
- primary_language
- technologies
- architecture_summary
- important_directories
- entry_points
- readme_summary

### Ownership

Written only by the Repository Analysis Agent.

Read by Contribution Mentor and Issue Recommendation agents.

---

## 4.5 ContributionState

Contains mentoring information related to contributing.

### Fields

- contribution_rules
- setup_steps
- git_workflow
- repository_guidelines
- contribution_roadmap
- recommended_next_step

### Ownership

Written only by the Contribution Mentor Agent.

---

## 4.6 IssueState

Contains issue recommendations.

### Fields

- recommended_issues
- selected_issue
- issue_difficulty
- implementation_plan
- estimated_completion_time

### Ownership

Written only by the Issue Recommendation Agent.

---

## 4.7 ProgressState

Represents the user's long-term mentoring progress.

### Fields

- completed_stages
- current_stage
- repositories_explored
- repositories_contributed
- contribution_history
- last_completed_action

### Ownership

Loaded and saved by the User Progress Service.

Readable by all agents.

---

## 4.8 RuntimeState

Contains temporary workflow execution data.

### Fields

- current_node
- completed_nodes
- active_parallel_branches
- failed_node
- execution_status

### Ownership

Managed by the GraphFlow runtime.

Never persisted.

---

## 4.9 ResponseState

Stores the final response returned to the frontend.

### Fields

- response_markdown
- response_sections
- suggested_actions
- follow_up_questions

### Ownership

Written only by the Response Composer Agent.

---

# 5. Ownership Matrix

| State             | Written By                 | Read By                                                      |
| ----------------- | -------------------------- | ------------------------------------------------------------ |
| UserState         | User Progress Service      | All Agents                                                   |
| SessionState      | Workflow Runtime           | All Agents                                                   |
| IntentState       | Planner Agent              | Workflow Runtime                                             |
| RepositoryState   | Repository Analysis Agent  | Contribution Mentor, Issue Recommendation, Response Composer |
| ContributionState | Contribution Mentor Agent  | Response Composer                                            |
| IssueState        | Issue Recommendation Agent | Response Composer                                            |
| ProgressState     | User Progress Service      | All Agents                                                   |
| RuntimeState      | Workflow Runtime           | Workflow Runtime                                             |
| ResponseState     | Response Composer Agent    | Frontend                                                     |

---

# 6. State Lifecycle

```text
User Request
      │
      ▼
Load User Progress
      │
      ▼
Initialize DevBridgeState
      │
      ▼
Planner Agent
      │
      ▼
Workflow Execution
      │
      ▼
Specialized Agents
      │
      ▼
Response Composer
      │
      ▼
Persist Progress
      │
      ▼
Return Response
```

---

# 7. Persistence Strategy

The following sections are persisted across sessions:

- UserState
- ProgressState

The following sections are temporary:

- SessionState
- IntentState
- RepositoryState
- ContributionState
- IssueState
- RuntimeState
- ResponseState

Temporary state exists only for the lifetime of the workflow execution.

---

# 8. Architectural Rules

The following rules govern the DevBridge State:

1. Every AI agent receives the same DevBridgeState object.
2. Every AI agent updates only the section it owns.
3. AI agents never overwrite another agent's data.
4. Agents never communicate directly with one another.
5. Communication occurs only through the shared DevBridge State.
6. Services may load or persist portions of the state.
7. The GraphFlow runtime manages workflow execution but does not perform AI reasoning.

---

# 9. Future Extensions

The state model is designed to support future additions without breaking existing workflows.

Potential future sections include:

- ReviewState
- SecurityState
- DocumentationState
- AnalyticsState
- TeamState

New sections should follow the same ownership model, where a single component is responsible for writing each state while other components consume it in a read-only manner.
