"""
Reusable Markdown parser for DevBridge.
"""
import re


class MarkdownParser:
    """
    Utility class for deterministically parsing markdown content.

    Provides methods to extract specific sections, bullet lists, fenced code blocks,
    and hyperlinks using regular expressions. This ensures extraction relies purely
    on deterministic heuristics, avoiding AI reasoning.
    """

    def __init__(self, content: str):
        """
        Initialize the parser with markdown content.

        Args:
            content: The raw markdown string to parse.
        """
        self.content = content

    def extract_title(self) -> str | None:
        """
        Extract the main title (# Heading 1) from the markdown.

        Returns:
            The text of the first level-1 heading, or None if not found.
        """
        match = re.search(r"^#\s+(.+)$", self.content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    def extract_section(self, section_name: str) -> str | None:
        """
        Extract a specific section by heading name.
        Matches ## Section Name (or ###), and captures until the next heading of same or higher level.

        Args:
            section_name: The name of the heading to extract (case-insensitive).

        Returns:
            The text content of the section, or None if the section was not found.
        """
        pattern = rf"^(#{{1,6}})\s*{re.escape(section_name)}\s*$(.*?)(?=^#{{1,6}}\s|\Z)"
        match = re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if match:
            return match.group(2).strip()
        return None

    def extract_list(self, text: str) -> list[str]:
        """
        Extract a list of bullet points from a given text block.

        Args:
            text: The text to parse for bullet points.

        Returns:
            A list of string items (bullet points).
        """
        items = []
        for line in text.splitlines():
            line = line.strip()
            # Handle standard Markdown bullet styles
            if line.startswith("- ") or line.startswith("* ") or line.startswith("+ "):
                items.append(line[2:].strip())
        return items

    def extract_section_list(self, section_name: str) -> list[str]:
        """
        Extract a specific section and parse it as a list of bullet points.

        Args:
            section_name: The name of the heading to extract.

        Returns:
            A list of string items.
        """
        section = self.extract_section(section_name)
        if not section:
            return []
        return self.extract_list(section)

    def extract_links(self, text: str) -> list[dict[str, str]]:
        """
        Extract markdown hyperlinks [text](url) from a text block.

        Args:
            text: The text block to parse.

        Returns:
            A list of dictionaries with 'text' and 'url' keys.
        """
        links = []
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
            links.append({
                "text": match.group(1),
                "url": match.group(2)
            })
        return links

    def extract_fenced_code_blocks(self, text: str) -> list[dict[str, str]]:
        """
        Extract fenced code blocks (```language ... ```) from a text block.

        Args:
            text: The text block to parse.

        Returns:
            A list of dictionaries with 'language' and 'code' keys.
        """
        blocks = []
        for match in re.finditer(r"^```(\w*)\s*\n(.*?)^```", text, re.MULTILINE | re.DOTALL):
            blocks.append({
                "language": match.group(1).strip() if match.group(1) else "text",
                "code": match.group(2).strip()
            })
        return blocks
