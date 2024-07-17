from src.features.contests.interfaces import IContestsProvider
from src.features.contests.models import Contest


class ContestsProviderMock(IContestsProvider):
    def __init__(self):
        self.contests: dict[int, Contest] = {}
        self.valid_handles = []

    def get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
        return self.contests[contest_id]

    def get_contest_results(self, contest_id: int, api_key: str, api_secret: str):
        pass

    def validate_handle(self, handle: str) -> bool:
        return handle in self.valid_handles
