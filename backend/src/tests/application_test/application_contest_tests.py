from application.contests.contests_service import ContestsService
from application.students.students_service import StudentsService

from contracts.student_data import StudentData

from application.students.students_repository import IStudentsRepository
from application.contests.contests_provider import IContestsProvider

from domain.contest import Contest, Problem, Submission
from domain.student import Student

from datetime import datetime, timedelta
from container import container

def test_get_contest():
    contests_service = ContestsService(IContestsProvider, IStudentsRepository)
    key = "da22f4ffb21dcaa93264dca546b55225c2cd82f5"
    secret = "ddb446df0943cf048db2f6678b211a3865dbe88a"
    contestId = 532926

    problem_a_submissions = [
        Submission(id=269320234, author=Student(handle="blazz1t", email=None), is_successful=True, passed_test_count=5,
                   points=0, programming_language="PyPy 3-64", submission_time_utc=datetime(2024, 7, 7, 21, 35, 15)),
        Submission(id=269059951, author=Student(handle="LayMorja", email=None), is_successful=True, passed_test_count=5,
                   points=0, programming_language="C++17 (GCC 7-32)", submission_time_utc=datetime(2024, 7, 6, 11, 4, 15))
    ]
    problem_b_submissions = [
        Submission(id=269068944, author=Student(handle="wyjjeless", email=None), is_successful=True, passed_test_count=5,
                   points=0, programming_language="C++20 (GCC 13-64)", submission_time_utc=datetime(2024, 7, 6, 12, 12, 2))
    ]

    problems = [
        Problem(index="A", name="Code Forcer", max_points=None, submissions=problem_a_submissions),
        Problem(index="B", name="Code Forcer", max_points=None, submissions=problem_b_submissions)
    ]

    contest = Contest(id=532926, name="Code Forcer Test", start_time_utc=datetime(2024, 7, 6, 8, 32),
                            duration=timedelta(days=31622400), problems=problems)

    result = container[ContestsService].get_contest(contestId, key, secret)

    assert result == result
