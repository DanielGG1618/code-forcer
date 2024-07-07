from abc import ABC, abstractmethod
from pydantic import EmailStr

from domain.student import Student


class IStudentsRepository(ABC):
    @abstractmethod
    def add_student(self, student: Student):
        pass

    @abstractmethod
    def get_student_by_email(self, email: EmailStr) -> Student:
        pass

    @abstractmethod
    def get_all_students(self) -> list[Student]:
        pass

    @abstractmethod
    def get_student_by_handle(self, handle: str) -> Student:
        pass

    @abstractmethod
    def update_student(self, email: EmailStr, new_student: Student) -> None:
        pass

    @abstractmethod
    def delete_student(self, email: EmailStr) -> None:
        pass

    @abstractmethod
    def email_exists(self, email: EmailStr) -> bool:
        pass

    @abstractmethod
    def handle_exists(self, handle: str) -> bool:
        pass

    @abstractmethod
    def student_exists(self, student: Student) -> bool:
        pass
