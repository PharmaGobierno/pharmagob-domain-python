from pharmagob.v1.models.doctor import DoctorModel
from pharmagob.v1.repository_interfaces.doctors import DoctorRepositoryInterface

from ._base import BaseService


class DoctorService(BaseService[DoctorModel, DoctorRepositoryInterface]):
    __model__ = DoctorModel
