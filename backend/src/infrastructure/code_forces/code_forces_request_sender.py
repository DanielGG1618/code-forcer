from abc import ABC, abstractmethod
from random import randint
from hashlib import sha512
from time import time
from typing import Final

from requests import get, Response, JSONDecodeError
from starlette import status
from starlette.exceptions import HTTPException

from infrastructure.code_forces.enums import CfContestType, CfPhase, CfProblemType, CfParticipantType, CfVerdict, \
    CfTestset
from infrastructure.code_forces.models import CfContest, CfProblem, CfRankListRow, CfSubmission, CfParty, CfMember


class ICodeForcesRequestsSender(ABC):
    @abstractmethod
    def contest_standings(self, contest_id: int) -> tuple[CfContest, list[CfProblem], list[CfRankListRow]]:
        pass

    @abstractmethod
    def contest_status(self, contest_id: int) -> list[CfSubmission]:
        pass


class IAnonymousCodeForcesRequestsSender(ABC):
    @abstractmethod
    def validate_handle(self, handle: str):
        pass


class CodeForcesRequestsSender(ICodeForcesRequestsSender, IAnonymousCodeForcesRequestsSender):
    API_URL: Final[str] = 'https://codeforces.com/api/'

    key: str | None
    secret: str | None

    def __init__(self, key: str = None, secret: str = None):
        self.key = key
        self.secret = secret

    def contest_standings(self, contest_id: int) -> tuple[CfContest, list[CfProblem], list[CfRankListRow]]:
        response = self._send_request(method_name="contest.standings", contestId=contest_id, asManager=True)

        contest = get_contest_from_data(response['contest'])
        problems = [get_problems_from_data(problem_data) for problem_data in response['problems']]
        rows = [get_rank_list_row_from_data(row) for row in response['rows']]

        return contest, problems, rows

    def contest_status(self, contest_id: int) -> list[CfSubmission]:
        response = self._send_request(method_name="contest.status", contestId=contest_id, asManager=True)

        return [get_submission_from_data(submission_data) for submission_data in response]

    def validate_handle(self, handle: str):
        return self._send_anonymous_request(method_name="user.info", handles=handle, checkHistoricHandles=False)

    def _send_request(self, method_name: str, **params: int | str | bool):
        rand = randint(100_000, 999_999)
        hasher = sha512()

        params["time"] = int(time())
        params["apiKey"] = self.key

        params_str = '&'.join(sorted(f"{p[0]}={p[1]}" for p in params.items()))

        hasher.update(f"{rand}/{method_name}?{params_str}#{self.secret}".encode())
        api_sig = str(rand) + hasher.hexdigest()

        response = get(self.API_URL + method_name, params | {"apiSig": api_sig})

        return self._process_response(response)

    def _send_anonymous_request(self, method_name: str, **params: int | str | bool):
        response = get(self.API_URL + method_name, params=params)

        return self._process_response(response)

    @staticmethod
    def _process_response(response: Response):
        try:
            responseJson = response.json()
        except JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="CodeForces API does not respond"
            )

        if responseJson["status"] is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="CodeForces API does not respond"
            )

        if responseJson["status"] == "FAILED":
            raise HTTPException(
                status_code=response.status_code,
                detail=f"CodeForces API: {responseJson["comment"]}"
            )

        return responseJson["result"]


def get_contest_from_data(contest_data: dict) -> CfContest:
    contest_data['type'] = CfContestType[contest_data['type']]
    contest_data['phase'] = CfPhase[contest_data['phase']]

    return CfContest(**contest_data)


def get_problems_from_data(problem_data: dict) -> CfProblem:
    problem_data['type'] = CfProblemType[problem_data['type']]
    return CfProblem(**problem_data)


def get_rank_list_row_from_data(rank_list_row_data: dict) -> CfRankListRow:
    rank_list_row_data['party']['participantType'] = CfParticipantType[rank_list_row_data['party']['participantType']]

    rank_list_row_data['party'] = get_party_from_data(rank_list_row_data['party'])
    return CfRankListRow(**rank_list_row_data)


def get_submission_from_data(submission_data: dict) -> CfSubmission:
    submission_data['problem'] = get_problems_from_data(submission_data['problem'])
    submission_data['author'] = get_party_from_data(submission_data['author'])
    submission_data['verdict'] = CfVerdict[submission_data['verdict']]
    submission_data['testset'] = CfTestset[submission_data['testset']]

    return CfSubmission(**submission_data)


def get_party_from_data(party_data: dict) -> CfParty:
    party_data['members'] = [get_member_from_data(member_data) for member_data in party_data['members']]
    return CfParty(**party_data)


def get_member_from_data(member_data: dict) -> CfMember:
    return CfMember(**member_data)


__all__ = ["ICodeForcesRequestsSender", "IAnonymousCodeForcesRequestsSender", "CodeForcesRequestsSender"]
