from pharmagob.v1.models.administrative_issue_record import (
    AdministrativeIssueRecordModel,
)
from pharmagob.v1.repository_interfaces.administrative_issue_records import (
    AdministrativeIssueRecordRepositoryInterface,
)

from ._base import BaseService


class AdministrativeIssueRecordService(
    BaseService[
        AdministrativeIssueRecordModel, AdministrativeIssueRecordRepositoryInterface
    ]
):
    __model__ = AdministrativeIssueRecordModel
