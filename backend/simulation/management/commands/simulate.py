import random
import time
from datetime import UTC, datetime

from django.core.management.base import BaseCommand

from core.container import container
from simulation.live import build_live_source


class Command(BaseCommand):
    help = "Generate one reading per equipment every N seconds and run the detection engine."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--interval", type=float, default=5.0, help="Seconds between ticks.")
        parser.add_argument(
            "--iterations", type=int, default=0, help="Stop after N ticks (0 = run forever)."
        )
        parser.add_argument("--seed", type=int, default=None)

    def handle(self, *args, **options) -> None:
        source = build_live_source(container, random.Random(options["seed"]))
        ingestion = container.ingestion_service(source, source)
        interval, iterations = options["interval"], options["iterations"]
        self.stdout.write(f"Simulating every {interval:g}s. Press Ctrl+C to stop.")

        tick = 0
        try:
            while iterations == 0 or tick < iterations:
                report = ingestion.ingest(datetime.now(UTC))
                tick += 1
                line = f"[{report.at:%H:%M:%S}Z] {report.readings} readings"
                for incident in report.incidents:
                    line += f" | NEW {incident.severity.upper()}: {incident.title}"
                self.stdout.write(line)
                if iterations == 0 or tick < iterations:
                    time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write("Stopped.")
