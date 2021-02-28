import uuid
from typing import Optional

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


class AddressBookMemberList(BaseModel):
    members: list[str]


class AddressBookCharacter(BaseModel):
    cid: str
    name: str
    world: str
    portrait: str
    isSightUser: bool
    isVisibleOnlineStatus: bool


class AddressBookGroup(BaseModel):
    name: Optional[str]
    characters: list[AddressBookCharacter]


class AddressBookModel(BaseModel):
    fr: list[AddressBookGroup]
    ls: list[AddressBookGroup]
    cwls: list[AddressBookGroup]
    fc: list[AddressBookGroup]
    etc: list[AddressBookGroup]
    blackList: list[AddressBookGroup]
    blockList: list[AddressBookGroup]
    favoriteList: list[AddressBookGroup]


class AddressBookWrapper(BaseModel):
    updatedAt: int
    addressBook: AddressBookModel


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
    async def get_addressbook(token: Token):
        """GET /address-book"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return await AddressBookWrapper(**data), res
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

    @staticmethod
    async def add_favorite_list(add_list: AddressBookMemberList, token: Token):
        """POST /address-book/favoritelist"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/favoritelist',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.post(add_list.dict())
        if res.status == 200:
            data = await res.json()
            return await AddressBookMemberList(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def delete_favorite_list(del_list: AddressBookMemberList, token: Token):
        """DELETE /address-book/favoritelist"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/favoritelist',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.delete(del_list.dict())
        if res.status == 200:
            data = await res.json()
            return await AddressBookMemberList(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def add_block_list(add_list: AddressBookMemberList, token: Token):
        """POST /address-book/blocklist"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/blocklist',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.post(add_list.dict())
        if res.status == 200:
            data = await res.json()
            return await AddressBookMemberList(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def delete_block_list(del_list: AddressBookMemberList, token: Token):
        """DELETE /address-book/blocklist"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}address-book/blocklist',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.delete(del_list.dict())
        if res.status == 200:
            data = await res.json()
            return await AddressBookMemberList(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
