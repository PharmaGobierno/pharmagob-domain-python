from pharmagob.v1.models.reports import ReportRequestModel
from pharmagob.v1.repository_interfaces.reports import ReportRepositoryInterface
from ._base import BaseService

class ReportService(BaseService[ReportRequestModel, ReportRepositoryInterface]):
    __model__ = ReportRequestModel
    
    def validate_report_request(self, report: ReportRequestModel):
        if not report.filters:
            raise ValueError("Filters cannot be empty")