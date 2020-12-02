import uuid

import aiohttp

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class OnlineStatusResponse:
    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.characters: list[str] = data['characters']

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class AddressBook:
    @staticmethod
    async def get_online_states(token: Token):
        """GET /address-book/online-status"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/online-status',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            return await OnlineStatusResponse.init(res)
        else:
            raise await CompanionErrorResponse.select(res)
