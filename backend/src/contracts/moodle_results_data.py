from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class MoodleResultsData:
    contest: ContestData
    plagiarizers: List[str]
    legally_excused: List[str]
    late_submission_rules: LateSubmissionRulesData


@dataclass
class ContestData:
    id: int
    name: str
    problems: List[ProblemData]


@dataclass
class ProblemData:
    name: str
    index: str
    max_points: int
    max_grade: int
    submissions: List[SubmissionData]


@dataclass
class SubmissionData:
    id: int
    author_email: str
    verdict: str
    passed_test_count: int
    points: int
    programming_language: str


@dataclass
class LateSubmissionRulesData:
    pass
