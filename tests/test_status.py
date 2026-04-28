def test_list_probes_empty(client):
    response = client.get("/probes")

    assert response.status_code == 200
    assert response.json() == {"probes": []}


def test_list_probes_after_launch(client):
    client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    response = client.get("/probes")

    data = response.json()
    assert len(data["probes"]) == 1
    assert data["probes"][0]["x"] == 0
    assert data["probes"][0]["y"] == 0


def test_list_probes_shows_all(client):
    client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    client.post("/probes", json={"x": 5, "y": 5, "direction": "EAST"})

    response = client.get("/probes")
    assert len(response.json()["probes"]) == 2


def test_list_probes_reflects_movement(client):
    launch = client.post("/probes", json={"x": 5, "y": 5, "direction": "NORTH"})
    probe_id = launch.json()["id"]
    client.patch(f"/probes/{probe_id}/commands", json={"commands": "MRM"})

    probes = client.get("/probes").json()["probes"]
    probe = next(p for p in probes if p["id"] == probe_id)

    assert probe["x"] == 1
    assert probe["y"] == 1
    assert probe["direction"] == "EAST"
