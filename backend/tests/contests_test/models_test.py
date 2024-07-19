from datetime import datetime, timedelta

from src.features.students.model import Student
from src.features.contests.models import Contest, Problem, Submission
from src.features.contests.submission_selectors import submission_selectors
from tests.mocks.data_generation import fake


def test_contest_map_handles_to_emails():
    # Arrange
    def handle_to_email_mapper(handle: str):
        return f"{handle}@example.com"

    contest = fake.contest()

    unmapped_participants = [
        participant
        for participant in contest.get_participants
        if participant.email is None
    ]

    # Act
    contest.map_handles_to_emails(handle_to_email_mapper)

    # Assert
    for participant in unmapped_participants:
        assert participant.email == handle_to_email_mapper(participant.handle)


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

    selector = submission_selectors["most passed test count"]

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
            submission_time_utc=datetime.now() + timedelta(days=2),
            programming_language="Python"
        ),
        Submission(
            id=3,
            author=student1,
            is_successful=False,
            passed_test_count=5,
            points=50.0,
            submission_time_utc=datetime.now() + timedelta(days=3),
            programming_language="Python"
        ),
        Submission(
            id=4,
            author=student2,
            is_successful=False,
            passed_test_count=0,
            points=0.0,
            submission_time_utc=datetime.now() + timedelta(days=4),
            programming_language="Python"
        ),
        Submission(
            id=5,
            author=student2,
            is_successful=False,
            passed_test_count=7,
            points=70.0,
            submission_time_utc=datetime.now() + timedelta(days=5),
            programming_language="Python"
        ),
    ]

    selector = submission_selectors['latest']

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
