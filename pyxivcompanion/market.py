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


class MarketFavoriteItem(BaseModel):
    catalogId: int
    eorzeadbItemId: str
    icon: str
    hq: int
    watchPrice: int
    matchCount: int
    exhibitionCount: int
    createdAt: int
    notification: bool


class MarketFavorites(BaseModel):
    updatedAt: int
    items: list[MarketFavoriteItem]


class MarketFavoritesNotificationSetting(BaseModel):
    marketItemCheckTimes: list[int]


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
            return MarketHistoryResponse(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_favorites(token: Token):
        """GET /market/favorites """
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}market/favorites',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get(params={'worldName': token.world})

        if res.status == 200:
            data = await res.json()
            return MarketFavorites(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_favorites_notification_setting(token: Token):
        """GET /market/favorites/notification-setting """
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}market/favorites/notification-setting',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return MarketFavoritesNotificationSetting(**data), res
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
