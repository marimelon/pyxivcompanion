import uuid
from typing import Optional

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class Matetia(BaseModel):
    key: int
    grade: str


class Gil(BaseModel):
    itemId: str
    stack: int
    catalogId: int


class Crystal(BaseModel):
    itemId: str
    stack: int
    catalogId: int
    eorzeadbItemId: str
    icon: str


class Item(BaseModel):
    itemId: str
    stack: int
    catalogId: int
    signatureName: str
    isCrafted: bool
    hq: int
    masterpiece: int
    durability: int
    refine: int
    materia: list[Matetia]
    stain: int
    pattern: int
    eorzeadbItemId: str
    icon: str


class Inventory(BaseModel):
    updatedAt: int
    bag: list[Item]
    gil: Gil
    crystal: list[Crystal]
    equipment: list[Item]


class RecycledItem(BaseModel):
    itemType: int
    dateLastModified: int
    sellPrice: str


class CharacterInventory(Inventory):
    armoryChest: list[Item]
    recycle: list[RecycledItem]
    chocoboBagFree: Optional[list[Item]]
    chocoboBagPaid: Optional[list[Item]]


class RetainerInventory(Inventory):
    soldPrice: int
    totalExhibitionPrice: int


class Items:
    @staticmethod
    async def get_character(token: Token):
        """GET /items/character"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}items/character',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return await CharacterInventory(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_retainer(retainer_id: str, token: Token):
        """GET /items/retainers/{retainer_id}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}items/retainers/{retainer_id}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return await RetainerInventory(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
