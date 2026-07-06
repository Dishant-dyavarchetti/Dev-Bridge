"""
Issue extraction tools package.

Provides the deterministic IssueExtractor for retrieving and
normalizing GitHub issues, separating them from Pull Requests.
"""

from app.tools.issue_knowledge.extract_issues import IssueKnowledgeExtractor

__all__ = [
    "IssueKnowledgeExtractor",
]
