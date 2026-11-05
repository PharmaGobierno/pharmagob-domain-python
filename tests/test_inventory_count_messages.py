"""Nombres de topic de los mensajes de Conteos (INF-02, docs/backend/08-pubsub-gcp-dev.md §7.3).

Los topics del módulo llevan el prefijo `pharmagob-` para distinguirlos en el proyecto GCP compartido
con OMS/TMS. Cambiarlos rompe la infraestructura aprovisionada: hay que actualizar el spec de Pub/Sub.
"""
import pytest

from pharmagob.v1.models.messages.pubsub_msgs import (
    InventoryCountAdjustmentAppliedPubsubMessage,
    InventoryCountEventsPubsubMessage,
    InventoryCountTaskReleasePubsubMessage,
)


@pytest.mark.parametrize(
    ("message", "topic"),
    [
        (InventoryCountTaskReleasePubsubMessage, "pharmagob-inventory-count-task-release"),
        (InventoryCountEventsPubsubMessage, "pharmagob-inventory-count-events"),
        (InventoryCountAdjustmentAppliedPubsubMessage, "pharmagob-inventory-count-adjustment-applied"),
    ],
)
def test_inventory_count_topics_have_pharmagob_prefix(message, topic):
    assert message.topic() == topic
    assert message.topic().startswith("pharmagob-inventory-count-")
