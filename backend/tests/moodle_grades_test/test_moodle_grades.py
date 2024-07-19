from datetime import datetime, timedelta

from fastapi import status

from tests.create_test_client import client

from src.features.moodle_grades.models import (
    MoodleResultsData,
    ContestData,
    ProblemData,
    SubmissionData,
    LateSubmissionPolicyData
)


def test_get_moodle_grades_if_data_is_valid():
    moodle_result_data = MoodleResultsData(
        contest=ContestData(
            id=1,
            name='test contest',
            start_time_utc=datetime.now(),
            duration=timedelta(days=3),
            problems=[
                ProblemData(
                    name='test problem 1',
                    index='A',
                    max_points=50,
                    max_grade=100,
                    submissions=[
                        SubmissionData(
                            id=1,
                            author_email='a@a.a',
                            is_successful=False,
                            passed_test_count=5,
                            points=20,
                            programming_language='Python',
                            submission_time_utc=datetime.now(),
                        ),
                        SubmissionData(
                            id=3,
                            author_email='b@b.b',
                            is_successful=False,
                            passed_test_count=8,
                            points=30,
                            programming_language='Java',
                            submission_time_utc=datetime.now() + timedelta(hours=2),
                        ),
                        SubmissionData(
                            id=5,
                            author_email='c@c.c',
                            is_successful=True,
                            passed_test_count=10,
                            points=50,
                            programming_language='C++',
                            submission_time_utc=datetime.now() + timedelta(hours=3),
                        )
                    ]
                ),
                ProblemData(
                    name='test problem 2',
                    index='B',
                    max_points=30,
                    max_grade=60,
                    submissions=[
                        SubmissionData(
                            id=5,
                            author_email='c@c.c',
                            is_successful=True,
                            passed_test_count=52,
                            points=30,
                            programming_language='C++',
                            submission_time_utc=datetime.now() + timedelta(days=5),
                        ),
                        SubmissionData(
                            id=5,
                            author_email='a@a.a',
                            is_successful=False,
                            passed_test_count=32,
                            points=18,
                            programming_language='Python',
                            submission_time_utc=datetime.now() + timedelta(days=1),
                        )
                    ]
                )
            ],
        ),
        legal_excuses={},
        late_submission_policy=LateSubmissionPolicyData(
            penalty=0.2,
            extra_time=259200
        )
    )

    expected_output = 'Email,test contest Grade,test contest Feedback\r\na@a.a,76.0,\r\nb@b.b,60.0,\r\nc@c.c,148.0,\r\n'

    response = client.post("/moodle_grades", data=moodle_result_data.model_dump_json())

    assert response.status_code == status.HTTP_200_OK
    assert response.text == expected_output
