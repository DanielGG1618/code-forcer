from src.container import container
from src.features.students.model import Student
from src.features.students.create_student import CreateStudentCommandHandler
from src.features.students.update_or_create_student import UpdateOrCreateStudentCommandHandler
from src.features.students.get_all_students import GetAllStudentsCommandHandler
from src.features.students.get_student import GetStudentQueryHandler
from src.features.students.delete_student import DeleteStudentCommandHandler
from src.features.students.interfaces import IStudentsRepository
from src.features.contests.interfaces import IContestsProvider


def test_create_student(email, handle):
    # Arrange
    student_data = Student(email=email, handle=handle)

    # Act
    CreateStudentCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(student_data)

    # Assert
    assert GetStudentQueryHandler(container[IStudentsRepository]).handle(email) == student_data


def test_update_student(email, handle):
    # Arrange
    new_student = Student(email=email, handle=handle)

    # Act
    UpdateOrCreateStudentCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(email, new_student)

    # Assert
    assert GetStudentQueryHandler(container[IStudentsRepository]).handle(email) == new_student


def test_get_all_students(contests_provider_mock):
    # Arrange
    students_data = [
        Student(email="test1@email.com", handle="wyjjeless"),
        Student(email="test2@email.com", handle="blazz1t"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    # Act
    for student in students_data:
        contests_provider_mock.valid_handles.append(student.handle)

        CreateStudentCommandHandler(
            container[IStudentsRepository],
            container[IContestsProvider]
        ).handle(student)

    # Assert
    for student in students_data:
        assert GetStudentQueryHandler(container[IStudentsRepository]).handle(student.email) == student

    # Additional arrange
    contests_provider_mock.valid_handles.append("tourist")
    students_data.append(Student(email="test4@email.com", handle="tourist"))

    # Additional act
    CreateStudentCommandHandler(
        container[IStudentsRepository],
        container[IContestsProvider]
    ).handle(students_data[-1])

    # Additional assert
    for student in students_data:
        assert GetStudentQueryHandler(container[IStudentsRepository]).handle(student.email) == student


def test_get_student_by_email_or_handle(students_repo_mock):
    # Arrange
    students_data = [
        Student(email="test1@email.com", handle="blazz1t"),
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    for student in students_data:
        students_repo_mock.db[student.email] = student

    # Act
    result_handle = GetStudentQueryHandler(container[IStudentsRepository]).handle("blazz1t")
    result_email = GetStudentQueryHandler(container[IStudentsRepository]).handle("test2@email.com")

    # Assert
    assert result_handle == students_data[0], "Getting student by handle failed"
    assert result_email == students_data[1], "Getting student by email failed"


def test_delete_student(students_repo_mock):
    # Arrange
    students_data = [
        Student(email="test1@email.com", handle="blazz1t"),
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    for student in students_data:
        students_repo_mock.db[student.email] = student

    expected_result = [
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    # Act
    DeleteStudentCommandHandler(container[IStudentsRepository]).handle(students_data[0].email)

    assert GetAllStudentsCommandHandler(container[IStudentsRepository]).handle() == expected_result
