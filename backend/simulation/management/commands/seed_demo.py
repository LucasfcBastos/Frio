from datetime import UTC, datetime, time

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.container import container
from simulation.seeder import DemoSeeder


class Command(BaseCommand):
    help = "Reset the database and replay a demo history (including the defrost attack)."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--hours", type=int, default=6, help="History length (default 6).")
        parser.add_argument(
            "--attack-at",
            type=time.fromisoformat,
            default=None,
            help="Local clock time of the attack, e.g. 02:07 (must fall inside --hours).",
        )
        parser.add_argument(
            "--attack-minutes-ago",
            type=int,
            default=95,
            help="When --attack-at is not given, start the attack this many minutes ago.",
        )
        parser.add_argument("--seed", type=int, default=42, help="Random seed (reproducible).")

    def handle(self, *args, **options) -> None:
        seeder = DemoSeeder(container, seed=options["seed"])
        try:
            with transaction.atomic():
                report = seeder.run(
                    now=datetime.now(UTC),
                    hours=options["hours"],
                    attack_at=options["attack_at"],
                    attack_minutes_ago=options["attack_minutes_ago"],
                )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        local = report.attack_started_at.astimezone(
            container.detection_config.defrost_schedule.timezone
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {report.stores} stores, {report.equipment} equipment, "
                f"{report.steps} minutes of history. Attack started at {local:%H:%M}; "
                f"{report.incidents} incidents detected."
            )
        )
