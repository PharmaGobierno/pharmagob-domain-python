from dataclasses import dataclass
from typing import Optional, Sequence

from pharmagob.v1.models.inventory_count_line import LineStatus


@dataclass(frozen=True)
class CountEntry:
    counted_quantity: int
    kardex_snapshot_quantity: int  # location-content quantity when this round was captured

    @property
    def diff(self) -> int:
        return self.counted_quantity - self.kardex_snapshot_quantity


@dataclass(frozen=True)
class RuleResult:
    status: LineStatus
    case: Optional[int]  # None on the audit rounds: the line keeps the round 2 case
    note: str


def evaluate(entries: Sequence[CountEntry], *, is_in_system: bool = True) -> RuleResult:
    """Evaluates a line after saving a round (1, 2 or one validated by the auditor).

    Compares DIFFERENCES (counted_quantity - kardex_snapshot_quantity of its own
    round), not absolute quantities: a prescription dispatched between rounds
    does not invalidate the count (D-01).

    From the third round on, every entry is a round validated by the auditor;
    a line that returned from adjustment to audit (H-13 / H-15) gets a new one
    (4, 5...) with its own snapshot, and only the LAST one decides.
    """
    if not entries:
        return RuleResult(LineStatus.PENDING, None, "Sin conteos")
    if len(entries) == 1:
        return _first_round(entries[0], is_in_system)
    if len(entries) == 2:
        return _second_round(entries[0], entries[1], is_in_system)
    return _validated_round(entries[-1])


def _first_round(c1: CountEntry, is_in_system: bool) -> RuleResult:
    if not is_in_system:  # cases 5 and 6: out of system always goes to a second round
        return RuleResult(LineStatus.SECOND_COUNT, 5, "Clave fuera de sistema: a segundo conteo")
    if c1.diff == 0:  # cases 7 and 8
        return RuleResult(LineStatus.CLOSED, 7, "Primer conteo igual al Kardex: cierra sin diferencia")
    if c1.counted_quantity == 0:  # case 9
        return RuleResult(LineStatus.SECOND_COUNT, 9, "Primer conteo en cero: a segundo conteo")
    if c1.diff > 0:  # case 10
        return RuleResult(LineStatus.SECOND_COUNT, 10, "Mayor al Kardex: a segundo conteo")
    return RuleResult(LineStatus.SECOND_COUNT, 3, "Menor al Kardex: a segundo conteo")


def _second_round(c1: CountEntry, c2: CountEntry, is_in_system: bool) -> RuleResult:
    if c2.diff == 0:  # cases 1 and 13
        return RuleResult(LineStatus.CLOSED, 13, "Segundo conteo igual al Kardex: cierra sin diferencia")
    if c1.diff == c2.diff:  # both rounds confirm the same difference -> adjustment
        if not is_in_system:  # case 4
            return RuleResult(LineStatus.ADJUSTMENT, 4, "Fuera de sistema confirmada: a ajuste")
        if c2.counted_quantity == 0:  # confirmed zero is labeled case 9
            return RuleResult(LineStatus.ADJUSTMENT, 9, "Cero confirmado: ajuste a cero")
        if c2.diff > 0:  # case 10 confirmed
            return RuleResult(LineStatus.ADJUSTMENT, 10, "Sobrante confirmado: ajuste positivo")
        return RuleResult(LineStatus.ADJUSTMENT, 2, "Faltante confirmado: ajuste negativo")  # cases 2 and 11
    case = 12 if not is_in_system else 14
    return RuleResult(LineStatus.VALIDATION, case, "Los conteos no coinciden entre sí ni con el Kardex: a auditoría")


def _validated_round(c3: CountEntry) -> RuleResult:
    """Third round captured and validated by the auditor."""
    if c3.diff == 0:
        return RuleResult(LineStatus.CLOSED, None, "Tercer conteo igual al Kardex: cierra sin diferencia")
    return RuleResult(LineStatus.ADJUSTMENT, None, "Tercer conteo distinto al Kardex: a ajuste")
