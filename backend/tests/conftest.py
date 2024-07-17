import pytest

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from src.features.students.interfaces import IStudentsRepository
from src.features.students.model import Student
from tests.mocks.contests_provider_mock import ContestsProviderMock
from tests.mocks.data_generation import fake
from tests.mocks.students_repository_mock import StudentRepositoryMock


@pytest.fixture(autouse=True)
def setup_and_teardown(contests_provider_mock, students_repo_mock):
    yield
    contests_provider_mock.valid_handles = []
    students_repo_mock.db.clear()
    print('mocks cleared')


@pytest.fixture
def contests_provider_mock():
    contests_provider_mock_instance = ContestsProviderMock()
    container[IContestsProvider] = contests_provider_mock_instance
    return contests_provider_mock_instance


@pytest.fixture
def students_repo_mock():
    students_repo_mock_instance = StudentRepositoryMock()
    container[IStudentsRepository] = students_repo_mock_instance
    return students_repo_mock_instance


@pytest.fixture
def email():
    return fake.email()


@pytest.fixture
def existing_email(students_repo_mock, email, handle):
    if not students_repo_mock.db.get(email):
        students_repo_mock.db[email] = Student(email=email, handle=handle)

    return email


@pytest.fixture
def invalid_email(email):
    return email + '!'


@pytest.fixture
def handle(contests_provider_mock):
    faked_handle = fake.word()
    contests_provider_mock.valid_handles = [faked_handle]
    return faked_handle


@pytest.fixture
def existing_handle(students_repo_mock, contests_provider_mock, email, handle):
    contests_provider_mock.valid_handles = [handle]

    if not students_repo_mock.db.get(email):
        students_repo_mock.db[email] = Student(email=email, handle=handle)

    return handle


@pytest.fixture
def invalid_handle():
    return fake.word()


@pytest.fixture
def contest(contests_provider_mock):
    contest = fake.contest()

    contests_provider_mock.contests[contest.id] = contest.model_copy(deep=True)

    return contest
