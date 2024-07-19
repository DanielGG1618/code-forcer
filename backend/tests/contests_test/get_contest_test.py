from datetime import datetime, timedelta

from fastapi import status

from src.features.contests.models import Contest, Submission
from src.features.students.model import Student
from tests.create_test_client import client
from tests.mocks.data_generation import fake


def test_gets_contest_when_contest_exists(contest):
    response = client.get(f"/contests/{contest.id}", params={"key": "", "secret": ""})

    assert response.status_code == status.HTTP_200_OK

    response_contest = Contest.model_validate_json(response.text)

    assert response_contest.id == contest.id
    assert response_contest.name == contest.name
    assert response_contest.start_time_utc == contest.start_time_utc
    assert response_contest.duration == contest.duration
    for response_problem in response_contest.problems:
        problem = None
        for problem in contest.problems:
            if problem.index == response_problem.index:
                break
        else:
            assert False, f"Problem with index {response_problem.index} not found in the original contest"

        assert response_problem.name == problem.name
        assert response_problem.max_points == problem.max_points


def test_gets_contest_with_single_submission_foreach_student(contest):
    response = client.get(f"/contests/{contest.id}", params={"key": "", "secret": ""})

    assert response.status_code == status.HTTP_200_OK

    response_contest = Contest.model_validate_json(response.text)

    for response_problem in response_contest.problems:
        for problem in contest.problems:
            if problem.index == response_problem.index:
                break
        else:
            assert False, f"Problem with index {response_problem.index} not found in the original contest"

        submission_authors: set[str] = set()

        for response_submission in response_problem.submissions:
            assert response_submission.author.handle not in submission_authors

            submission_authors.add(response_submission.author.handle)


def test_gets_contest_with_mapped_emails_foreach_student(contest, students_repo_mock):
    students_by_email = {
        (fake_email := fake.email()): Student(email=fake_email, handle=student.handle)
        for student
        in contest.get_participants
        if student.email is None
    }

    students_repo_mock.db |= students_by_email

    response = client.get(f"/contests/{contest.id}", params={"key": "", "secret": ""})

    assert response.status_code == status.HTTP_200_OK

    response_contest = Contest.model_validate_json(response.text)
    for student in response_contest.get_participants:
        assert student.email is not None
        if student.email in students_by_email:
            assert student == students_by_email[student.email]


def test_gets_contest_with_latest_submission_for_each_student_if_selected_selector_is_latest(
        contest,
        contests_provider_mock
):
    [problem] = contest.problems = contest.problems[:1]
    problem.submissions = [
        Submission(
            id=1,
            author=Student(handle="student1", email=None),
            is_successful=True,
            passed_test_count=10,
            points=100.0,
            submission_time_utc=datetime.now(),
            programming_language="С#"
        ),
        Submission(
            id=2,
            author=Student(handle="student1", email=None),
            is_successful=False,
            passed_test_count=0,
            points=50.0,
            submission_time_utc=datetime.now() + timedelta(days=2),
            programming_language="Haskell"
        ),
        Submission(
            id=3,
            author=Student(handle="student1", email=None),
            is_successful=False,
            passed_test_count=0,
            points=0.0,
            submission_time_utc=datetime.now() + timedelta(days=3),
            programming_language="Python"
        )
    ]

    contests_provider_mock.contests[contest.id] = contest

    response = client.get(f"/contests/{contest.id}", params={
        "key": "", "secret": "",
        "submission_selector_name": "latest"
    })

    assert response.status_code == status.HTTP_200_OK

    response_contest = Contest.model_validate_json(response.text)
    assert len(response_contest.get_participants) == 1
    assert response_contest.problems[0].submissions[0].id == 3
