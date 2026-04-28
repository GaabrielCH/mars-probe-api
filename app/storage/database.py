from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = "sqlite:///./probes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


def get_session():
    with Session(engine) as session:
        yield session


def init_db() -> None:
    from app.storage import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
