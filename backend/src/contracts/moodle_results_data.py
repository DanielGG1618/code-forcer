from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class MoodleResultsData:
    contest: ContestData
    legally_excused: list[str]
    late_submission_rules: LateSubmissionRulesData


@dataclass
class ContestData:
    id: int
    name: str
    start_time_utc: datetime
    duration: timedelta
    problems: list[ProblemData]


@dataclass
class ProblemData:
    name: str
    index: str
    max_points: int | None
    max_grade: int
    submissions: list[SubmissionData]


@dataclass
class SubmissionData:
    id: int
    author_email: str
    is_successful: bool
    passed_test_count: int
    points: int | None
    programming_language: str


@dataclass
class LateSubmissionRulesData:
    pass
