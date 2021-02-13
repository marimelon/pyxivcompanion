import uuid

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class Retainer(BaseModel):
    createUnixTime: int
    status: int
    retainerId: str
    retainerName: str
    isRenamed: bool


class RetainersResponse(BaseModel):
    updatedAt: int
    retainer: list[Retainer]


class Retainers:
    @staticmethod
    async def get_retainers(token: Token):
        """/retainers"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}retainers',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return await RetainersResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
