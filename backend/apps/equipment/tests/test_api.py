import pytest
from rest_framework.test import APIClient

from simulation.demo_data import ATTACK_EQUIPMENT

pytestmark = pytest.mark.django_db
client = APIClient()


def _equipment():
    return client.get("/api/v1/equipment/").json()["results"]


def test_attacked_equipment_shows_divergence(seeded):
    attacked = next(e for e in _equipment() if e["name"] == ATTACK_EQUIPMENT)

    assert attacked["status"] == "critical"
    assert attacked["mode"] == "defrost"
    assert attacked["is_diverging"] is True
    assert attacked["controller_temperature_c"] < -17
    assert attacked["sensor_temperature_c"] > attacked["controller_temperature_c"] + 4
    assert attacked["firmware_outdated"] is True
    assert len(attacked["sparkline"]) == 30


def test_filters_by_store(seeded):
    store_id = _equipment()[0]["store_id"]
    response = client.get("/api/v1/equipment/", {"store_id": store_id})
    assert {e["store_id"] for e in response.json()["results"]} == {store_id}


def test_readings_series_has_both_sources_and_incident_markers(seeded):
    attacked = next(e for e in _equipment() if e["name"] == ATTACK_EQUIPMENT)

    response = client.get(f"/api/v1/equipment/{attacked['id']}/readings/", {"hours": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["equipment"]["safe_max_c"] == -15
    assert len(body["points"]) >= 60
    point = body["points"][-1]
    assert point["controller_c"] is not None and point["sensor_c"] is not None
    assert {m["rule_code"] for m in body["incidents"]} >= {"UNSCHEDULED_DEFROST"}


def test_readings_validates_hours(seeded):
    response = client.get("/api/v1/equipment/1/readings/", {"hours": 0})
    assert response.status_code == 400


def test_readings_unknown_equipment_is_404(seeded):
    assert client.get("/api/v1/equipment/99999/readings/").status_code == 404
