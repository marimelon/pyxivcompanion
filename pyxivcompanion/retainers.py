import uuid
import aiohttp

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class RetainersResponse:
    class Retainer:
        def __init__(self, data: dict):
            self.createUnixTime: int = data['createUnixTime']
            self.status: int = data['status']
            self.retainerId: str = data['retainerId']
            self.retainerName: str = data['retainerName']
            self.isRenamed: bool = data['isRenamed']

    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.updatedAt: int = data['updatedAt']
        self.retainer: list[self.Retainer] = [self.Retainer(d) for d in data['retainer']]

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class Retainers:
    @staticmethod
    async def get_retainers(token: Token):
        """/retainers"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}retainers',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            return await RetainersResponse.init(response=res)
        else:
            raise await CompanionErrorResponse.select(res)
