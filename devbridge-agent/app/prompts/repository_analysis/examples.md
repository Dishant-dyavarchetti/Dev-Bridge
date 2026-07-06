Input Codebase Info:
- Files: ['app/main.py', 'app/routes.py', 'tests/test_main.py', 'requirements.txt', 'README.md']
- Readme: "FastAPI App for user management"

Output:
{
  "repository_name": "user-management-api",
  "repository_url": "https://github.com/example/user-management-api",
  "description": "A FastAPI web application for managing users.",
  "primary_language": "Python",
  "technologies": ["FastAPI", "Uvicorn", "pytest"],
  "architecture_summary": "Uses a standard single-module web server layout with routing separated from the main startup code.",
  "important_directories": [
    "app: Contains the source code of the web application",
    "tests: Contains unit and integration tests"
  ],
  "entry_points": ["app/main.py"],
  "readme_summary": "FastAPI App for user management. Outlines setup and API endpoints.",
  "summary": "Successfully analyzed user-management-api codebase layout.",
  "confidence": {
    "level": "HIGH",
    "score": 0.95,
    "reasoning": "Standard structure matches expected patterns with clear file organization."
  }
}
