from abc import ABC, abstractmethod

from src.features.contests.models import Contest


class IContestsProvider(ABC):
    @abstractmethod
    def get_contest(self, contest_id: int, api_key: str, api_secret: str) -> Contest:
        pass

    @abstractmethod
    def validate_handle(self, handle: str) -> bool:
        pass
