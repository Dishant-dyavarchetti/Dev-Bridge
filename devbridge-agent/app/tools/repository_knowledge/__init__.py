"""
Repository extraction tools package.

This module exposes the RepositoryExtractor tool which fetches and parses
metadata from the GitHub API into DevBridge knowledge models.
"""

from app.tools.repository_knowledge.extract_repository import (
    RepositoryKnowledgeExtractor,
)

__all__ = [
    "RepositoryKnowledgeExtractor",
]
