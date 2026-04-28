from app.models.probe import Probe

_probes: dict[str, Probe] = {}
_grids: dict[str, tuple[int, int]] = {}


def save_probe(probe: Probe, grid_x: int, grid_y: int) -> None:
    _probes[probe.id] = probe
    _grids[probe.id] = (grid_x, grid_y)


def get_probe(probe_id: str) -> Probe | None:
    return _probes.get(probe_id)


def get_grid(probe_id: str) -> tuple[int, int] | None:
    return _grids.get(probe_id)


def update_probe(probe: Probe) -> None:
    _probes[probe.id] = probe


def get_all_probes() -> list[Probe]:
    return list(_probes.values())


def clear() -> None:
    _probes.clear()
    _grids.clear()
