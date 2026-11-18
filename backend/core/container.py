"""Composition root: the only place that knows which concrete class implements
each abstraction (Dependency Inversion).

Views and management commands ask the container for a ready-to-use service;
services only ever see the interfaces from ``core.interfaces``. Swapping the
SQL repositories for an API client, or the simulator for a real controller
gateway, is a change in this file only.

Concrete imports are lazy so this module can be imported before Django apps
are ready.
"""

from functools import cached_property

from django.conf import settings


class Container:
    # -- Configuration -------------------------------------------------------------
    @cached_property
    def detection_config(self):
        from apps.detection.config import DetectionConfig

        return DetectionConfig.from_settings(settings.DETECTION, settings.TIME_ZONE)

    # -- Repositories --------------------------------------------------------------
    @cached_property
    def store_repository(self):
        from apps.stores.repositories import DjangoStoreRepository

        return DjangoStoreRepository()

    @cached_property
    def equipment_repository(self):
        from apps.equipment.repositories import DjangoEquipmentRepository

        return DjangoEquipmentRepository()

    @cached_property
    def reading_repository(self):
        from apps.telemetry.repositories import DjangoReadingRepository

        return DjangoReadingRepository()

    @cached_property
    def config_event_repository(self):
        from apps.telemetry.repositories import DjangoConfigEventRepository

        return DjangoConfigEventRepository()

    @cached_property
    def incident_repository(self):
        from apps.incidents.repositories import DjangoIncidentRepository

        return DjangoIncidentRepository()

    @cached_property
    def firmware_advisory(self):
        from apps.equipment.firmware import StaticFirmwareCatalog

        return StaticFirmwareCatalog()

    # -- Services ------------------------------------------------------------------
    def store_service(self):
        from apps.stores.services import StoreService

        return StoreService(self.store_repository)

    def equipment_service(self):
        from apps.equipment.services import EquipmentService

        return EquipmentService(
            stores=self.store_repository,
            equipment=self.equipment_repository,
            readings=self.reading_repository,
            incidents=self.incident_repository,
            firmware=self.firmware_advisory,
            divergence_threshold_c=self.detection_config.divergence_threshold_c,
        )

    def incident_service(self):
        from apps.incidents.services import IncidentService

        return IncidentService(
            stores=self.store_repository,
            incidents=self.incident_repository,
            config_events=self.config_event_repository,
        )

    def dashboard_service(self):
        from apps.dashboard.services import DashboardService

        return DashboardService(
            stores=self.store_repository,
            equipment=self.equipment_repository,
            incidents=self.incident_repository,
            readings=self.reading_repository,
            firmware=self.firmware_advisory,
        )

    def detection_service(self):
        import apps.detection.rules  # noqa: F401  (registers built-in rules)
        from apps.detection.engine import DetectionEngine
        from apps.detection.registry import rule_registry
        from apps.detection.services import DetectionService
        from apps.detection.status_policy import EquipmentStatusPolicy

        config = self.detection_config
        return DetectionService(
            equipment=self.equipment_repository,
            readings=self.reading_repository,
            config_events=self.config_event_repository,
            incidents=self.incident_repository,
            engine=DetectionEngine(rule_registry.build(config)),
            status_policy=EquipmentStatusPolicy(config.warning_margin_c),
            config=config,
        )

    def ingestion_service(self, reading_source, config_event_source=None):
        from apps.telemetry.services import TelemetryIngestionService

        return TelemetryIngestionService(
            equipment=self.equipment_repository,
            readings=self.reading_repository,
            config_events=self.config_event_repository,
            reading_source=reading_source,
            config_event_source=config_event_source,
            detection=self.detection_service(),
        )


container = Container()
