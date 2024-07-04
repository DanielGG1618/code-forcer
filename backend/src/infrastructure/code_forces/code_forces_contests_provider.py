from collections import defaultdict
from typing import Callable

from domain.student import Student
from domain.contest import Contest, Submission, Problem
from application.contests.contests_provider import IContestsProvider
from infrastructure.code_forces.requests_sending.code_forces_request_sender import (ICodeForcesRequestsSender,
                                                                                    IAnonymousCodeForcesRequestsSender)


class CodeForcesContestsProvider(IContestsProvider):
    requests_sender_factory: Callable[[str, str], ICodeForcesRequestsSender]
    anonymous_requests_sender_factory: Callable[[], IAnonymousCodeForcesRequestsSender]

    def __init__(self,
                 requests_sender_factory: Callable[[str, str], ICodeForcesRequestsSender],
                 anonymous_requests_sender_factory: Callable[[], IAnonymousCodeForcesRequestsSender]):
        self.requests_sender_factory = requests_sender_factory
        self.anonymous_requests_sender_factory = anonymous_requests_sender_factory

    def get_contest_results(self, contest_id: int, api_key: str, api_secret: str):
        requests_sender = self.requests_sender_factory(api_key, api_secret)

        _, _, rows = requests_sender.contest_standings(contest_id)

        return [
            {"handle": row.party.members[0].handle, "result": row.points}
            for row in rows
        ]

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
                verdict=cf_submission.verdict.value,
                passed_test_count=cf_submission.passedTestCount,
                points=cf_submission.points,
                programming_language=cf_submission.programmingLanguage
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

        return Contest(
            id=contest_id,
            name=cf_contest.name,
            phase=cf_contest.phase.value,
            problems=problems
        )

    def validate_handle(self, handle: str) -> bool:
        anonymous_requests_sender = self.anonymous_requests_sender_factory()
        return anonymous_requests_sender.validate_handle(handle) is not None
