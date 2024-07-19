from collections import defaultdict
from datetime import datetime, timedelta
from typing import Callable

from fastapi import HTTPException, status
from pytz import timezone

from src.features.students.models import Student
from src.features.contests.models import Contest, Submission, Problem
from src.features.contests.interfaces import IContestsProvider
from .enums import CfVerdict
from .request_sender import ICodeForcesRequestsSender, IAnonymousCodeForcesRequestsSender


class CodeForcesContestsProvider(IContestsProvider):
    requests_sender_factory: Callable[[str, str], ICodeForcesRequestsSender]
    anonymous_requests_sender_factory: Callable[[], IAnonymousCodeForcesRequestsSender]

    def __init__(
            self,
            requests_sender_factory: Callable[[str, str], ICodeForcesRequestsSender],
            anonymous_requests_sender_factory: Callable[[], IAnonymousCodeForcesRequestsSender]
    ):
        self.requests_sender_factory = requests_sender_factory
        self.anonymous_requests_sender_factory = anonymous_requests_sender_factory

    def get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
        requests_sender = self.requests_sender_factory(api_key, api_secret)

        cf_submissions = requests_sender.contest_status(contest_id)
        cf_contest, cf_problems, _ = requests_sender.contest_standings(contest_id)

        submissions_by_problem_index = defaultdict(list)
        for cf_submission in cf_submissions:
            problem_index = cf_submission.problem.index
            submission = Submission(
                id=cf_submission.id,
                author=Student(
                    handle=cf_submission.author.members[0].handle
                ),
                is_successful=cf_submission.verdict == CfVerdict.OK,
                passed_test_count=cf_submission.passedTestCount,
                points=cf_submission.points,
                programming_language=cf_submission.programmingLanguage,
                submission_time_utc=datetime.fromtimestamp(cf_submission.creationTimeSeconds, tz=timezone("utc"))
            )
            submissions_by_problem_index[problem_index].append(submission)

        problems = [
            Problem(
                index=cf_problem.index,
                name=cf_problem.name,
                max_points=cf_problem.points,
                submissions=submissions_by_problem_index[cf_problem.index]
            ) for cf_problem in cf_problems
        ]

        for problem in problems:
            if problem.max_points is None:
                problem.max_points = _get_max_points_from_submissions(problem)

        return Contest(
            id=contest_id,
            name=cf_contest.name,
            start_time_utc=datetime.fromtimestamp(cf_contest.startTimeSeconds, tz=timezone("utc")),
            duration=timedelta(seconds=cf_contest.durationSeconds),
            problems=problems
        )

    def validate_handle(self, handle: str) -> bool:
        if ';' in handle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='CodeForces handle cannot contain \';\''
            )

        anonymous_requests_sender = self.anonymous_requests_sender_factory()
        return anonymous_requests_sender.validate_handle(handle) is not None


def _get_max_points_from_submissions(problem: Problem) -> float:
    for submission in problem.submissions:
        if submission.is_successful:
            return submission.points

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Max points for the problem {problem.index} is undefined'
    )
