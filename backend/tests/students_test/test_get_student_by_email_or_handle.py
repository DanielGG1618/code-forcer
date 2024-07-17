from fastapi import status

from tests.create_test_client import client


def test_gets_student_by_email_if_email_is_valid_and_exists(existing_email, students_repo_mock):
    response = client.get(f"/students/{existing_email}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == students_repo_mock.get_student_by_email(existing_email).model_dump()


def test_returns_404_not_found_if_email_is_valid_but_does_not_exist(email):
    response = client.get(f"/students/{email}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_gets_student_by_handle_if_handle_is_valid_and_exists(existing_handle, students_repo_mock):
    response = client.get(f"/students/{existing_handle}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == students_repo_mock.get_student_by_handle(existing_handle).model_dump()


def test_returns_404_not_found_if_handle_is_valid_but_does_not_exist(handle):
    response = client.get(f"/students/{handle}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
