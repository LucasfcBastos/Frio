import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db
client = APIClient()


def _store_id(name="Loja Centro") -> int:
    stores = client.get("/api/v1/stores/").json()["results"]
    return next(s["id"] for s in stores if s["name"] == name)


def test_summary_reports_attack(seeded):
    response = client.get("/api/v1/dashboard/summary/", {"store_id": _store_id()})

    assert response.status_code == 200
    body = response.json()
    assert body["total_equipment"] == 5
    assert body["critical_equipment"] == 1
    assert body["warning_equipment"] == 1
    assert body["active_incidents"] == 4
    assert body["overall_status"] == "critical"
    assert 0 < body["mean_detection_seconds"] < 60


def test_summary_validates_store_id(seeded):
    response = client.get("/api/v1/dashboard/summary/", {"store_id": "abc"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"


def test_summary_unknown_store_is_404(seeded):
    response = client.get("/api/v1/dashboard/summary/", {"store_id": 9999})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
