import os

from src.features.contests.interfaces import IContestsProvider
from src.features.students.interfaces import IStudentsRepository
from src.infrastructure.storage.db_students_repository import DBStudentsRepository
from src.infrastructure.code_forces.request_sender import CodeForcesRequestsSender
from src.infrastructure.code_forces.contests_provider import CodeForcesContestsProvider
from src.utils.dependencies_container import DependenciesContainer

db_connection_string = os.getenv('DB_CONNECTION_STRING', 'students.db')

container = DependenciesContainer()

container[IContestsProvider] = lambda: CodeForcesContestsProvider(
    requests_sender_factory=CodeForcesRequestsSender,
    anonymous_requests_sender_factory=CodeForcesRequestsSender
)
container[IStudentsRepository] = lambda: DBStudentsRepository(db_connection_string)
