import uuid
from typing import TYPE_CHECKING

import aiohttp

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse

if TYPE_CHECKING:
    from .token import Token


class LoginCharacterResponse:
    class Domains:
        def __init__(self, lodestone: str, cdn1: str, cdn2: str, appWeb: str):
            self.lodestone = lodestone
            self.cdn1 = cdn1
            self.cdn2 = cdn2
            self.appWeb = appWeb

    class Character:
        def __init__(self, cid: str, name: str, world: str, portrait: str, lodestonecid: str):
            self.cid = cid
            self.name = name
            self.world = world
            self.portrait = portrait
            self.lodestonecid = lodestonecid

    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.updatedAt: int = data['updatedAt']
        self.domains: self.Domains = self.Domains(lodestone=data['domains']['lodestone'], cdn1=data['domains']['cdn1'],
                                                  cdn2=data['domains']['cdn2'], appWeb=data['domains']['appWeb'])
        self.role: str = data['role']
        self.character: self.Character = self.Character(cid=data['character']['cid'], name=data['character']['name'],
                                                        world=data['character']['world'], portrait=data['character']['portrait'],
                                                        lodestonecid=data['character']['lodestonecid'])

    @ classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class Login:
    @ staticmethod
    async def get_character(token: 'Token'):
        """GET /login/character"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}login/character',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            return await LoginCharacterResponse.init(response=res)
        else:
            raise await CompanionErrorResponse.select(res)
