import uuid

from aiohttp import ClientResponse
from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class Matetia(BaseModel):
    key: int
    grade: str


class Entry(BaseModel):
    itemId: str
    stack: int
    catalogId: int
    signatureName: str
    isCrafted: bool
    hq: int
    stain: int
    materia: list[Matetia]
    materias: int
    sellPrice: int
    sellRetainerName: str
    registerTown: int


class MarketResponse(BaseModel):
    icon: str
    iconHq: str
    eorzeadbItemId: str
    entries: list[Entry]


class History(BaseModel):
    stack: int
    hq: int
    sellPrice: int
    buyCharacterName: str
    buyRealDate: int


class MarketHistoryResponse(BaseModel):
    icon: str
    iconHq: str
    eorzeadbItemId: str
    history: list[History]


class Market:
    @staticmethod
    async def get_market(itemid: int, token: Token) -> tuple[MarketResponse, ClientResponse]:
        """GET /market/items/catalog/{itemid}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}market/items/catalog/{itemid}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get(params={'worldName': token.world})
        if res.status == 200:
            data = await res.json()
            return MarketResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_history(itemid: int, token: Token) -> tuple[MarketHistoryResponse, ClientResponse]:
        """GET /market/items/history/catalog/{itemid}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}market/items/history/catalog/{itemid}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get(params={'worldName': token.world})

        if res.status == 200:
            data = await res.json()
            return await MarketHistoryResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def stop_retainer_market(retainer_id: str, token: Token):
        """DELETE /market/retainers/{retainer_id}"""
        pass

    @staticmethod
    async def start_retainer_market(retainer_id: str, token: Token):
        """POST /market/retainers/{retainer_id}"""
        pass

    @staticmethod
    async def get_retainer_market(retainer_id: str, token: Token):
        """GET /market/retainers/{retainer_id}"""
        pass
