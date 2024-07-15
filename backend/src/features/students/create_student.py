from fastapi import HTTPException, APIRouter
from starlette import status

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from .model import Student
from .interfaces import IStudentsRepository

router = APIRouter()


@router.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student: Student) -> Student | None:
    return CreateStudentCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(student)


class CreateStudentCommandHandler:
    def __init__(self, students_repository: IStudentsRepository, contests_provider: IContestsProvider):
        self.students_repository = students_repository
        self.contests_provider = contests_provider

    def handle(self, student: Student) -> Student:
        if not self.contests_provider.validate_handle(student.handle):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Handle does not belong to CodeForces user'
            )

        self.students_repository.add_student(student)

        return student
