from fastapi import status, APIRouter, HTTPException
from pydantic import EmailStr

from src.container import container
from .interfaces import IStudentsRepository

router = APIRouter()


@router.delete("/students/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(email: EmailStr) -> None:
    DeleteStudentCommandHandler(
        container[IStudentsRepository]
    ).handle(email)


class DeleteStudentCommandHandler:
    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def handle(self, email: EmailStr) -> None:
        if not self.students_repository.email_exists(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Student with given email is not found'
            )

        self.students_repository.delete_student(email)
