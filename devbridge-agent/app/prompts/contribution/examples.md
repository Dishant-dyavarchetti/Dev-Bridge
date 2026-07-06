Input Repository Data:
- Readme/Contributing: "Use poetry. Run pytest. Use black for formatting."

Output:
{
  "contribution_steps": [
    "Fork and clone the repository.",
    "Install dependencies using Poetry.",
    "Create a new branch for your feature.",
    "Make code changes, adhering to code style.",
    "Run tests and ensure they pass.",
    "Submit a pull request targeting the main branch."
  ],
  "pr_guidelines": "Submit PR targeting the main branch. Ensure CI builds pass and tests are green.",
  "code_style": "Formatting is enforced using Black. Run `poetry run black .` before committing.",
  "testing_setup": "Run tests using pytest: `poetry run pytest`",
  "setup_instructions": "Install Poetry first, then run `poetry install` in the project root.",
  "summary": "Mentored on contribution guidelines for the project.",
  "confidence": {
    "level": "HIGH",
    "score": 0.95,
    "reasoning": "Found clear documentation on package manager, testing library, and formatter."
  }
}
