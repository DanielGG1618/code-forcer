from domain.student import Student
from domain.contest import Contest, Problem, Submission
from application.contests.contests_service import temp_most_passed_test_count_selector, temp_latest_submission_selector

from datetime import datetime, timedelta
from unittest import mock


def test_contest_map_handles_to_emails():
    # Arrange
    handle_to_email_mapper = mock.Mock()
    handle_to_email_mapper.side_effect = lambda handle: f"{handle}@example.com"

    student1 = Student(handle="student1", email=None)
    student2 = Student(handle="student2", email=None)
    student3 = Student(handle="student3", email="student3@example.com")

    submission1 = Submission(
        id=1,
        author=student1,
        is_successful=True,
        passed_test_count=10,
        points=100.0,
        submission_time_utc=datetime.now(),
        programming_language="Python"
    )
    submission2 = Submission(
        id=2,
        author=student2,
        is_successful=False,
        passed_test_count=8,
        points=80.0,
        submission_time_utc=datetime.now(),
        programming_language="Java"
    )
    submission3 = Submission(
        id=3,
        author=student3,
        is_successful=True,
        passed_test_count=5,
        points=50.0,
        submission_time_utc=datetime.now(),
        programming_language="C++"
    )

    problem1 = Problem(index="A", name="Problem A", max_points=100.0, submissions=[submission1, submission3])
    problem2 = Problem(index="B", name="Problem B", max_points=100.0, submissions=[submission2])

    contest = Contest(
        id=1,
        name="Contest 1",
        start_time_utc=datetime.now(),
        duration=timedelta(hours=2),
        problems=[problem1, problem2]
    )

    # Act
    contest.map_handles_to_emails(handle_to_email_mapper)

    # Assert
    assert student1.email == "student1@example.com"
    assert student2.email == "student2@example.com"
    assert student3.email == "student3@example.com"


def test_contest_select_single_submission_for_each_participant_most_points():
    # Arrange
    student1 = Student(handle="student1", email="example1@email.com")
    student2 = Student(handle="student2", email="example2@email.com")

    submissions: list[Submission] = [
        Submission(
            id=1,
            author=student1,
            is_successful=True,
            passed_test_count=10,
            points=100.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=2,
            author=student1,
            is_successful=False,
            passed_test_count=0,
            points=0.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=3,
            author=student1,
            is_successful=False,
            passed_test_count=5,
            points=50.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=4,
            author=student2,
            is_successful=False,
            passed_test_count=0,
            points=0.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=5,
            author=student2,
            is_successful=False,
            passed_test_count=7,
            points=70.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
    ]

    selector = mock.Mock()
    selector.side_effect = temp_most_passed_test_count_selector

    problem = Problem(index="A", name="Problem A", max_points=100.0, submissions=submissions)

    contest = Contest(
        id=1,
        name="Contest 1",
        start_time_utc=datetime.now(),
        duration=timedelta(hours=2),
        problems=[problem]
    )

    # Act
    contest.select_single_submission_for_each_participant(selector=selector)

    # Assert
    assert problem.submissions[0] == submissions[0]
    assert problem.submissions[1] == submissions[4]


def test_contest_select_single_submission_for_each_participant_latest_submission():
    # Arrange
    student1 = Student(handle="student1", email="example1@email.com")
    student2 = Student(handle="student2", email="example2@email.com")

    submissions: list[Submission] = [
        Submission(
            id=1,
            author=student1,
            is_successful=True,
            passed_test_count=10,
            submission_time_utc=datetime.now(),
            points=100.0,
            programming_language="Python"
        ),
        Submission(
            id=2,
            author=student1,
            is_successful=False,
            passed_test_count=0,
            points=0.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=3,
            author=student1,
            is_successful=False,
            passed_test_count=5,
            points=50.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=4,
            author=student2,
            is_successful=False,
            passed_test_count=0,
            points=0.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
        Submission(
            id=5,
            author=student2,
            is_successful=False,
            passed_test_count=7,
            points=70.0,
            submission_time_utc=datetime.now(),
            programming_language="Python"
        ),
    ]

    selector = mock.Mock()
    selector.side_effect = temp_latest_submission_selector

    problem = Problem(index="A", name="Problem A", max_points=100.0, submissions=submissions)

    contest = Contest(
        id=1,
        name="Contest 1",
        start_time_utc=datetime.now(),
        duration=timedelta(hours=2),
        problems=[problem]
    )

    # Act
    contest.select_single_submission_for_each_participant(selector=selector)

    # Assert
    assert problem.submissions[0] == submissions[2]
    assert problem.submissions[1] == submissions[4]
