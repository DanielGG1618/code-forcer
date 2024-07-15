from fastapi import HTTPException, status, APIRouter
from validate_email import validate_email

from src.container import container
from .interfaces import IStudentsRepository
from .model import Student

router = APIRouter()


@router.get("/students/{email_or_handle}", status_code=status.HTTP_200_OK)
async def get_student(email_or_handle: str) -> Student:
    return GetStudentQueryHandler(
        container[IStudentsRepository]
    ).handle(email_or_handle)


class GetStudentQueryHandler:
    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def handle(self, email_or_handle: str) -> Student:
        if validate_email(email_or_handle):
            response = self.students_repository.get_student_by_email(email_or_handle)

            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Student with given email is not found'
                )
        else:
            response = self.students_repository.get_student_by_handle(email_or_handle)

            if response is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Student with given handle is not found'
                )

        return response
