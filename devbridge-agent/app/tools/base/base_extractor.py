"""
Abstract base class for all data extraction tools.
"""
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

# Generic type variable for the return type of the extraction
T = TypeVar("T")

class BaseExtractor(ABC, Generic[T]):
    """
    Abstract base class for all extraction tools in DevBridge.

    This class defines the common contract for deterministic data extraction.
    All future extractors should inherit from this class and implement the
    `extract` method. This layer is strictly for fetching and formatting data
    without AI reasoning or business logic.
    """

    @abstractmethod
    async def extract(self, *args: Any, **kwargs: Any) -> T:
        """
        Execute the extraction process.

        Subclasses must implement this method to perform the specific data
        extraction logic. It should interact with integration layers (e.g., GitHub)
        and return deterministically formatted data structures.

        Args:
            *args: Variable length argument list specific to the extractor.
            **kwargs: Arbitrary keyword arguments specific to the extractor.

        Returns:
            The extracted data of generic type T.
        """
        pass
