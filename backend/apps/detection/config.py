"""Typed detection configuration, built once from ``settings.DETECTION``."""

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo


@dataclass(frozen=True, slots=True)
class TimeWindow:
    start: time
    end: time

    def contains(self, moment: time) -> bool:
        if self.start <= self.end:
            return self.start <= moment < self.end
        return moment >= self.start or moment < self.end  # Window crosses midnight.

    def __str__(self) -> str:
        return f"{self.start:%H:%M}-{self.end:%H:%M}"


@dataclass(frozen=True, slots=True)
class DefrostSchedule:
    """Programmed defrost windows, expressed in the store's local time."""

    windows: tuple[TimeWindow, ...]
    timezone: ZoneInfo

    @classmethod
    def parse(cls, raw: list[str], timezone: str) -> "DefrostSchedule":
        windows = []
        for item in raw:
            start, end = item.split("-")
            windows.append(TimeWindow(time.fromisoformat(start), time.fromisoformat(end)))
        return cls(windows=tuple(windows), timezone=ZoneInfo(timezone))

    def is_scheduled(self, moment: datetime) -> bool:
        local = moment.astimezone(self.timezone).time()
        return any(window.contains(local) for window in self.windows)

    def local_time(self, moment: datetime) -> str:
        return moment.astimezone(self.timezone).strftime("%H:%M")

    def __str__(self) -> str:
        return ", ".join(str(w) for w in self.windows)


@dataclass(frozen=True, slots=True)
class DetectionConfig:
    defrost_schedule: DefrostSchedule
    divergence_threshold_c: float = 4.0
    setpoint_change_limit_c: float = 5.0
    warning_margin_c: float = 1.0
    context_readings: int = 15
    config_event_lookback: timedelta = field(default=timedelta(minutes=10))

    @classmethod
    def from_settings(cls, raw: dict, timezone: str) -> "DetectionConfig":
        return cls(
            defrost_schedule=DefrostSchedule.parse(raw["DEFROST_WINDOWS"], timezone),
            divergence_threshold_c=raw["DIVERGENCE_THRESHOLD_C"],
            setpoint_change_limit_c=raw["SETPOINT_CHANGE_LIMIT_C"],
            warning_margin_c=raw["WARNING_MARGIN_C"],
            context_readings=raw["CONTEXT_READINGS"],
            config_event_lookback=timedelta(minutes=raw["CONFIG_EVENT_LOOKBACK_MINUTES"]),
        )
