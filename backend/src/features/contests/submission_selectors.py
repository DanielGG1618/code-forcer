from typing import Annotated

from pydantic.functional_validators import AfterValidator

from src.features.contests.models import Submission, SubmissionSelector


def submission_name_validator(name: str) -> str:
    assert name in submission_selectors, "Invalid submission selector name"
    return name


SubmissionSelectorName = Annotated[str, AfterValidator(submission_name_validator)]

submission_selectors: dict[str, SubmissionSelector] = {}


def submission_selector(name: str):
    def decorator(selector: SubmissionSelector):
        submission_selectors[name] = selector
        return selector

    return decorator


@submission_selector("most passed test count")
def most_passed_test_count_selector(submissions: list[Submission]) -> Submission:
    return max(submissions, key=lambda s: (s.passed_test_count, s.submission_time_utc))


@submission_selector("latest")
def latest_submission_selector(submissions: list[Submission]) -> Submission:
    return max(submissions, key=lambda s: s.submission_time_utc)


@submission_selector("latest successful")  # returns latest unsuccessful submission if no successful submissions
def latest_successful_submission_selector(submissions: list[Submission]) -> Submission:
    return max(submissions, key=lambda s: (s.is_successful, s.submission_time_utc))


@submission_selector("most points")
def most_points_selector(submissions: list[Submission]) -> Submission:
    return max(
        submissions,
        key=lambda submission: (submission.points if submission.points is not None else 0,
                                submission.submission_time_utc)
    )


__all__ = ["submission_selectors", "SubmissionSelectorName"]
