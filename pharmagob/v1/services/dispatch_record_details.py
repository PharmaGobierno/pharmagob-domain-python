from pharmagob.v1.models.dispatch_record_details import DispatchRecordDetailModel
from pharmagob.v1.repository_interfaces.dispatch_record_details import DispatchRecordDetailRepositoryInterface

from ._base import BaseService


class DispatchRecordDetailService(BaseService[DispatchRecordDetailModel, DispatchRecordDetailRepositoryInterface]):
    __model__ = DispatchRecordDetailModel
