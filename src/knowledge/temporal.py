from datetime import date

# Fixed, not datetime.date.today() -- reproducibility matters here the same
# way it does for the reconciliation engine's DEFAULT_AS_OF-style constants;
# reading the wall clock would make the same question answerable
# differently on different days. Set to this project's own working date.
# Doesn't actually affect any answer's correctness: every "today" question
# in the practice set resolves to PP-2023 regardless of the exact day
# chosen, since any date this far past 2023-10-01 gives the same result.
KNOWLEDGE_AS_OF = date(2026, 9, 7)


def resolve_transaction_date(month: int, year: int, default: date = KNOWLEDGE_AS_OF) -> date:
    """A question either states an explicit month+year, or asks about
    'today' with no date at all -- in which case `default` (KNOWLEDGE_AS_OF)
    applies. Uses day=1 for an explicit month/year since no question ever
    gives a specific day -- correct because every date-band boundary this
    project's policy_kb checks against falls on the 1st of a month anyway
    (2023-10-01), so day-of-month granularity never changes which policy
    applies."""
    if month is None or year is None:
        return default
    return date(year, month, 1)


def add_months(d: date, months: int) -> date:
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, 1)
