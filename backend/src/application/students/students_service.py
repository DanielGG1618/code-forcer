from validate_email import validate_email
from fastapi import HTTPException, status, UploadFile

from os import path, remove

from application.students.students_data_parsing import parse_students_data
from domain.student import Student
from application.students.students_repository import IStudentsRepository
from application.contests.contests_provider import IContestsProvider
from contracts.student_data import StudentData


class StudentsService:
    students_repository: IStudentsRepository
    contests_provider: IContestsProvider

    def __init__(self, students_repository: IStudentsRepository, contests_provider: IContestsProvider):
        self.students_repository = students_repository
        self.contests_provider = contests_provider

    def create_student(self, student_data: StudentData) -> Student:
        student = student_data_to_student(student_data)

        if not self.contests_provider.validate_handle(student.handle):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Handle does not belong to CodeForces user'
            )

        self.students_repository.add_student(student)

        return student

    def update_or_create_students_from_file(self, file: UploadFile) -> list[Student]:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        students_data = parse_students_data(file_location)

        if path.exists(file_location):
            remove(file_location)

        return filter(
            lambda student: student is not None, [
                self.update_or_create_student(student_data.email, student_data)
                for student_data
                in students_data
            ]
        )

    def get_all_students(self) -> list[Student]:
        return self.students_repository.get_all_students()

    def get_student_by_email_or_handle(self, email_or_handle: str) -> Student:
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

    def update_or_create_student(self, email: str, student_data: StudentData) -> Student | None:
        if email != student_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email from URL should match email from reqeust body"
            )

        if not self.students_repository.email_exists(email):
            return self.create_student(student_data)

        student = student_data_to_student(student_data)

        if not self.contests_provider.validate_handle(student.handle):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Handle does not belong to CodeForces user'
            )

        self.students_repository.update_student(email, student)

    def delete_student(self, email: str) -> None:
        self.students_repository.delete_student(email)


def student_data_to_student(student_data: StudentData) -> Student:
    email = student_data.email
    handle = student_data.handle

    return Student(email=email, handle=handle)
