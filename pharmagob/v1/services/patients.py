from pharmagob.v1.models.patient import PatientModel
from pharmagob.v1.repository_interfaces.patients import PatientRepositoryInterface
from ._base import BaseService


class PatientService(BaseService[PatientModel, PatientRepositoryInterface]):
    __model__ = PatientModel
