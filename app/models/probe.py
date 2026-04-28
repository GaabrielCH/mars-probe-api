from enum import Enum
from pydantic import BaseModel


class Direction(str, Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class Probe(BaseModel):
    id: str
    x: int
    y: int
    direction: Direction


class LaunchProbeRequest(BaseModel):
    x: int
    y: int
    direction: Direction


class MoveProbeRequest(BaseModel):
    commands: str


class ProbeListResponse(BaseModel):
    probes: list[Probe]
