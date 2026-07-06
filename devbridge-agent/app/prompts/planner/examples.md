User Request: "Show me some good Python projects to get started with open source. I like web frameworks."
Output:
{
  "summary": "User is looking for Python web framework repository recommendations to begin open source contributions.",
  "intent": "DISCOVER_REPOSITORIES",
  "confidence": {
    "level": "HIGH",
    "score": 0.95,
    "reasoning": "Explicit request for repository recommendations matching specific language (Python) and domain (web frameworks) preferences."
  },
  "required_agents": ["repository_discovery_agent"],
  "execution_plan": ["Analyze user preferences and skill level.", "Query and discover relevant open-source repositories.", "Format repository recommendations with reasons."]
}

User Request: "How do I set up and run tests for fast-api?"
Output:
{
  "summary": "User wants instructions on setting up fast-api project locally and running its test suite.",
  "intent": "CONTRIBUTE",
  "confidence": {
    "level": "HIGH",
    "score": 0.9,
    "reasoning": "Setting up the project and running tests are standard parts of the contribution workflow."
  },
  "required_agents": ["repository_analysis_agent", "contribution_mentor_agent"],
  "execution_plan": ["Analyze repository setup and test configs.", "Provide step-by-step developer guidelines for setup and testing."]
}
