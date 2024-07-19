from fastapi import APIRouter
from pydantic import EmailStr
from starlette import status

from src.container import container
from src.features.students.interfaces import IStudentsRepository
from .submission_selectors import submission_selectors, SubmissionSelectorName
from .interfaces import IContestsProvider
from .models import Contest

router = APIRouter()


@router.get("/contests/{contest_id}", status_code=status.HTTP_200_OK)
async def get_contest(
        contest_id: int,
        key: str, secret: str,
        submission_selector_name: SubmissionSelectorName = 'latest'
) -> Contest:
    return GetContestQuery(
        container[IContestsProvider],
        container[IStudentsRepository]
    ).handle(contest_id, key, secret, submission_selector_name)


class GetContestQuery:
    contests_provider: IContestsProvider
    students_repository: IStudentsRepository

    def __init__(self, contests_provider: IContestsProvider, students_repository: IStudentsRepository):
        self.contests_provider = contests_provider
        self.students_repository = students_repository

    def handle(self, contest_id: int, api_key: str, api_secret: str, submission_selector_name: str) -> Contest:
        contest = self.contests_provider.get_contest(contest_id, api_key, api_secret)

        contest.select_single_submission_for_each_participant(selector=submission_selectors[submission_selector_name])
        contest.map_handles_to_emails(handle_to_email_mapper=self._get_email_by_handle)

        return contest

    def _get_email_by_handle(self, handle) -> EmailStr | None:
        student = self.students_repository.get_student_by_handle(handle)
        return student.email if student is not None else None
