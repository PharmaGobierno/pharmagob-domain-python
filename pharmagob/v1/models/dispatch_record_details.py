from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel
from .minified import min_models


@dataclass(kw_only=True)
class DispatchRecordDetailModel(UpdatableModel):
    __entity_name__ = "dispatch-record-details"

    umu_id: str
    dispatch_record: min_models.DispatchRecordMin
    dispatch_at: int
    author: min_models.UserMin
    quantity: int
    prescribed_quantity: Optional[int] = None
    prescribed_at: Optional[int] = None
    location_content: min_models.LocationContentMin
    item: min_models.ItemMin
    administration_type: Optional[str] = None
    doctor: Optional[min_models.DoctorMin] = None
    patient: Optional[min_models.PatientMin] = None
    patient_bed: Optional[str] = None
    notes: Optional[str] = None
    context: Optional[dict] = None

    def minified(self) -> min_models.DispatchRecordDetailMin:
        return min_models.DispatchRecordDetailMin(
            id=self._id,
            umu_id=self.umu_id,
            dispatch_record_id=self.dispatch_record.id,
            dispatch_record_reference_id=self.dispatch_record.reference_id,
            item_id=self.item.id,
            quantity=self.quantity,
            dispatch_at=self.dispatch_at,
            location_content_id=self.location_content.id,
            doctor_id=self.doctor.id if self.doctor else None,
            patient_id=self.patient.id if self.patient else None,
            prescribed_quantity=self.prescribed_quantity,
            prescribed_at=self.prescribed_at,
        )
