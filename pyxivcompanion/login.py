import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse

if TYPE_CHECKING:
    from .token import Token


class Domains(BaseModel):
    lodestone: str
    cdn1: str
    cdn2: str
    appWeb: str


class Character(BaseModel):
    cid: str
    name: str
    world: str
    portrait: str
    lodestonecid: str


class LoginCharacterResponse(BaseModel):
    updatedAt: int
    domains: Domains
    role: str
    character: Character


class Login:
    @ staticmethod
    async def get_character(token: 'Token'):
        """GET /login/character"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}login/character',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return LoginCharacterResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
