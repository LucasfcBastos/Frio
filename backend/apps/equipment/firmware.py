"""Firmware advisory: which controller firmware versions are outdated.

MVP: a static catalog of the latest known-good release per controller model.
A production implementation could pull vendor advisories / CVE feeds while
keeping the same ``FirmwareAdvisory`` contract.
"""

from core.interfaces import FirmwareAdvisory

DEFAULT_LATEST_FIRMWARE: dict[tuple[str, str], str] = {
    ("Polarix", "PX-400"): "3.2.0",
    ("CryoTech", "CT-Edge 2"): "2.8.4",
    ("Glacial Systems", "GS-Ctrl 7"): "5.1.0",
}


def _parse(version: str) -> tuple[int, ...]:
    parts = []
    for chunk in version.strip().lstrip("vV").split("."):
        digits = "".join(ch for ch in chunk if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


class StaticFirmwareCatalog(FirmwareAdvisory):
    def __init__(self, latest: dict[tuple[str, str], str] | None = None) -> None:
        self._latest = latest if latest is not None else DEFAULT_LATEST_FIRMWARE

    def latest_version(self, manufacturer: str, model: str) -> str | None:
        return self._latest.get((manufacturer, model))

    def is_outdated(self, manufacturer: str, model: str, firmware_version: str) -> bool:
        latest = self.latest_version(manufacturer, model)
        return latest is not None and _parse(firmware_version) < _parse(latest)
