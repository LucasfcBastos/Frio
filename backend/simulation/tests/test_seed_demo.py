import pytest
from django.core.management import call_command

from core.enums import IncidentStatus

pytestmark = pytest.mark.django_db


def test_replay_opens_every_attack_incident_with_fast_detection(seeded):
    container, report = seeded

    incidents = container.incident_repository.list(status=IncidentStatus.ACTIVE)

    assert report.equipment == 8
    assert len(incidents) == 4
    assert {i.equipment_name for i in incidents} == {"Câmara de Congelados 02"}
    assert all(i.detection_seconds < 60 for i in incidents)


def test_simulate_command_appends_live_readings(seeded):
    container, _ = seeded
    before = container.reading_repository.last_recorded_at()

    call_command("simulate", iterations=1, interval=0)

    assert container.reading_repository.last_recorded_at() > before
