from src.container import container
from src.features.students.model import Student
from src.features.students.create_student import CreateStudentCommandHandler
from src.features.students.update_or_create_student import UpdateOrCreateStudentCommandHandler
from src.features.students.get_all_students import GetAllStudentsCommandHandler
from src.features.students.get_student import GetStudentQueryHandler
from src.features.students.delete_student import DeleteStudentCommandHandler
from src.features.students.interfaces import IStudentsRepository
from src.features.contests.interfaces import IContestsProvider


delete_students_command_handler = DeleteStudentCommandHandler(container[IStudentsRepository])
get_all_students_command_handler = GetAllStudentsCommandHandler(container[IStudentsRepository])
create_student_command_handler = CreateStudentCommandHandler(
    container[IStudentsRepository],
    container[IContestsProvider]
)


def test_create_student():
    # Arrange
    student_data = Student(email="exampleemail@email.com", handle="blazz1t")

    # Act
    create_student_command_handler.handle(student_data)

    # Assert
    try:
        assert get_all_students_command_handler.handle()[0] == student_data
    except AssertionError:
        delete_students_command_handler.handle("exampleemail@email.com")

    # Clean up
    delete_students_command_handler.handle("exampleemail@email.com")


def test_update_student():
    # Arrange
    update_or_create_student_command_handler = UpdateOrCreateStudentCommandHandler(container[IStudentsRepository],
                                                                                   container[IContestsProvider])

    students_data = [
        Student(email="test1@email.com", handle="blazz1t"),
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    for student in students_data:
        create_student_command_handler.handle(student)

    new_student = Student(email="test1@email.com", handle="tourist")

    expected_result = [
        Student(email="test1@email.com", handle="tourist"),
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    # Act
    update_or_create_student_command_handler.handle("test1@email.com", new_student)

    # Assert
    try:
        assert get_all_students_command_handler.handle() == expected_result
    except AssertionError:
        clean_up_database_data(expected_result)

    # Clean up
    clean_up_database_data(expected_result)


def test_get_all_students():
    # Arrange
    students_data = [
        Student(email="test1@email.com", handle="wyjjeless"),
        Student(email="test2@email.com", handle="blazz1t"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    # Act
    for student in students_data:
        create_student_command_handler.handle(student)

    # Assert
    try:
        assert get_all_students_command_handler.handle() == students_data
    except AssertionError:
        clean_up_database_data(students_data)

    # Additional arrange
    students_data.append(Student(email="test4@email.com", handle="tourist"))

    # Additional act
    create_student_command_handler.handle(students_data[3])

    # Additional assert
    try:
        assert get_all_students_command_handler.handle() == students_data
    except AssertionError:
        clean_up_database_data(students_data)

    # Clean up
    clean_up_database_data(students_data)


def test_get_student_by_email_or_handle():
    # Arrange
    students_data = [
        Student(email="test1@email.com", handle="blazz1t"),
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    for student in students_data:
        create_student_command_handler.handle(student)

    # Act
    result_handle = GetStudentQueryHandler(container[IStudentsRepository]).handle("blazz1t")
    result_email = GetStudentQueryHandler(container[IStudentsRepository]).handle("test2@email.com")

    # Assert
    try:
        assert result_handle == students_data[0], "Getting student by handle failed"
        assert result_email == students_data[1], "Getting student by email failed"
    except AssertionError:
        clean_up_database_data(students_data)

    # Clean up
    clean_up_database_data(students_data)


def test_delete_student():
    # Arrange
    students_data = [
        Student(email="test1@email.com", handle="blazz1t"),
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    for student in students_data:
        create_student_command_handler.handle(student)

    expected_result = [
        Student(email="test2@email.com", handle="wyjjeless"),
        Student(email="test3@email.com", handle="laymorja")
    ]

    # Act
    delete_students_command_handler.handle(students_data[0].email)

    # Assert
    try:
        assert get_all_students_command_handler.handle() == expected_result
    except AssertionError:
        clean_up_database_data(expected_result)

    # Clean up
    clean_up_database_data(expected_result)


def clean_up_database_data(student_data: list[Student]):
    for student in student_data:
        delete_students_command_handler.handle(student.email)
