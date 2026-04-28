from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.probe import LaunchProbeRequest, MoveProbeRequest, Probe, ProbeListResponse
from app.services.probe_service import (
    InvalidCommandError,
    OutOfBoundsError,
    ProbeNotFoundError,
    get_all_probes,
    launch_probe,
    move_probe,
)
from app.storage.database import get_session

router = APIRouter(prefix="/probes", tags=["probes"])


@router.post("", response_model=Probe, status_code=status.HTTP_201_CREATED)
def launch(body: LaunchProbeRequest, session: Session = Depends(get_session)) -> Probe:
    return launch_probe(session, body.x, body.y, body.direction)


@router.patch("/{probe_id}/commands", response_model=Probe)
def move(probe_id: str, body: MoveProbeRequest, session: Session = Depends(get_session)) -> Probe:
    try:
        return move_probe(session, probe_id, body.commands)
    except ProbeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Probe not found")
    except InvalidCommandError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid commands: {e.invalid_commands}",
        )
    except OutOfBoundsError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Movement would take probe out of bounds at ({e.x}, {e.y})",
        )


@router.get("", response_model=ProbeListResponse)
def list_probes(session: Session = Depends(get_session)) -> ProbeListResponse:
    return ProbeListResponse(probes=get_all_probes(session))
