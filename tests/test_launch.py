def test_launch_probe_returns_initial_position(client):
    response = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})

    assert response.status_code == 201
    data = response.json()
    assert data["x"] == 0
    assert data["y"] == 0
    assert data["direction"] == "NORTH"
    assert "id" in data


def test_launch_probe_returns_unique_ids(client):
    first = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    second = client.post("/probes", json={"x": 5, "y": 5, "direction": "EAST"})

    assert first.json()["id"] != second.json()["id"]


def test_launch_probe_with_different_directions(client):
    for direction in ["NORTH", "SOUTH", "EAST", "WEST"]:
        response = client.post("/probes", json={"x": 5, "y": 5, "direction": direction})
        assert response.status_code == 201
        assert response.json()["direction"] == direction


def test_launch_probe_with_invalid_direction_returns_422(client):
    response = client.post("/probes", json={"x": 5, "y": 5, "direction": "UP"})

    assert response.status_code == 422


def test_launch_probe_with_missing_fields_returns_422(client):
    response = client.post("/probes", json={"x": 5})

    assert response.status_code == 422
