from fastapi import Response, HTTPException, status, APIRouter
from validate_email import validate_email

from src.container import container
from src.features.contests.interfaces import IContestsProvider
from .interfaces import IStudentsRepository
from .model import Student

router = APIRouter()


@router.put("/students/{email_or_handle}")
async def update_or_create_student(
        email_or_handle: str,
        updated_student: Student,
        response: Response
) -> Student | None:
    result = UpdateOrCreateStudentCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(email_or_handle, updated_student)

    if result is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return None

    response.status_code = status.HTTP_201_CREATED
    return result


class UpdateOrCreateStudentCommandHandler:
    def __init__(self, students_repository: IStudentsRepository, contests_provider: IContestsProvider):
        self.students_repository = students_repository
        self.contests_provider = contests_provider

    def handle(self, email_or_handle: str, student: Student) -> Student | None:
        if validate_email(email_or_handle):
            email = email_or_handle.lower()

            if email != student.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email from URL should match email from reqeust body"
                )

            if not self.contests_provider.validate_handle(student.handle):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Handle does not belong to CodeForces user'
                )

            if self.students_repository.email_exists(email):
                self.students_repository.update_student_by_email(email, student)
                return None

        else:
            handle = email_or_handle.lower()

            if handle != student.handle:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Handle from URL should match handle from reqeust body"
                )

            if not self.contests_provider.validate_handle(student.handle):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Handle does not belong to CodeForces user'
                )

            if self.students_repository.handle_exists(handle):
                self.students_repository.update_student_by_handle(handle, student)
                return None

        self.students_repository.add_student(student)
        return student
