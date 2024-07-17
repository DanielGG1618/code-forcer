from fastapi import status

from src.features.contests.models import Contest
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
