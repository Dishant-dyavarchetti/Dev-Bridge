"""
Deterministic extraction tool for GitHub repository issues.
"""
from typing import Any

from app.integrations.github.client import GitHubClient
from app.integrations.github.issues import IssueAPI
from app.tools.base.base_extractor import BaseExtractor


class IssueKnowledgeExtractor(BaseExtractor[list[dict[str, Any]]]):
    """
    Extractor for retrieving, filtering, and normalizing repository issues.

    Communicates with the GitHub REST API to fetch issues and deterministically
    filters out pull requests. It normalizes the data into a standard dictionary
    format intended to be consumed by future IssueKnowledge models. It does not
    perform any AI reasoning, ranking, or estimation.
    """

    def __init__(self, client: GitHubClient):
        """
        Initialize the issue extractor.

        Args:
            client: An authenticated GitHubClient instance.
        """
        self.api = IssueAPI(client)

    async def extract(self, owner: str, repo: str, limit: int = 30) -> list[dict[str, Any]]:
        """
        Extract and normalize open issues for a repository.

        Fetches up to the specified limit of open issues, strictly filtering
        out pull requests. Returns normalized dictionaries of factual data.

        Args:
            owner: The repository owner.
            repo: The repository name.
            limit: The maximum number of issues to retrieve (max 100 per page, defaults to 30).

        Returns:
            A list of normalized issue dictionaries.
        """
        raw_issues = await self.api.list_open_issues(owner, repo, per_page=limit)

        normalized_issues = []
        for raw_issue in raw_issues:
            # GitHub's REST API v3 considers every pull request an issue,
            # but not every issue is a pull request.
            # We filter out items that have the 'pull_request' key.
            if "pull_request" in raw_issue:
                continue

            # Normalize labels
            labels = []
            for label in raw_issue.get("labels", []):
                if isinstance(label, dict):
                    labels.append(label.get("name", ""))
                elif isinstance(label, str):
                    labels.append(label)

            # Extract user login
            user_data = raw_issue.get("user") or {}
            author = user_data.get("login", "unknown")

            # Map into a standardized dictionary layout
            normalized = {
                "number": raw_issue.get("number"),
                "title": raw_issue.get("title", ""),
                "state": raw_issue.get("state", "open"),
                "url": raw_issue.get("html_url", ""),
                "author": author,
                "body": raw_issue.get("body"),
                "labels": [lbl for lbl in labels if lbl],
                "created_at": raw_issue.get("created_at"),
                "updated_at": raw_issue.get("updated_at"),
                "comments_count": raw_issue.get("comments", 0)
            }
            normalized_issues.append(normalized)

        return normalized_issues
