from pharmagob.v1.models.reference_counter import ReferenceCounterModel
from pharmagob.v1.services.reference_counters import ReferenceCounterService


class FakeRepository:
    def __init__(self):
        self.calls = []
        self.seq = 11

    def next_sequence(self, entity, prefix, *, scope=None, updated_at):
        self.calls.append((entity, prefix, scope, updated_at))
        self.seq += 1
        return self.seq


def test_build_key_with_and_without_scope():
    assert ReferenceCounterModel.build_key("inventory-count-tasks", "CF") == "inventory-count-tasks:CF"
    assert (
        ReferenceCounterModel.build_key("inventory-count-tasks", "CF", "MCIMB006316:2027")
        == "inventory-count-tasks:CF:MCIMB006316:2027"
    )


def test_next_reference_id_formats_six_digits():
    repository = FakeRepository()
    service = ReferenceCounterService(repository)
    assert service.next_reference_id("inventory-count-tasks", "CF") == "CF-000012"
    assert service.next_reference_id("inventory-count-tasks", "CC") == "CC-000013"
    entity, prefix, scope, updated_at = repository.calls[0]
    assert (entity, prefix, scope) == ("inventory-count-tasks", "CF", None)
    assert updated_at > 0


def test_format_reference_id_keeps_wider_numbers():
    assert ReferenceCounterService.format_reference_id("CF", 1234567) == "CF-1234567"
