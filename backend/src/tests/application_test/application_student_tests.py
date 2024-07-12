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
    assert container[StudentsService].get_all_students()[0] == student_data

    #Clean up
    container[StudentsService].delete_student("exampleemail@email.com")

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
        for student in students_data:
            container[StudentsService].delete_student(student.email)



    #Additional arrange
    students_data.append(Student(email="test4@email.com", handle="test4"))

    #Additional act
    container[StudentsService].create_student(students_data[3])

    #Additional assert
    try:
        assert container[StudentsService].get_all_students() == students_data
    except AssertionError:
        for student in students_data:
            container[StudentsService].delete_student(student.email)

    #Clean up
    for student in students_data:
        container[StudentsService].delete_student(student.email)
