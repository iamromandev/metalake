import uuid
from typing import Any

from tortoise import fields

from src.core.base import Base


class Lake(Base):
    app: str = fields.CharField(max_length=255, index=True)
    dataset: str = fields.CharField(max_length=255, index=True)
    ref_id: uuid.UUID = fields.UUIDField(default=uuid.uuid4, index=True)
    meta: dict[str, Any] | list[Any] | None = fields.JSONField(null=True)

    class Meta:
        table = "lake"
        table_description = "Lake"
        ordering = ["app", "dataset", "ref_id"]
        unique_together = [("app", "dataset", "ref_id",)]

    def __str__(self) -> str:
        return f"[Lake: {self.app}, {self.dataset}, {self.ref_id}]"
