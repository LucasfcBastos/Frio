"""Rule registry: the extension point that keeps the engine closed for modification.

Adding a detection rule = create a ``BaseRule`` subclass decorated with
``@rule_registry.register``. Neither the engine nor the service changes.
"""

from apps.detection.config import DetectionConfig
from core.interfaces import BaseRule


class RuleRegistry:
    def __init__(self) -> None:
        self._rules: dict[str, type[BaseRule]] = {}

    def register(self, rule_cls: type[BaseRule]) -> type[BaseRule]:
        if rule_cls.code in self._rules:
            raise ValueError(f"Rule code '{rule_cls.code}' is already registered.")
        self._rules[rule_cls.code] = rule_cls
        return rule_cls

    def codes(self) -> list[str]:
        return list(self._rules)

    def build(self, config: DetectionConfig) -> list[BaseRule]:
        """Instantiate every registered rule with the shared configuration."""
        return [rule_cls(config) for rule_cls in self._rules.values()]


rule_registry = RuleRegistry()
