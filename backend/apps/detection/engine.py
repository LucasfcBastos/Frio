"""Detection engine: runs every rule (Strategy) against a context.

The engine knows only ``BaseRule``; it never changes when rules are added.
"""

import logging
from collections.abc import Sequence

from core.interfaces import BaseRule, RuleContext, RuleResult

logger = logging.getLogger(__name__)


class DetectionEngine:
    def __init__(self, rules: Sequence[BaseRule]) -> None:
        self._rules = tuple(rules)

    @property
    def rule_codes(self) -> list[str]:
        return [rule.code for rule in self._rules]

    def evaluate(self, context: RuleContext) -> list[RuleResult]:
        results: list[RuleResult] = []
        for rule in self._rules:
            try:
                result = rule.evaluate(context)
            except Exception:  # One faulty rule must not blind the others.
                logger.exception("Rule %s failed for equipment %s", rule.code, context.equipment.id)
                continue
            if result is not None:
                results.append(result)
        return results
