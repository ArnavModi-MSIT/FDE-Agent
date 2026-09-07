from ..matching.resolver import MatchResult
from ..models.check_result import CheckResult


def check_po_exists(match_result: MatchResult) -> CheckResult:
    """Thin consumer of matching/resolver.py's result -- deliberately never
    re-derives PO existence independently, so this can't disagree with what
    matching/ actually found."""
    return CheckResult(
        check="po_exists",
        passed=match_result.matched,
        observed=match_result.match_type,
        expected="exact or normalized",
        reason="no purchase order found for this po_number"
        if not match_result.matched
        else f"purchase order located via {match_result.match_type} match",
    )
