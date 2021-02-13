import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse

if TYPE_CHECKING:
    from .token import Token


class CharacterWorldsResponse(BaseModel):
    loginStatusCode: int
    getBagFlag: bool
    world: str
    currentWorld: str


class Character:
    @staticmethod
    async def get_worlds(token: 'Token'):
        """GET /character/worlds"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}character/worlds',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return CharacterWorldsResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
