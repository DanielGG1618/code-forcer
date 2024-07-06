from __future__ import annotations

from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta


@dataclass
class MoodleResultsData:
    contest: ContestData
    legally_excused: List[str]
    late_submission_rules: LateSubmissionRulesData


@dataclass
class ContestData:
    id: int
    name: str
    start_time: datetime
    duration: timedelta
    problems: List[ProblemData]


@dataclass
class ProblemData:
    name: str
    index: str
    max_points: int | None
    max_grade: int
    submissions: List[SubmissionData]


@dataclass
class SubmissionData:
    id: int
    author_email: str
    verdict: str
    passed_test_count: int
    points: int | None
    programming_language: str


@dataclass
class LateSubmissionRulesData:
    pass
