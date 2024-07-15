from fastapi import status, APIRouter

from src.container import container
from .interfaces import IContestsProvider

router = APIRouter()


@router.get("/contests/{contest_id}/results", status_code=status.HTTP_200_OK)
async def get_contest_results(contest_id: int, key: str, secret: str):
    return GetContestResultsQuery(
        container[IContestsProvider]
    ).handle(contest_id, key, secret)


class GetContestResultsQuery:
    contests_provider: IContestsProvider

    def __init__(self, contests_provider: IContestsProvider):
        self.contests_provider = contests_provider

    def handle(self, contest_id: int, key: str, secret: str):
        return self.contests_provider.get_contest_results(contest_id, key, secret)
