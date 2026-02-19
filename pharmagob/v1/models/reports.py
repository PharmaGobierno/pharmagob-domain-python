from dataclasses import dataclass, field

from typing import Any, Dict, Optional
from ._base import UpdatableModel
from .minified import min_models

@dataclass(kw_only=True)
class ReportRequestModel(UpdatableModel):
    __entity_name__ = "reports-control"

    status: str = "PENDING"
    progress: int = 0
    report_type: str = "GLOBAL_INVENTORY"
    filters: Dict[str, Any]
    author: min_models.UserMin
    download_url: Optional[str] = None
    temp_collection: Optional[str] = None

    def minified(self) -> min_models.ReportRequestMin:
        return min_models.ReportRequestMin(
            id=self._id,
            status=self.status,
            report_type=self.report_type,
            progress=self.progress,
            user_id=self.author.id
        )