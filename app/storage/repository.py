from sqlalchemy.orm import Session

from app.models.probe import Probe
from app.storage.models import ProbeRecord


def save_probe(session: Session, probe: Probe, grid_x: int, grid_y: int) -> None:
    record = ProbeRecord(
        id=probe.id,
        x=probe.x,
        y=probe.y,
        grid_x=grid_x,
        grid_y=grid_y,
        direction=probe.direction,
    )
    session.add(record)
    session.commit()


def get_probe(session: Session, probe_id: str) -> Probe | None:
    record = session.get(ProbeRecord, probe_id)
    if record is None:
        return None
    return _to_probe(record)


def get_grid(session: Session, probe_id: str) -> tuple[int, int] | None:
    record = session.get(ProbeRecord, probe_id)
    if record is None:
        return None
    return (record.grid_x, record.grid_y)


def update_probe(session: Session, probe: Probe) -> None:
    record = session.get(ProbeRecord, probe.id)
    record.x = probe.x
    record.y = probe.y
    record.direction = probe.direction
    session.commit()


def get_all_probes(session: Session) -> list[Probe]:
    records = session.query(ProbeRecord).all()
    return [_to_probe(r) for r in records]


def _to_probe(record: ProbeRecord) -> Probe:
    return Probe(id=record.id, x=record.x, y=record.y, direction=record.direction)
