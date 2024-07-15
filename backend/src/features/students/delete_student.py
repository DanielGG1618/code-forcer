from fastapi import status, APIRouter

from src.container import container
from .interfaces import IStudentsRepository

router = APIRouter()


@router.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: str) -> None:
    DeleteStudentCommandHandler(
        container[IStudentsRepository]
    ).handle(email)


class DeleteStudentCommandHandler:
    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def handle(self, email: str) -> None:
        self.students_repository.delete_student(email)
