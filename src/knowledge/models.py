from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedQuestion:
    """The structured parameters extracted from a question's free text.
    `topic` is None when nothing recognized -- caller must never guess a
    topic just because SOME fields parsed."""

    topic: Optional[str]
    amount_rupees: Optional[float] = None
    month: Optional[int] = None
    year: Optional[int] = None
    second_month: Optional[int] = None  # for warranty questions with two dates
    second_year: Optional[int] = None
    tier: Optional[str] = None
    is_flowtech_pre_acquisition: bool = False


@dataclass(frozen=True)
class Answer:
    qid: str
    answer: str
    governing_source: str
    reasoning: str  # never enters the CSV -- for debugging/human review only
