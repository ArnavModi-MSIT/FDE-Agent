from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    """One check's full evidence, not just pass/fail. Never enters the
    submission CSV -- exists for debugging, W2's future exception-report
    aggregation, and human review, exactly per the review that asked for
    it: 'observed vs expected vs reason', not a bare boolean."""

    check: str
    passed: bool
    observed: Any
    expected: Any
    reason: str
