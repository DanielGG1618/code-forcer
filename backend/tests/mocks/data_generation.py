from datetime import timedelta
from random import choice

from faker import Faker
from faker.providers import BaseProvider

from src.features.contests.models import Contest, Problem, Submission
from src.features.moodle_grades.models import (
    MoodleResultsData,
    LateSubmissionPolicyData,
    ContestData,
    ProblemData,
    SubmissionData
)
from src.features.students.model import Student

fake = Faker('en-US')


class MoodleResultsDataProvider(BaseProvider):
    @staticmethod
    def moodle_results_data() -> MoodleResultsData:
        contest_data: ContestData = fake.contest_data()

        return MoodleResultsData(
            contest=contest_data,
            legally_excused=[
                submission.author_email
                for submission
                in choice(contest_data.problems).submissions
                if fake.pyfloat(min_value=0, max_value=1) < 0.3
            ],
            late_submission_policy=fake.late_submission_policy_data()
        )


class ContestDataProvider(BaseProvider):
    @staticmethod
    def contest_data() -> ContestData:
        participants = [
            fake.unique.email()
            for _ in range(fake.random_int(min=20, max=100))
        ]

        problems: list[ProblemData] = [
            fake.problem_data()
            for _ in range(fake.random_int(min=1, max=10))
        ]

        for problem in problems:
            for submission in problem.submissions:
                submission.author_email = choice(participants)

        return ContestData(
            id=fake.unique.random_int(min=1, max=1000000),
            name=fake.name(),
            start_time_utc=fake.date_time(),
            duration=timedelta(hours=fake.random_int(min=1, max=10)),
            problems=problems,
        )


class ProblemDataProvider(BaseProvider):
    @staticmethod
    def problem_data() -> ProblemData:
        return ProblemData(
            name=fake.name(),
            index=fake.unique.random_letter(),
            max_points=fake.random_int(min=1, max=10),
            max_grade=fake.random_int(min=1, max=10),
            submissions=[
                fake.submission_data()
                for _ in range(fake.random_int(min=50, max=200))
            ],
        )


class SubmissionDataProvider(BaseProvider):
    @staticmethod
    def submission_data() -> SubmissionData:
        return SubmissionData(
            id=fake.unique.random_int(min=1, max=1000000),
            author_email=fake.email(),
            is_successful=fake.boolean(),
            passed_test_count=fake.random_int(min=1, max=100),
            points=fake.random_int(min=1, max=10),
            submission_time_utc=fake.date_time(),
            programming_language=fake.language_name()
        )


class LateSubmissionPolicyDataProvider(BaseProvider):
    @staticmethod
    def late_submission_policy_data() -> LateSubmissionPolicyData:
        return LateSubmissionPolicyData(
            penalty=fake.pyfloat(min_value=0, max_value=1),
            extra_time=fake.random_int(min=3600, max=360000)
        )


class ContestProvider(BaseProvider):
    @staticmethod
    def contest() -> Contest:
        result = Contest(
            id=fake.unique.random_int(min=1, max=1000000),
            name=fake.name(),
            start_time_utc=fake.date_time(),
            duration=timedelta(hours=fake.random_int(min=1, max=10)),
            problems=[fake.problem() for _ in range(fake.random_int(min=1, max=5))],
        )

        students_list = [fake.student() for _ in range(fake.random_int(min=1, max=10))]

        for problem in result.problems:
            for submission in problem.submissions:
                submission.author = choice(students_list)

        return result


class ProblemProvider(BaseProvider):
    @staticmethod
    def problem() -> Problem:
        return Problem(
            index=fake.random_letter(),
            name=fake.name(),
            max_points=fake.pyfloat(min_value=0, max_value=100),
            submissions=[fake.submission() for _ in range(fake.random_int(min=0, max=100))]
        )


class SubmissionProvider(BaseProvider):
    @staticmethod
    def submission() -> Submission:
        return Submission(
            id=fake.unique.random_int(min=1, max=1000000),
            author=fake.student(),
            is_successful=fake.boolean(),
            passed_test_count=fake.pyint(min_value=0, max_value=100),
            points=fake.pyint(min_value=0, max_value=100),
            programming_language=fake.language_name(),
            submission_time_utc=fake.date_time()
        )


class StudentProvider(BaseProvider):
    @staticmethod
    def student() -> Student:
        return Student(
            email=fake.email() if fake.boolean() else None,
            handle=fake.first_name(),
        )


fake.add_provider(ContestProvider)
fake.add_provider(ProblemProvider)
fake.add_provider(SubmissionProvider)
fake.add_provider(StudentProvider)
fake.add_provider(MoodleResultsDataProvider)
fake.add_provider(ContestDataProvider)
fake.add_provider(ProblemDataProvider)
fake.add_provider(SubmissionDataProvider)
fake.add_provider(LateSubmissionPolicyDataProvider)
