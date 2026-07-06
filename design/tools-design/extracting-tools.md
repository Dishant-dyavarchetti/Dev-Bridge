# Knowledge Extraction Layer

# DevBridge

**File:** `extracting-tools.md`

**Version:** 1.0

**Status:** Draft

**Last Updated:** 30 June 2026

---

# 1. Purpose

The Knowledge Extraction Layer is responsible for transforming raw repository artifacts into structured knowledge objects.

It serves as the bridge between external repositories and the AI reasoning layer.

Extraction tools never perform reasoning or invoke language models.

Their responsibility is limited to extracting, parsing, normalizing, and structuring repository information.

The generated knowledge objects are stored in the **DevBridgeState** and become the primary input for all AI agents.

---

# 2. Design Principles

Every extraction tool follows these principles.

- Deterministic Execution
- No AI Reasoning
- Single Responsibility
- Framework Independent
- Reusable
- Testable
- Strongly Typed Outputs

---

# 3. Extraction Architecture

```text
                    Git Repository
                          │
                          ▼
                 Repository Artifacts
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 Documentation      Configuration      Source Code
     Artifacts         Artifacts         Artifacts
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
              Knowledge Extraction Layer
                          │
                          ▼
                 Structured Knowledge Objects
                          │
                          ▼
                   DevBridgeState
                          │
                          ▼
                Understanding Agents
```

---

# 4. Repository Artifacts

Repository artifacts represent every source of information available inside a repository.

## Documentation Artifacts

- README.md
- CONTRIBUTING.md
- LICENSE
- CHANGELOG.md
- CODE_OF_CONDUCT.md
- SECURITY.md
- Wiki pages
- Documentation directory

---

## Configuration Artifacts

- package.json
- package-lock.json
- pnpm-lock.yaml
- yarn.lock
- pyproject.toml
- requirements.txt
- Dockerfile
- docker-compose.yml
- Makefile
- .env.example
- GitHub Actions workflows

---

## Source Code Artifacts

- Source directories
- Test directories
- API routes
- Components
- Services
- Models
- Utilities
- Middleware
- Scripts

---

## Repository Metadata

- Repository information
- Branches
- Releases
- Issues
- Pull Requests
- Labels
- Topics
- Contributors

---

# 5. Knowledge Objects

Every extraction tool produces a strongly typed knowledge object.

| Knowledge Object       | Description                           |
| ---------------------- | ------------------------------------- |
| RepositoryKnowledge    | Repository metadata and statistics    |
| ReadmeKnowledge        | README structure and content          |
| ContributionKnowledge  | Contribution rules and workflows      |
| DocumentationKnowledge | Additional project documentation      |
| DependencyKnowledge    | Dependencies and package information  |
| BuildKnowledge         | Build system and scripts              |
| ContainerKnowledge     | Docker and container configuration    |
| WorkflowKnowledge      | GitHub Actions and CI/CD workflows    |
| ArchitectureKnowledge  | Repository structure and entry points |
| CodebaseKnowledge      | Symbols, modules, and relationships   |
| IssueKnowledge         | Repository issues and metadata        |

These knowledge objects are stored inside the DevBridgeState.

---

# 6. Extraction Tool Contract

Every extractor follows the same contract.

## Purpose

Describe the responsibility of the extractor.

## Input Artifacts

Repository files consumed by the extractor.

## Extraction Method

Deterministic techniques used for parsing.

## Output Schema

Knowledge object generated.

## Consumers

AI agents that consume the extracted knowledge.

---

# 7. Extraction Tools

---

## README Extractor

### Purpose

Extract project overview, installation instructions, usage information, features, examples, and documentation structure.

### Input Artifacts

- README.md

### Extraction Method

- Markdown Parsing
- Heading Detection
- List Extraction
- Code Block Extraction
- Link Extraction

### Output Schema

ReadmeKnowledge

### Consumers

- Repository Analysis Agent
- Learning Mentor
- Response Composer

---

## Contribution Extractor

### Purpose

Extract repository contribution guidelines.

### Input Artifacts

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md

### Extraction Method

- Markdown Parsing
- Section Detection
- Rule Extraction

### Output Schema

ContributionKnowledge

### Consumers

- Contribution Mentor
- Response Composer

---

## Dependency Extractor

### Purpose

Extract project dependencies.

### Input Artifacts

- package.json
- pyproject.toml
- requirements.txt
- composer.json
- go.mod
- Cargo.toml

### Extraction Method

- JSON Parsing
- TOML Parsing
- YAML Parsing
- Text Parsing

### Output Schema

DependencyKnowledge

### Consumers

- Repository Analysis Agent
- Tech Stack Mentor

---

## Build Configuration Extractor

### Purpose

Extract build and execution configuration.

### Input Artifacts

- package.json
- Makefile
- Dockerfile
- docker-compose.yml

### Extraction Method

- Configuration Parsing

### Output Schema

BuildKnowledge

### Consumers

- Repository Analysis Agent
- Contribution Mentor

---

## CI/CD Workflow Extractor

### Purpose

Extract repository automation workflows.

### Input Artifacts

- .github/workflows/

### Extraction Method

- YAML Parsing

### Output Schema

WorkflowKnowledge

### Consumers

- Repository Analysis Agent

---

## Repository Structure Extractor

### Purpose

Extract the repository hierarchy.

### Input Artifacts

- Complete Repository Tree

### Extraction Method

- Directory Traversal
- File Classification

### Output Schema

ArchitectureKnowledge

### Consumers

- Repository Analysis Agent
- Learning Mentor

---

## Source Code Extractor

### Purpose

Extract structural information from the codebase.

### Input Artifacts

- Source Code

### Extraction Method

- AST Parsing
- Symbol Extraction
- Import Graph Analysis

### Output Schema

CodebaseKnowledge

### Consumers

- Repository Analysis Agent
- Architecture Mentor

---

## GitHub Metadata Extractor

### Purpose

Extract repository metadata.

### Input Artifacts

- GitHub Repository API

### Extraction Method

- GitHub REST / GraphQL APIs

### Output Schema

RepositoryKnowledge

### Consumers

- Repository Discovery Agent
- Repository Analysis Agent

---

## Issue Extractor

### Purpose

Extract repository issue metadata.

### Input Artifacts

- GitHub Issues

### Extraction Method

- GitHub API

### Output Schema

IssueKnowledge

### Consumers

- Issue Recommendation Agent

---

# 8. Extraction Workflow

```text
GitHub Repository
        │
        ▼
Integration Layer
        │
        ▼
Repository Artifacts
        │
        ▼
Extraction Tool
        │
        ▼
Knowledge Object
        │
        ▼
DevBridgeState
```

---

# 9. Architectural Rules

1. Extraction tools never invoke LLMs.
2. Extraction tools never generate explanations.
3. Extraction tools never modify workflow execution.
4. Extraction tools only consume repository artifacts.
5. Extraction tools always return typed knowledge objects.
6. Extraction tools are reusable across multiple AI agents.
7. AI agents consume knowledge objects instead of raw repository files.

---

# 10. Future Extensions

Future extraction capabilities may include:

- UML Diagram Extraction
- Database Schema Extraction
- OpenAPI Specification Extraction
- GraphQL Schema Extraction
- Security Configuration Extraction
- Infrastructure-as-Code Extraction
- Kubernetes Manifest Extraction
- Terraform Configuration Extraction

The architecture allows new extraction tools to be added without modifying existing AI agents.
