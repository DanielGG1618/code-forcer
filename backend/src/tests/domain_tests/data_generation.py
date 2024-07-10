from datetime import timedelta
from random import choice

from faker import Faker
from faker.providers import BaseProvider

from domain.contest import Contest, Problem, Submission
from domain.student import Student

fake = Faker()


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

contest = fake.contest()
print(contest)
