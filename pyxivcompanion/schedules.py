import uuid

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class ScheduleCharacter(BaseModel):
    join: int
    role: str


class JoinStatus(BaseModel):
    yes: int
    no: int
    unanswered: int


class Schedule(BaseModel):
    updatedAt: int
    sid: str
    cid: str
    title: str
    startTime: int
    endTime: int
    category: int
    closed: bool
    canceled: bool
    rid: str
    comment: str
    modifiedAt: int
    character: ScheduleCharacter
    joinStatus: JoinStatus
    titleCensoredAt: int
    commentCensoredAt: int
    censoredAt: int
    deletedAt: int
    repetition: bool


class SchedulesModel(BaseModel):
    responseTime: int
    schedules: list[Schedule]


class ScheduleRepetitionRule(BaseModel):
    loop: int
    cycle: int
    week: list
    month: int
    timezone: str


class ScheduleRepetitionScheduleJoinInfo(BaseModel):
    join: int
    comment: str
    role: str


class ScheduleRepetitionSchedule(BaseModel):
    sid: str
    startTime: int
    endTime: int
    closed: bool
    canceled: bool
    joinInfo: ScheduleRepetitionScheduleJoinInfo


class ScheduleRepetition(BaseModel):
    parentSid: str
    rule: ScheduleRepetitionRule
    schedules: list[ScheduleRepetitionSchedule]


class MakeScheduleDetailCharacter(BaseModel):
    join: int
    role: str
    cid: str
    comment: str
    censoredAt: int


class MakeScheduleDetail(BaseModel):
    sid: str
    parentSid: str
    cid: str
    title: str
    startTime: int
    endTime: int
    category: int
    rid: str
    comment: str
    closed: bool
    canceled: bool
    modifiedAt: int
    pushStatus: bool
    characters: list[MakeScheduleDetailCharacter]
    titleCensoredAt: int
    commentCensoredAt: int
    censoredAt: int
    deletedAt: int


class ScheduleDetails(BaseModel):
    updatedAt: int
    schedule: MakeScheduleDetail
    repetition: list[ScheduleRepetition]


class Schedules:
    @staticmethod
    async def get_schedules(token: Token,
                            _from: int,
                            count: int,
                            startAt: int,
                            lastResponseTime: int,
                            to: int):
        """GET /schedules"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}schedules',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        params = {'from': _from, 'count': count, 'startAt': startAt, 'lastResponseTime': lastResponseTime, 'to': to}
        res = await req.get(params=params)
        if res.status == 200:
            data = await res.json()
            return SchedulesModel(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_schedule_details(sid: str, token: Token):
        """GET /schedules/{sid}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}schedules/{sid}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return ScheduleDetails(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def make_schedule(schedule: ScheduleDetails, token: Token):
        """POST /schedules/repetition"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}schedules/repetition',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.post(schedule.dict())
        if res.status == 200:
            data = await res.json()
            return ScheduleDetails(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
