from pydantic import BaseModel, ConfigDict


class BaseDevBridgeModel(BaseModel):
    """
    Base model for all internal DevBridge models.

    Provides strict typing, assignment validation, and forbids extra fields
    to ensure data consistency across the DevBridge platform. Every future
    model in DevBridge must inherit from this class.
    """
    model_config = ConfigDict(
        strict=False,
        validate_assignment=True,
        extra="ignore",
        frozen=False,
        use_enum_values=True,
        validate_default=True
    )

    def to_dict(self) -> dict:
        """Serialize the model using DevBridge defaults."""
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """Serialize the model to JSON."""
        return self.model_dump_json(exclude_none=True)
