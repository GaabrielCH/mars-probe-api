def _launch(client, x=5, y=5, direction="NORTH") -> str:
    response = client.post("/probes", json={"x": x, "y": y, "direction": direction})
    return response.json()["id"]


def test_move_forward(client):
    probe_id = _launch(client)
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "M"})

    assert response.status_code == 200
    data = response.json()
    assert data["x"] == 0
    assert data["y"] == 1
    assert data["direction"] == "NORTH"


def test_rotate_left(client):
    probe_id = _launch(client, direction="NORTH")
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "L"})

    assert response.json()["direction"] == "WEST"


def test_rotate_right(client):
    probe_id = _launch(client, direction="NORTH")
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "R"})

    assert response.json()["direction"] == "EAST"


def test_sequence_mrm_results_in_1_1_east(client):
    probe_id = _launch(client)
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "MRM"})

    data = response.json()
    assert data["x"] == 1
    assert data["y"] == 1
    assert data["direction"] == "EAST"


def test_full_rotation_left_returns_to_north(client):
    probe_id = _launch(client, direction="NORTH")
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "LLLL"})

    assert response.json()["direction"] == "NORTH"


def test_full_rotation_right_returns_to_north(client):
    probe_id = _launch(client, direction="NORTH")
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "RRRR"})

    assert response.json()["direction"] == "NORTH"


def test_movement_persists_between_requests(client):
    probe_id = _launch(client)
    client.patch(f"/probes/{probe_id}/commands", json={"commands": "MM"})
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "MM"})

    assert response.json()["y"] == 4


def test_out_of_bounds_north_returns_422(client):
    probe_id = _launch(client, x=5, y=1)
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "MM"})

    assert response.status_code == 422
    assert "out of bounds" in response.json()["detail"]


def test_out_of_bounds_does_not_update_position(client):
    probe_id = _launch(client, x=5, y=1)
    client.patch(f"/probes/{probe_id}/commands", json={"commands": "MM"})

    probes = client.get("/probes").json()["probes"]
    probe = next(p for p in probes if p["id"] == probe_id)

    assert probe["y"] == 0


def test_invalid_command_returns_422(client):
    probe_id = _launch(client)
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "MXM"})

    assert response.status_code == 422
    assert "Invalid commands" in response.json()["detail"]


def test_probe_not_found_returns_404(client):
    response = client.patch("/probes/nonexistent/commands", json={"commands": "M"})

    assert response.status_code == 404


def test_commands_are_case_insensitive(client):
    probe_id = _launch(client)
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "mrm"})

    data = response.json()
    assert data["x"] == 1
    assert data["y"] == 1
    assert data["direction"] == "EAST"


def test_empty_commands_returns_same_position(client):
    probe_id = _launch(client)
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": ""})

    data = response.json()
    assert data["x"] == 0
    assert data["y"] == 0


def test_probe_cannot_go_below_zero_moving_south(client):
    probe_id = _launch(client, direction="SOUTH")
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "M"})

    assert response.status_code == 422


def test_probe_cannot_go_below_zero_moving_west(client):
    probe_id = _launch(client, direction="WEST")
    response = client.patch(f"/probes/{probe_id}/commands", json={"commands": "M"})

    assert response.status_code == 422
