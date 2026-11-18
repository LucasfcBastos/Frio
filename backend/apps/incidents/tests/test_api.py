import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
client = APIClient()


def test_active_incidents_sorted_by_severity(seeded):
    response = client.get("/api/v1/incidents/", {"status": "active"})

    assert response.status_code == 200
    results = response.json()["results"]
    assert {i["rule_code"] for i in results} == {
        "UNSCHEDULED_DEFROST",
        "SENSOR_DIVERGENCE",
        "OUT_OF_SAFE_RANGE",
        "SETPOINT_TAMPERING",
    }
    severities = [i["severity"] for i in results]
    assert severities == sorted(severities, key=["critical", "high", "medium", "low"].index)


def test_rejects_unknown_status(seeded):
    response = client.get("/api/v1/incidents/", {"status": "bogus"})
    assert response.status_code == 400


def test_detail_includes_config_changes_from_unknown_ip(seeded):
    incident_id = client.get("/api/v1/incidents/").json()["results"][0]["id"]

    body = client.get(f"/api/v1/incidents/{incident_id}/").json()

    changes = [e for e in body["timeline"] if e["kind"] == "config_change"]
    assert changes and all(e["data"]["origin_ip"] == "203.0.113.47" for e in changes)
    assert any(e["kind"] == "incident_detected" for e in body["timeline"])


def test_detail_unknown_incident_is_404(seeded):
    assert client.get("/api/v1/incidents/99999/").status_code == 404
