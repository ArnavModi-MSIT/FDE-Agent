"""Question text -> ParsedQuestion. Regex-based, not an LLM call --
matches this project's deterministic-first discipline, and every practice
question follows a consistent template shape. If the hidden/rotated set
uses genuinely different phrasing this won't generalize -- that's a real,
documented limitation (see CLAUDE.md), not silently assumed away: an
unrecognized question produces topic=None, which answering.py refuses to
guess an answer for, rather than a wrong confident one."""
import re
from typing import List, Optional, Tuple

from .models import ParsedQuestion

_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}
_MONTH_PATTERN = re.compile(
    r"\b(" + "|".join(_MONTHS.keys()) + r")\s+(\d{4})\b", re.IGNORECASE
)
_AMOUNT_PATTERN = re.compile(r"Rs\.?\s*([\d,]+)")

# "Standard" is a genuine tier name in this business's data (customers.csv
# has real Standard-tier accounts alongside Gold/Platinum), but the word
# also appears as a plain adjective ("the standard credit terms") unrelated
# to any specific tier -- e.g. K-02 says "standard credit terms for a
# Gold-tier distributor," where a bare-word search wrongly grabs "standard"
# instead of the real answer, "Gold." Require the "-tier"/" tier" suffix
# first (a real tier DESIGNATION, not a description) and only fall back to
# a bare word if no suffixed form exists anywhere in the text.
_TIER_SUFFIXED_PATTERN = re.compile(r"\b(Gold|Platinum|Silver|Standard)[\s-]+tier\b", re.IGNORECASE)
_TIER_BARE_PATTERN = re.compile(r"\b(Gold|Platinum|Silver|Standard)\b", re.IGNORECASE)

# Ordered most-specific-first: the first topic whose keyword set is fully
# present wins. Prevents e.g. a warranty question that also happens to
# mention an amount from being misrouted to "discount".
_TOPIC_KEYWORDS: List[Tuple[str, List[str]]] = [
    ("warranty_flowtech", ["warranty", "flowtech"]),
    ("warranty_calc", ["warranty", "despatch"]),
    ("warranty_calc", ["warranty", "dispatch"]),
    ("vendor_documents", ["document", "vendor", "submit"]),
    ("trial_po_cap", ["trial", "purchase order"]),
    ("approval_matrix", ["approval"]),
    ("restocking_charge", ["restocking"]),
    ("price_revision_notice", ["notice", "revis"]),
    ("credit_terms", ["credit terms"]),
    ("freight", ["freight"]),
    ("discount", ["discount"]),
]


def _classify_topic(text_lower: str) -> Optional[str]:
    for topic, keywords in _TOPIC_KEYWORDS:
        if all(kw in text_lower for kw in keywords):
            return topic
    return None


def _extract_amount(text: str) -> Optional[float]:
    match = _AMOUNT_PATTERN.search(text)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def _extract_month_years(text: str) -> List[Tuple[int, int]]:
    return [(_MONTHS[m.lower()], int(y)) for m, y in _MONTH_PATTERN.findall(text)]


def _extract_tier(text: str) -> Optional[str]:
    match = _TIER_SUFFIXED_PATTERN.search(text)
    if match:
        return match.group(1)
    match = _TIER_BARE_PATTERN.search(text)
    return match.group(1) if match else None


def parse_question(text: str) -> ParsedQuestion:
    text_lower = text.lower()
    topic = _classify_topic(text_lower)
    if topic is None:
        return ParsedQuestion(topic=None)

    dates = _extract_month_years(text)
    month, year = (dates[0] if dates else (None, None))
    second_month, second_year = (dates[1] if len(dates) > 1 else (None, None))

    return ParsedQuestion(
        topic=topic,
        amount_rupees=_extract_amount(text),
        month=month,
        year=year,
        second_month=second_month,
        second_year=second_year,
        tier=_extract_tier(text),
        is_flowtech_pre_acquisition=("flowtech" in text_lower and "pre-acquisition" in text_lower),
    )
