from __future__ import annotations
from dataclasses import dataclass

from .enums import CfContestType, CfPhase, CfProblemType, CfVerdict, CfTestset, CfParticipantType


@dataclass
class CfContest:
    id: int
    name: str
    type: CfContestType
    phase: CfPhase
    frozen: bool
    durationSeconds: int
    startTimeSeconds: int | None = None
    relativeTimeSeconds: int | None = None
    preparedBy: str | None = None
    websiteUrl: str | None = None
    description: str | None = None
    difficulty: int | None = None
    kind: str | None = None
    icpcRegion: str | None = None
    country: str | None = None
    city: str | None = None
    season: str | None = None


@dataclass
class CfProblem:
    index: str
    type: CfProblemType
    name: str
    tags: list[str]
    contestId: int | None = None
    problemsetName: str | None = None
    points: float | None = None
    rating: int | None = None


@dataclass
class CfRankListRow:
    party: CfParty
    rank: int
    points: float
    penalty: int
    successfulHackCount: int
    unsuccessfulHackCount: int
    problemResults: list[int]
    lastSubmissionTimeSeconds: int | None = None


@dataclass
class CfSubmission:
    id: int
    creationTimeSeconds: int
    relativeTimeSeconds: int
    problem: CfProblem
    author: CfParty
    programmingLanguage: str
    verdict: CfVerdict | None
    testset: CfTestset
    passedTestCount: int
    timeConsumedMillis: int
    memoryConsumedBytes: int
    points: float | None = None
    contestId: int | None = None


@dataclass
class CfParty:
    members: list[CfMember]
    ghost: bool
    participantType: CfParticipantType
    teamId: int | None = None
    teamName: str | None = None
    room: int | None = None
    contestId: int | None = None
    startTimeSeconds: int | None = None


@dataclass
class CfMember:
    handle: str
    name: str | None = None
