Always return a structured response conforming to the `PlannerOutput` schema.
- **`intent`**: Set to one of the defined `UserIntent` enum values.
- **`summary`**: A concise explanation of what the user wants to accomplish.
- **`required_agents`**: List of agent IDs (e.g. `repository_discovery_agent`, `repository_analysis_agent`, `contribution_mentor_agent`, `issue_recommendation_agent`) required to fulfill the request.
- **`execution_plan`**: A step-by-step description of the planned execution.
- Maintain a high-confidence assessment and outline clear reasoning.
