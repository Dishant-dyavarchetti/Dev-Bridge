"""
Deterministic framework and ecosystem detection utility.
"""


class FrameworkDetector:
    """
    Utility for detecting frameworks and ecosystems based on deterministic
    inspection of manifest files and characteristic filenames.
    """

    ECOSYSTEM_FILES = {
        "package.json": "Node.js / npm",
        "pyproject.toml": "Python (Poetry/Flit/setuptools)",
        "requirements.txt": "Python (pip)",
        "Cargo.toml": "Rust (Cargo)",
        "Cargo.lock": "Rust (Cargo)",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java/Kotlin (Gradle)",
        "build.gradle.kts": "Java/Kotlin (Gradle)",
        "go.mod": "Go (Modules)",
        "composer.json": "PHP (Composer)",
        "Gemfile": "Ruby (Bundler)",
        "mix.exs": "Elixir (Mix)",
    }

    FRAMEWORK_INDICATORS = {
        "manage.py": "Django",
        "next.config.js": "Next.js",
        "next.config.mjs": "Next.js",
        "nuxt.config.js": "Nuxt.js",
        "nuxt.config.ts": "Nuxt.js",
        "vue.config.js": "Vue.js",
        "angular.json": "Angular",
        "gatsby-config.js": "Gatsby",
        "svelte.config.js": "Svelte",
        "tailwind.config.js": "Tailwind CSS",
        "webpack.config.js": "Webpack",
        "vite.config.js": "Vite",
        "vite.config.ts": "Vite",
        "artisan": "Laravel",
    }

    @classmethod
    def detect_ecosystems(cls, root_files: list[str]) -> list[str]:
        """
        Identify programming ecosystems and package managers from root files.

        Args:
            root_files: List of file names found in the root of the repository.

        Returns:
            A list of detected ecosystems.
        """
        detected = set()
        for file in root_files:
            file_name = file.split("/")[-1]
            if file_name in cls.ECOSYSTEM_FILES:
                detected.add(cls.ECOSYSTEM_FILES[file_name])
        return sorted(detected)

    @classmethod
    def detect_frameworks_from_files(cls, file_paths: list[str]) -> list[str]:
        """
        Identify frameworks based on characteristic file names present in the repository.

        Args:
            file_paths: List of file paths in the repository.

        Returns:
            A list of detected frameworks.
        """
        detected = set()
        for path in file_paths:
            file_name = path.split("/")[-1]
            if file_name in cls.FRAMEWORK_INDICATORS:
                detected.add(cls.FRAMEWORK_INDICATORS[file_name])
        return sorted(detected)
