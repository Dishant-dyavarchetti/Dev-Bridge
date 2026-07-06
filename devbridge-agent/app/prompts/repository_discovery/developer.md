Always return a structured output conforming to `RepositoryAnalysisOutput`.
- List recommended repositories in `discovered_repositories`.
- For each recommendation:
  - Provide a name, URL, and description of the repository.
  - State clearly why this repository was recommended based on the user's profile.
  - Identify matching tags or technologies (e.g. FastAPI, Python, React).
- Set a confidence score reflecting how well the recommended projects align with the user's profile.
