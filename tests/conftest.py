import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import memory


@pytest.fixture(autouse=True)
def clear_storage():
    memory.clear()
    yield
    memory.clear()


@pytest.fixture
def client():
    return TestClient(app)
