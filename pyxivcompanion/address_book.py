import uuid

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class OnlineStatusResponse(BaseModel):
    characters: list[str]


class CharacterDetailsCharacterSkill(BaseModel):
    code: str
    level: int


class CharacterDetailsGC(BaseModel):
    gcid: int
    gcRank: int


class CharacterDetailsFCCrest(BaseModel):
    base: str
    frame: str
    symbol: str


class CharacterDetailsFC(BaseModel):
    name: str
    abbr: str
    crest: CharacterDetailsFCCrest


class CharacterDetailsCharacter(BaseModel):
    cid: str
    name: str
    world: str
    portrait: str
    skills: list[CharacterDetailsCharacterSkill]
    gc: CharacterDetailsGC
    fc: CharacterDetailsFC
    classJob: str
    jobStone: list[str]
    lodestonecid: str


class CharacterDetails(BaseModel):
    updatedAt: int
    character: CharacterDetailsCharacter


class AddressBook:
    @staticmethod
    async def get_online_states(token: Token):
        """GET /address-book/online-status"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/online-status',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return await OnlineStatusResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_character_details(cid: str, token: Token, updatedAt: int = 0):
        """GET /address-book/{cid}/profile?updatedAt={updatedAt}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/{cid}/profile',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get(params={'updatedAt': updatedAt})
        if res.status == 200:
            data = await res.json()
            return await CharacterDetails(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
