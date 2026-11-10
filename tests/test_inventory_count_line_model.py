"""InventoryCountLineModel: `pending_adjustment_quantity` (H-28, DOM-11)."""

from pharmagob.v1.models.inventory_count_line import InventoryCountLineModel, LineStatus
from pharmagob.v1.models.minified import min_models


def _line(**overrides) -> InventoryCountLineModel:
    author = min_models.UserMin(id="u1", umu_id="908", display_name="Contador")
    data = dict(
        umu_id="908",
        task=min_models.CountTaskMin(
            id="t1", reference_id="CF-000001", task_name="T1", count_type="PHYSICAL"
        ),
        item=min_models.ItemMin(
            id="010.000.1701.00",
            foreign_id="010.000.1701.00",
            description="Item",
            is_controlled=False,
            category="MED",
            sub_category="GEN",
        ),
        lot="L1",
        expiration_date=1_900_000_000_000,
        location=min_models.LocationMin(id="loc1", umu_id="908", label_code="STANDARD"),
        location_content_id="lc1",
        is_in_system=True,
        kardex_initial_quantity=36,
        last_author=author,
    )
    data.update(overrides)
    return InventoryCountLineModel(**data)


def test_pending_adjustment_quantity_defaults_to_none_and_is_serialized():
    line = _line()
    assert line.pending_adjustment_quantity is None
    assert line.status is LineStatus.PENDING
    assert "pending_adjustment_quantity" in line.dict()
    assert line.dict()["pending_adjustment_quantity"] is None


def test_old_documents_without_the_field_still_load():
    doc = _line().dict()
    doc.pop("pending_adjustment_quantity")
    rebuilt = InventoryCountLineModel(**doc)
    assert rebuilt.pending_adjustment_quantity is None
    assert rebuilt._id == _line()._id


def test_signed_value_round_trips_through_dict():
    counts = [
        min_models.CountEntryMin(
            round=1,
            counted_quantity=31,
            kardex_snapshot_quantity=36,
            author=min_models.UserMin(id="u1", umu_id="908", display_name="Contador"),
            counted_at=1,
        ),
        min_models.CountEntryMin(
            round=2,
            counted_quantity=31,
            kardex_snapshot_quantity=36,
            author=min_models.UserMin(id="u2", umu_id="908", display_name="Contador 2"),
            counted_at=2,
        ),
    ]
    last = counts[-1]
    line = _line(
        counts=counts,
        status=LineStatus.ADJUSTMENT,
        pending_adjustment_quantity=last.counted_quantity - last.kardex_snapshot_quantity,
    )
    assert line.pending_adjustment_quantity == -5
    rebuilt = InventoryCountLineModel(**line.dict())
    assert rebuilt.pending_adjustment_quantity == -5
    assert rebuilt.resolution is None  # pending and applied are never set together
