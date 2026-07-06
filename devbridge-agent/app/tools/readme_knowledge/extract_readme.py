"""
Deterministic extraction tool for GitHub repository README files.
"""

from app.integrations.github.client import GitHubClient
from app.integrations.github.contents import ContentAPI
from app.integrations.github.exceptions import GitHubNotFoundError
from app.models.knowledge.readme import ReadmeKnowledge
from app.tools.base.base_extractor import BaseExtractor
from app.tools.markdown.markdown_parser import MarkdownParser


class ReadmeKnowledgeExtractor(BaseExtractor[ReadmeKnowledge]):
    """
    Extractor for retrieving and parsing repository READMEs.

    This extractor fetches the README content via ContentAPI and uses a
    MarkdownParser to deterministically map standard sections into the
    DevBridge ReadmeKnowledge model without any AI logic.
    """

    def __init__(self, client: GitHubClient):
        """
        Initialize the README extractor.

        Args:
            client: An authenticated GitHubClient instance.
        """
        self.api = ContentAPI(client)

    async def extract(self, owner: str, repo: str) -> ReadmeKnowledge:
        """
        Extract README data and map to ReadmeKnowledge.

        Args:
            owner: The repository owner (user or organization).
            repo: The repository name.

        Returns:
            The deterministically mapped ReadmeKnowledge object.

        Raises:
            GitHubError: If the underlying GitHub integration fails.
        """
        try:
            # Fetch the README JSON which will have the base64 content decoded
            readme_data = await self.api.get_readme(owner, repo)
            content = readme_data.get("content", "")
        except GitHubNotFoundError:
            # Fallback for repositories without a README
            content = ""

        parser = MarkdownParser(content)

        # We attempt to find standard sections
        overview = (
            parser.extract_section("Overview") or
            parser.extract_section("About") or
            parser.extract_section("Description")
        )

        # Extract documentation links (format as string "text: url")
        links_section = parser.extract_section("Documentation") or parser.extract_section("Links")
        doc_links = []
        if links_section:
            for link in parser.extract_links(links_section):
                doc_links.append(f"{link['text']}: {link['url']}")

        title = parser.extract_title() or "Untitled Repository"

        knowledge = ReadmeKnowledge(
            title=title,
            overview=overview,
            installation=parser.extract_section("Installation") or parser.extract_section("Setup"),
            usage=parser.extract_section("Usage") or parser.extract_section("Getting Started"),
            features=parser.extract_section_list("Features"),
            examples=parser.extract_section_list("Examples"),
            prerequisites=parser.extract_section_list("Prerequisites") or parser.extract_section_list("Requirements"),
            documentation_links=doc_links
        )

        return knowledge
