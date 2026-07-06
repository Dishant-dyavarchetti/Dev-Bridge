"""
Deterministic language detection utility.
"""
from collections import Counter


class LanguageDetector:
    """
    Utility for detecting programming languages based on repository metadata
    and file extensions. Returns strictly factual data without AI interpretation.
    """

    # Common extension mappings
    EXTENSION_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "JavaScript (React)",
        ".tsx": "TypeScript (React)",
        ".java": "Java",
        ".go": "Go",
        ".rs": "Rust",
        ".c": "C",
        ".cpp": "C++",
        ".cs": "C#",
        ".rb": "Ruby",
        ".php": "PHP",
        ".html": "HTML",
        ".css": "CSS",
        ".sh": "Shell",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".m": "Objective-C",
        ".scala": "Scala",
        ".dart": "Dart",
    }

    @classmethod
    def detect_from_files(cls, file_paths: list[str]) -> dict[str, int]:
        """
        Tally up the programming languages based on file extensions.

        Args:
            file_paths: A list of file paths in the repository.

        Returns:
            A dictionary mapping language names to file counts.
        """
        tally: Counter[str] = Counter()
        for path in file_paths:
            ext_idx = path.rfind(".")
            if ext_idx != -1:
                ext = path[ext_idx:].lower()
                lang = cls.EXTENSION_MAP.get(ext)
                if lang:
                    tally[lang] += 1
        return dict(tally)
