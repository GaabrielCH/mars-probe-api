from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.database import Base


class ProbeRecord(Base):
    __tablename__ = "probes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    x: Mapped[int]
    y: Mapped[int]
    grid_x: Mapped[int]
    grid_y: Mapped[int]
    direction: Mapped[str] = mapped_column(String)
