from random import randint
from hashlib import sha512
from time import time
from typing import Final

from requests import get

from infrastructure.code_forces.enums import CfContestType, CfPhase, CfProblemType, CfParticipantType, CfVerdict, \
    CfTestset
from infrastructure.code_forces.models import CfContest, CfProblem, CfRankListRow, CfSubmission, CfParty, CfMember


class CodeForcesRequestSender:
    API_URL: Final[str] = 'https://codeforces.com/api/'

    key: str
    secret: str

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret

    def contest_standings(self, contest_id: int) -> tuple[CfContest, list[CfProblem], list[CfRankListRow]]:
        response = self.__send_request(method_name="contest.standings", contestId=contest_id, asManager=True)

        contest = get_contest_from_data(response['contest'])
        problems = [get_problems_from_data(problem_data) for problem_data in response['problems']]
        rows = [get_rank_list_row_from_data(row) for row in response['rows']]

        return contest, problems, rows

    def contest_status(self, contest_id: int) -> list[CfSubmission]:
        response = self.__send_request(method_name="contest.status", contestId=contest_id, asManager=True)

        return [get_submission_from_data(submission_data) for submission_data in response]

    def validate_handle(self, handle: str):
        return self.__send_anonymous_request(method_name="user.info", handles=handle, checkHistoricHandles=False)

    def __send_request(self, method_name: str, **params: int | str | bool):
        rand = randint(100_000, 1_000_000 - 1)
        hasher = sha512()

        params["time"] = int(time()) + 7200
        params["apiKey"] = self.key

        params_str = '&'.join(sorted(f"{p[0]}={p[1]}" for p in params.items()))

        hasher.update(f"{rand}/{method_name}?{params_str}#{self.secret}".encode())
        api_sig = str(rand) + hasher.hexdigest()

        resp = get(self.API_URL + method_name, params | {"apiSig": api_sig})

        if resp.status_code != 200:
            return None

        return resp.json()["result"]

    def __send_anonymous_request(self, method_name: str, **params: int | str | bool):
        resp = get(self.API_URL + method_name, params=params)

        if resp.status_code != 200:
            return None

        return resp.json()["result"]


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


__all = ["CodeForcesRequestSender"]
