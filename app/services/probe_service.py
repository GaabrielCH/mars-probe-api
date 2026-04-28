import uuid

from app.models.probe import Direction, Probe
from app.storage import memory

TURN_LEFT = {
    Direction.NORTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
}

TURN_RIGHT = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
}

MOVE_DELTA = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0),
}

VALID_COMMANDS = {"M", "L", "R"}


def launch_probe(grid_x: int, grid_y: int, direction: Direction) -> Probe:
    probe = Probe(
        id=str(uuid.uuid4())[:8],
        x=0,
        y=0,
        direction=direction,
    )
    memory.save_probe(probe, grid_x, grid_y)
    return probe


def move_probe(probe_id: str, commands: str) -> Probe:
    probe = memory.get_probe(probe_id)
    if probe is None:
        raise ProbeNotFoundError(probe_id)

    grid = memory.get_grid(probe_id)

    invalid = [c for c in commands.upper() if c not in VALID_COMMANDS]
    if invalid:
        raise InvalidCommandError(invalid)

    x, y, direction = probe.x, probe.y, probe.direction

    for command in commands.upper():
        if command == "L":
            direction = TURN_LEFT[direction]
        elif command == "R":
            direction = TURN_RIGHT[direction]
        elif command == "M":
            dx, dy = MOVE_DELTA[direction]
            new_x = x + dx
            new_y = y + dy

            if not _is_within_bounds(new_x, new_y, grid):
                raise OutOfBoundsError(new_x, new_y)

            x, y = new_x, new_y

    updated_probe = probe.model_copy(update={"x": x, "y": y, "direction": direction})
    memory.update_probe(updated_probe)
    return updated_probe


def get_all_probes() -> list[Probe]:
    return memory.get_all_probes()


def _is_within_bounds(x: int, y: int, grid: tuple[int, int]) -> bool:
    grid_x, grid_y = grid
    return 0 <= x <= grid_x and 0 <= y <= grid_y


class ProbeNotFoundError(Exception):
    def __init__(self, probe_id: str):
        self.probe_id = probe_id
        super().__init__(f"Probe {probe_id} not found")


class InvalidCommandError(Exception):
    def __init__(self, invalid_commands: list[str]):
        self.invalid_commands = invalid_commands
        super().__init__(f"Invalid commands: {invalid_commands}")


class OutOfBoundsError(Exception):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        super().__init__(f"Position ({x}, {y}) is out of bounds")
