from collections.abc import Callable, Sequence
from datetime import datetime


def trailing_streak_start[T](
    items: Sequence[T], predicate: Callable[[T], bool], timestamp: Callable[[T], datetime]
) -> datetime | None:
    """Timestamp of the first item of the streak that satisfies ``predicate`` up to now.

    Returns ``None`` when the most recent item does not satisfy it.
    """
    start: datetime | None = None
    for item in reversed(items):
        if not predicate(item):
            break
        start = timestamp(item)
    return start
