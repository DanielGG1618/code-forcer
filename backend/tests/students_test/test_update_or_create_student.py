from fastapi import status

from src.features.students.model import Student
from tests.create_test_client import client


def test_creates_student_if_not_exists_and_data_is_valid(email, handle, contests_provider_mock, students_repo_mock):
    contests_provider_mock.valid_handles = [handle]

    request_data = {
        "email": email,
        "handle": handle
    }

    response = client.put(f"/students/{email}", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert students_repo_mock.get_student_by_email(email).model_dump() == request_data


def test_returns_400_bad_request_if_handle_is_invalid(email, invalid_handle):
    request_data = {
        "email": email,
        "handle": invalid_handle
    }

    response = client.put(f"/students/{email}", json=request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_updates_student_if_data_is_valid_and_student_exists(email, handle, students_repo_mock):
    request_data = {
        "email": email,
        "handle": handle
    }

    students_repo_mock.add_student(Student(email=email, handle=handle))

    response = client.put(f"/students/{email}", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert students_repo_mock.get_student_by_email(email).model_dump() == request_data


def test_creates_new_student_if_data_is_valid_and_student_does_not_exist(email, handle, students_repo_mock):
    request_data = {
        "email": email,
        "handle": handle
    }

    response = client.put(f"/students/{email}", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert students_repo_mock.get_student_by_email(email).model_dump() == request_data


def test_returns_422_unprocessable_entity_if_email_is_invalid(invalid_email, handle, contests_provider_mock):
    contests_provider_mock.valid_handles = [handle]

    request_data = {
        "email": invalid_email,
        "handle": handle
    }

    response = client.put(f"/students/{invalid_email}", json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
