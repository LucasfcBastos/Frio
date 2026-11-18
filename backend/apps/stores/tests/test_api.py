import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_lists_stores_paginated(seeded):
    response = APIClient().get("/api/v1/stores/")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert {s["name"] for s in body["results"]} == {"Loja Centro", "Loja Jundiaí"}
