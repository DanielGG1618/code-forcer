from fastapi import status, APIRouter

from src.container import container
from .interfaces import IStudentsRepository
from .model import Student

router = APIRouter()


@router.get("/students", status_code=status.HTTP_200_OK)
async def get_all_students() -> list[Student]:
    return GetAllStudentsCommandHandler(
        container[IStudentsRepository]
    ).handle()


class GetAllStudentsCommandHandler:
    def __init__(self, students_repository: IStudentsRepository):
        self.students_repository = students_repository

    def handle(self) -> list[Student]:
        return self.students_repository.get_all_students()
