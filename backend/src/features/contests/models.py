from __future__ import annotations
from datetime import datetime, timedelta

from collections import defaultdict
from typing import Callable
from pydantic import BaseModel, EmailStr

from src.features.students.model import Student


class Contest(BaseModel):
    id: int
    name: str
    start_time_utc: datetime
    duration: timedelta
    problems: list[Problem]

    def map_handles_to_emails(self, handle_to_email_mapper: Callable[[str], EmailStr | None]) -> None:
        for problem in self.problems:
            problem.map_handles_to_emails(handle_to_email_mapper)

    def select_single_submission_for_each_participant(self, selector: Callable[[list[Submission]], Submission]) -> None:
        for problem in self.problems:
            problem.select_single_submission_for_each_participant(selector)

    @property
    def get_participants(self) -> set[Student]:
        return {
            participant
            for problem in self.problems
            for participant in problem.get_participants
        }


class Problem(BaseModel):
    index: str
    name: str
    max_points: float | None
    submissions: list[Submission]

    def map_handles_to_emails(self, handle_to_email_mapper: Callable[[str], EmailStr | None]) -> None:
        for submission in self.submissions:
            submission.map_author_handle_to_email(handle_to_email_mapper)

    def select_single_submission_for_each_participant(self, selector: Callable[[list[Submission]], Submission]) -> None:
        submissions_by_student = defaultdict(list[Submission])

        for submission in self.submissions:
            handle = submission.author.handle
            submissions_by_student[handle].append(submission)

        selected_submissions = [
            selector(submissions)
            for submissions
            in submissions_by_student.values()
        ]
        self.submissions = selected_submissions

    @property
    def get_participants(self) -> set[Student]:
        return {submission.author for submission in self.submissions}


class Submission(BaseModel):
    id: int
    author: Student
    is_successful: bool
    passed_test_count: int
    points: float | None
    programming_language: str
    submission_time_utc: datetime

    def map_author_handle_to_email(self, handle_to_email_mapper: Callable[[str], EmailStr | None]) -> None:
        if self.author.email is None:
            self.author.email = handle_to_email_mapper(self.author.handle)
