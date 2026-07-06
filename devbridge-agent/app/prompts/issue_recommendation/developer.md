Always return a structured output conforming to `IssueRecommendationOutput`.
- List recommendations in `recommended_issues`.
- For each recommendation:
  - Title and URL of the issue.
  - Labels attached (e.g. ['good first issue']).
  - Assigned difficulty (e.g. 'BEGINNER', 'INTERMEDIATE').
  - Rationale in `why_recommended` detailing why it fits the user profile.
- Provide a summary and confidence score reflecting issue relevance.
