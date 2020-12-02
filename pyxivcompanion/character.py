import uuid
from typing import TYPE_CHECKING

import aiohttp

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse

if TYPE_CHECKING:
    from .token import Token


class CharacterWorldsResponse:
    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.loginStatusCode:int = data['loginStatusCode']
        self.getBagFlag:bool = data['getBagFlag']
        self.world:str = data['world']
        self.currentWorld:str = data['currentWorld']

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body,raw=response)


class Character:
    @staticmethod
    async def get_worlds(token: 'Token'):
        """GET /character/worlds"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}character/worlds',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            return await CharacterWorldsResponse.init(response=res)
        else:
            raise await CompanionErrorResponse.select(res)
