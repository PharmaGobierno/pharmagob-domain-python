from pharmagob.v1.models.dispatch_record_status import DispatchRecordStatusModel
from pharmagob.v1.repository_interfaces.dispatch_record_status import (
    DispatchRecordStatusRepositoryInterface,
)

from ._base import BaseService


class DispatchRecordStatusService(
    BaseService[DispatchRecordStatusModel, DispatchRecordStatusRepositoryInterface]
):
    __model__ = DispatchRecordStatusModel
