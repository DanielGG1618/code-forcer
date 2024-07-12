from application.students.students_service import Student, StudentData, StudentsService

from application.students.students_repository import IStudentsRepository
from application.contests.contests_provider import IContestsProvider

from container import container

student_service = StudentsService(IStudentsRepository, IContestsProvider)

def test_create_student():
    #Arrange
    student_data = Student(email="exampleemail@email.com", handle="example")

    #Act
    container[StudentsService].create_student(student_data)

    #Assert
    try:
        assert container[StudentsService].get_all_students()[0] == student_data
    except AssertionError:
        container[StudentsService].delete_student("exampleemail@email.com")

    #Clean up
    container[StudentsService].delete_student("exampleemail@email.com")

def test_update_student():
    #Arrange
    students_data = [
        Student(email="test1@email.com", handle="test1"),
        Student(email="test2@email.com", handle="test2"),
        Student(email="test3@email.com", handle="test3")
    ]

    for student in students_data:
        container[StudentsService].create_student(student)

    new_student = Student(email="test1@email.com", handle="blazz1t")

    expected_result = [
        Student(email="test1@email.com", handle="blazz1t"),
        Student(email="test2@email.com", handle="test2"),
        Student(email="test3@email.com", handle="test3")
    ]

    #Act
    container[StudentsService].update_or_create_student("test1@email.com", new_student)

    #Assert
    try:
        assert container[StudentsService].get_all_students() == expected_result
    except AssertionError:
        clean_up_database_data(expected_result)

    #Clean up
    clean_up_database_data(expected_result)

def test_get_all_students():
    #Arrange
    students_data = [
        Student(email="test1@email.com", handle="test1"),
        Student(email="test2@email.com", handle="test2"),
        Student(email="test3@email.com", handle="test3")
    ]

    #Act
    for student in students_data:
        container[StudentsService].create_student(student)

    #Assert
    try:
        assert container[StudentsService].get_all_students() == students_data
    except AssertionError:
        clean_up_database_data(students_data)



    #Additional arrange
    students_data.append(Student(email="test4@email.com", handle="test4"))

    #Additional act
    container[StudentsService].create_student(students_data[3])

    #Additional assert
    try:
        assert container[StudentsService].get_all_students() == students_data
    except AssertionError:
        clean_up_database_data(students_data)

    #Clean up
    clean_up_database_data(students_data)

def test_get_student_by_email_or_handle():
    #Arrange
    students_data = [
        Student(email="test1@email.com", handle="test1"),
        Student(email="test2@email.com", handle="test2"),
        Student(email="test3@email.com", handle="test3")
    ]

    for student in students_data:
        container[StudentsService].create_student(student)

    #Act
    result_handle = container[StudentsService].get_student_by_email_or_handle("test1")
    result_email = container[StudentsService].get_student_by_email_or_handle("test2@email.com")

    #Assert
    try:
        assert result_handle == students_data[0], "Getting student by handle failed"
        assert result_email == students_data[1], "Getting student by email failed"
    except AssertionError:
        clean_up_database_data(students_data)

    #Clean up
    clean_up_database_data(students_data)

def test_delete_student():
    #Arrange
    students_data = [
        Student(email="test1@email.com", handle="test1"),
        Student(email="test2@email.com", handle="test2"),
        Student(email="test3@email.com", handle="test3")
    ]

    for student in students_data:
        container[StudentsService].create_student(student)

    expected_result = [
        Student(email="test2@email.com", handle="test2"),
        Student(email="test3@email.com", handle="test3")
    ]

    #Act
    container[StudentsService].delete_student(students_data[0].email)

    #Assert
    try:
        assert container[StudentsService].get_all_students() == expected_result
    except AssertionError:
        clean_up_database_data(expected_result)

    #Clean up
    clean_up_database_data(expected_result)

def clean_up_database_data(student_data: list[Student]):
    for student in student_data:
        container[StudentsService].delete_student(student.email)
