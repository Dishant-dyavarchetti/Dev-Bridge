# System Architecture

# DevBridge

**Version:** 1.0

**Status:** Draft

**Last Updated:** 29 June 2026

---

# 1. Purpose

This document describes the high-level architecture of the DevBridge platform.

It defines the major system components, their responsibilities, and how they interact. This document intentionally avoids implementation details such as prompts, APIs, or internal agent logic.

---

# 2. High-Level Architecture

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
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                             ▼
                    External Services
                             │
          ┌──────────────────┴──────────────────┐
          │                                     │
      GitHub APIs                       Database
```

---

# 3. System Components

## 3.1 Frontend Layer

The frontend provides the user interface for interacting with DevBridge.

### Responsibilities

- User authentication
- Conversation interface
- Repository discovery interface
- Progress visualization
- Display learning roadmaps
- Display repository insights
- Display contribution guidance

The frontend does not perform AI reasoning.

---

## 3.2 Agent Layer

The Agent Layer contains specialized AI agents responsible for different mentoring tasks.

Each agent has a single responsibility.

The Agent Layer does not communicate directly with databases or external services.

Instead, agents interact through shared tools.

The detailed design of each agent is documented separately in the Agent Architecture document.

Its responsibilities include:

- Receiving user requests
- Coordinating AI agents
- Managing conversations
- Accessing tools
- Maintaining user progress
- Producing responses

---

## 3.3 Shared Tool Layer

The Tool Layer acts as the capability provider for all agents.

Examples include:

- GitHub interaction
- Repository analysis
- Contribution guideline parsing
- User progress management
- Repository search

Tools encapsulate external integrations so agents remain focused on reasoning.

---

## 3.4 User Progress Layer

The User Progress Layer stores the mentoring state for each user.

Its purpose is to maintain continuity across multiple sessions.

Examples of information stored include:

- Current repository
- Current issue
- Contribution progress
- Completed mentoring stages
- Learning roadmap progress

The system tracks mentorship progress rather than storing arbitrary conversation history.

---

## 3.5 External Services

External services provide information required by DevBridge.

Examples include:

- GitHub repositories
- Repository documentation
- GitHub Issues
- Pull Request metadata
- Persistent database

External services are accessed only through the Tool Layer.

---

# 4. Communication Principles

DevBridge follows the following architectural principles.

## Single Entry Point

All user requests enter through the frontend and are processed by the backend.

---

## Centralized Agent Coordination

One orchestration component coordinates all AI agents.

Individual agents do not communicate directly with the frontend.

---

## Tool-Based Integration

Agents never communicate directly with external services.

All external interactions occur through shared tools.

---

## Separation of Responsibilities

Each architectural layer has a single responsibility.

Frontend → User Experience

Backend → AI Coordination

Agents → Reasoning

Tools → External Capabilities

User Progress → Persistent Mentorship State

---

# 5. Scalability

The architecture is designed to support additional clients without changing the backend.

Potential future clients include:

- VS Code Extension
- Slack Bot
- Discord Bot
- GitHub App
- Command Line Interface

Each client communicates with the same backend application.

---

# 6. Guiding Principles

DevBridge is designed around the following architectural principles:

- Separation of Concerns
- Modular Agent Design
- Shared Tool Ecosystem
- Stateless Agent Reasoning
- Persistent User Progress
- Extensible Client Architecture

---

# 7. Out of Scope

This document does not define:

- Individual AI agents
- Agent prompts
- Workflow logic
- Tool implementations
- Database schema
- API contracts

These are documented in subsequent design documents.
