from datetime import UTC, datetime

import pytest

from core.container import Container
from simulation.seeder import DemoSeeder


@pytest.fixture
def seeded(db):
    """A short, deterministic demo: 1h of history with the attack 20 minutes ago."""
    container = Container()
    report = DemoSeeder(container, seed=7).run(
        now=datetime.now(UTC), hours=1, attack_minutes_ago=20
    )
    return container, report
