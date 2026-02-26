from abc import abstractmethod
from typing import Optional
from pharmagob.v1.models.reports import ReportRequestModel
from ._base import BaseRepositoryInterface

class ReportRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def get_by_id(self, report_id: str) -> Optional[ReportRequestModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, report: ReportRequestModel) -> ReportRequestModel:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, report_id: str, status: str, progress: int) -> bool:
        raise NotImplementedError