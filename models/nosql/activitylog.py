from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field


class ActivityLog(Document):
    action: str                      # e.g. "app_info_updated"
    performed_by: str                # admin username or id
    before: Optional[dict] = None    # old values
    after: Optional[dict] = None     # new values
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "activity_logs"        # collection name