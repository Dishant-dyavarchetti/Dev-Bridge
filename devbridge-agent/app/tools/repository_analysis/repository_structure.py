"""
Deterministic repository structure analyzer.
"""


class RepositoryStructureAnalyzer:
    """
    Utility for analyzing the directory tree and layout of a repository.
    Strictly provides deterministic metadata based on path structures.
    """

    IMPORTANT_DIRECTORIES = {
        "src": "Source Code",
        "tests": "Test Suite",
        "test": "Test Suite",
        "docs": "Documentation",
        "scripts": "Utility Scripts",
        "examples": "Example Code",
        "packages": "Monorepo Packages",
        "apps": "Monorepo Applications",
        ".github": "GitHub Actions / Configs",
        "public": "Public Assets",
        "dist": "Build Output",
        "build": "Build Output",
        "bin": "Executables / Scripts",
    }

    @classmethod
    def identify_directories(cls, directory_paths: list[str]) -> dict[str, str]:
        """
        Identify and map known important directories to their standard purpose.

        Args:
            directory_paths: A list of directory paths in the repository.

        Returns:
            A dictionary mapping the matched directory path to its purpose.
        """
        identified = {}
        for path in directory_paths:
            parts = path.split("/")
            for part in parts:
                if part in cls.IMPORTANT_DIRECTORIES:
                    identified[path] = cls.IMPORTANT_DIRECTORIES[part]
                    break
        return identified

    @classmethod
    def detect_layout(cls, directory_paths: list[str]) -> str:
        """
        Detect common project layouts (e.g., monorepo vs standard).

        Args:
            directory_paths: A list of directory paths.

        Returns:
            A string describing the likely project layout.
        """
        top_level_dirs = set()
        for path in directory_paths:
            parts = path.split("/")
            if parts:
                top_level_dirs.add(parts[0])

        if "packages" in top_level_dirs or "apps" in top_level_dirs or "workspaces" in top_level_dirs:
            return "Monorepo Layout"

        return "Standard Layout"
