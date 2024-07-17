from fastapi import status

from tests.create_test_client import client


def test_deletes_student_by_email_if_email_is_valid_and_exists(existing_email, students_repo_mock):
    response = client.delete(f"/students/{existing_email}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert students_repo_mock.get_student_by_email(existing_email) is None


def test_returns_422_unprocessable_entity_if_email_is_invalid(invalid_email):
    response = client.delete(f"/students/{invalid_email}")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_returns_404_not_found_if_email_is_valid_but_does_not_exist(email):
    response = client.delete(f"/students/{email}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
