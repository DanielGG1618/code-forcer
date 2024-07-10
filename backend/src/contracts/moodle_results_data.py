from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr


class MoodleResultsData(BaseModel):
    contest: ContestData
    legally_excused: list[EmailStr]
    late_submission_policy: LateSubmissionPolicyData


class ContestData(BaseModel):
    id: int
    name: str
    start_time_utc: datetime
    duration: timedelta
    problems: list[ProblemData]


class ProblemData(BaseModel):
    name: str
    index: str
    max_points: int | None
    max_grade: int
    submissions: list[SubmissionData]


class SubmissionData(BaseModel):
    id: int
    author_email: EmailStr
    is_successful: bool
    passed_test_count: int
    points: int | None
    programming_language: str
    submission_time_utc: datetime


class LateSubmissionPolicyData(BaseModel):
    penalty: float
    extra_time: int
    # TODO: handle penalty (0.0 < extra_time 1.0)
