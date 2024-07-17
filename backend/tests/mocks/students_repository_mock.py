from pydantic import EmailStr

from src.features.students.interfaces import IStudentsRepository
from src.features.students.model import Student


class StudentRepositoryMock(IStudentsRepository):
    def __init__(self) -> None:
        self.db: dict = {}

    def add_student(self, student: Student):
        self.db[student.email] = student

    def get_student_by_email(self, email: EmailStr) -> Student:
        student = self.db.get(email)

        if not student:
            return None

        return student

    def get_student_by_handle(self, handle: str) -> Student:
        for student in self.db.values():
            if student.handle == handle:
                return student

        return None

    def get_all_students(self) -> list[Student]:
        return list(self.db.values())

    def update_student(self, email: EmailStr, new_student: Student) -> None:
        self.db[email] = new_student

    def delete_student(self, email: EmailStr) -> None:
        if not self.db.get(email):
            return

        self.db.pop(email)

    def email_exists(self, email: EmailStr) -> bool:
        return self.db.get(email) is not None

    def handle_exists(self, handle: str) -> bool:
        for student in self.db.values():
            if student["handle"] == handle:
                return True

        return False

    def update_student_by_email(self, email: EmailStr, new_student: Student) -> None:
        pass

    def update_student_by_handle(self, handle: str, new_student: Student) -> None:
        pass

    def student_exists(self, student: Student) -> bool:
        return self.email_exists(student.email) or self.handle_exists(student.handle)
