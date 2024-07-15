from fastapi import HTTPException, status
from pydantic import EmailStr

from src.features.students.model import Student
from src.features.students.interfaces import IStudentsRepository
from src.infrastructure.storage.db_context import DBContext


class DBStudentsRepository(IStudentsRepository):
    def __init__(self, db_name: str) -> None:
        self.db_context = DBContext(db_name)

    def email_exists(self, email: EmailStr) -> bool:
        return self.get_student_by_email(email.lower()) is not None

    def handle_exists(self, handle: str) -> bool:
        return self.get_student_by_handle(handle.lower()) is not None

    def student_exists(self, student: Student) -> bool:
        return self.email_exists(student.email) or self.handle_exists(student.handle)

    def add_student(self, student: Student) -> None:
        student = student.lower()

        if self.email_exists(student.email):
            print(f'Student with email {student.email} already exists')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Student with email {student.email} already exists'
            )

        if self.handle_exists(student.handle):
            print(f'Student with handle {student.handle} already exists')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Student with handle {student.handle} already exists'
            )

        self.db_context.execute_command(
            "INSERT INTO students(email, handle) VALUES (?, ?)",
            (student.email, student.handle, )
        )
        self.db_context.commit()

    def get_all_students(self) -> list[Student]:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students"
        ).fetchall()

        return [
            Student(email=email, handle=handle)
            for email, handle in result
        ]

    def get_student_by_email(self, email: EmailStr) -> Student | None:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE email = ?",
            (email.lower(), )
        ).fetchone()

        if not result:
            print(f"Student with email {email} not found")
            return None

        (email, handle) = result
        return Student(email=email, handle=handle)

    def get_student_by_handle(self, handle: str) -> Student | None:
        result = self.db_context.execute_command(
            "SELECT email, handle FROM students WHERE handle = ?",
            (handle.lower(), )
        ).fetchone()

        if not result:
            print(f"Student with handle {handle} not found")
            return None

        (email, handle) = result
        return Student(email=email, handle=handle)

    def update_student(self, email: EmailStr, new_student: Student) -> None:
        if not self.email_exists(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Student with given email is not found'
            )

        new_student = new_student.lower()
        self.db_context.execute_command(
            "UPDATE students SET email = ?, handle = ? WHERE email = ?",
            (new_student.email, new_student.handle, email.lower(), )
        )
        self.db_context.commit()

    def delete_student(self, email: EmailStr) -> None:
        if not self.email_exists(email):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Student with given email is not found'
            )

        self.db_context.execute_command(
            "DELETE FROM students WHERE email = ?",
            (email.lower(), )
        )
        self.db_context.commit()
