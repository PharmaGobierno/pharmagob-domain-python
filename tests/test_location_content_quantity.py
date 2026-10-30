import pytest

from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified.min_models import ItemMin, LocationMin, UserMin
from pharmagob.v1.repository_interfaces.location_contents import (
    LocationContentRepositoryInterface,
)
from pharmagob.v1.services.location_contents import LocationContentService

AUTHOR = UserMin(id="a1", umu_id="u1", display_name="Ana")


def build_entity(quantity=0):
    return LocationContentModel(
        umu_id="u1",
        lot="L1",
        expiration_date=99,
        quantity=quantity,
        item=ItemMin(
            id="i1",
            foreign_id="f1",
            description="d",
            is_controlled=False,
            category="c",
            sub_category="s",
        ),
        location=LocationMin(id="loc1", umu_id="u1", label_code="FARB"),
        last_author=AUTHOR,
    )


class FakeRepository:
    """Stands in for the Mongo repository: returns the document AFTER."""

    def __init__(self, document=None):
        self.document = document
        self.calls = []

    def increment_quantity(self, location_content_id, delta, **kwargs):
        self.calls.append(("increment", location_content_id, delta, kwargs))
        return self.document

    def upsert_increment_quantity(self, location_content_id, delta, **kwargs):
        self.calls.append(("upsert", location_content_id, delta, kwargs))
        return self.document

    def update_if(self, entity_id, *, expected, data):
        self.calls.append(("update_if", entity_id, expected, data))
        return 1


def test_increase_adds_with_author_and_umu():
    entity = build_entity(quantity=15)
    repository = FakeRepository(entity.dict())
    after = LocationContentService(repository).increase_quantity(
        entity._id, 5, author=AUTHOR, umu_id="u1"
    )
    assert isinstance(after, LocationContentModel) and after.quantity == 15
    kind, lc_id, delta, kwargs = repository.calls[0]
    assert (kind, lc_id, delta) == ("increment", entity._id, 5)
    assert kwargs["last_author"] == {
        "id": "a1",
        "umu_id": "u1",
        "display_name": "Ana",
    }
    assert kwargs["umu_id"] == "u1" and kwargs["updated_at"] > 0
    assert "min_quantity" not in kwargs


def test_increase_of_a_missing_location_content_is_none():
    assert (
        LocationContentService(FakeRepository(None)).increase_quantity(
            "x", 1, author=AUTHOR
        )
        is None
    )


def test_decrease_subtracts_and_requires_the_stock():
    entity = build_entity(quantity=6)
    repository = FakeRepository(entity.dict())
    after = LocationContentService(repository).decrease_quantity(
        entity._id, 4, author=AUTHOR
    )
    assert after.quantity == 6
    _, _, delta, kwargs = repository.calls[0]
    assert delta == -4 and kwargs["min_quantity"] == 4


def test_decrease_without_enough_stock_is_none():
    assert (
        LocationContentService(FakeRepository(None)).decrease_quantity(
            "x", 9, author=AUTHOR
        )
        is None
    )


@pytest.mark.parametrize("quantity", [0, -3])
@pytest.mark.parametrize("method", ["increase_quantity", "decrease_quantity"])
def test_quantity_must_be_positive(method, quantity):
    repository = FakeRepository(build_entity().dict())
    with pytest.raises(ValueError):
        getattr(LocationContentService(repository), method)(
            "x", quantity, author=AUTHOR
        )
    assert repository.calls == []


def test_upsert_sends_the_full_document_and_returns_the_model_after():
    entity = build_entity()
    stored = build_entity(quantity=7)
    repository = FakeRepository(stored.dict())
    after = LocationContentService(repository).upsert_increase_quantity(
        entity, 7, author=AUTHOR
    )
    assert after.quantity == 7
    kind, lc_id, delta, kwargs = repository.calls[0]
    assert (kind, lc_id, delta) == ("upsert", entity._id, 7)
    assert kwargs["insert_data"] == entity.dict()
    assert kwargs["last_author"]["id"] == "a1"


def test_upsert_rejects_non_positive_quantity():
    repository = FakeRepository(build_entity().dict())
    with pytest.raises(ValueError):
        LocationContentService(repository).upsert_increase_quantity(
            build_entity(), 0, author=AUTHOR
        )
    assert repository.calls == []


def test_update_if_goes_through_the_base_service():
    repository = FakeRepository()
    service = LocationContentService(repository)
    assert service.update_if("x", expected={"a": 1}, data={"b": 2}) == 1
    assert repository.calls == [("update_if", "x", {"a": 1}, {"b": 2})]


def test_port_declares_the_new_operations():
    assert {
        "increment_quantity",
        "upsert_increment_quantity",
        "update_if",
    } <= LocationContentRepositoryInterface.__abstractmethods__
