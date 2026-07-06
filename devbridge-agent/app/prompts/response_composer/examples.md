Input Data:
- Repository Output: user-management-api overview
- Contribution Output: poetry install, pytest guidelines
- Issue Output: docstring typo issue recommendation

Output:
{
  "sections": [
    "# Welcome to DevBridge Mentoring!\n\nWe matched you with the **user-management-api** project.",
    "## Project Overview\n\nA FastAPI user management API with source code in `/app` and entry point `/app/main.py`.",
    "## Setup & Test Instructions\n\n> [!IMPORTANT]\n> Enforce styling by running Black formatter.\n\n```bash\n# Install dependencies\npoetry install\n\n# Run tests\npoetry run pytest\n```",
    "## Recommended Issues\n\n* **Fix typo in docstring**\n  * URL: https://github.com/example/repo/issues/1\n  * Why: Fits your beginner skill level perfectly."
  ],
  "summary": "Mentoring guide successfully composed.",
  "confidence": {
    "level": "HIGH",
    "score": 0.95,
    "reasoning": "Fully aggregated all component agent outputs into markdown."
  }
}
