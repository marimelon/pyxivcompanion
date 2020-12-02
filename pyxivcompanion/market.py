import datetime
import uuid

import aiohttp

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token
from .utility import http_date_to_datetime


class MarketResponse:
    class Entry:
        class Matetia:
            def __init__(self, data: dict):
                self.key: int = data['key']
                self.grade: str = data['grade']

        def __init__(self, data: dict):
            self.itemid: str = data['itemId']
            self.stack: int = data['stack']
            self.catalogId: int = data['catalogId']
            self.signatureName: str = data['signatureName']
            self.isCrafted: bool = data['isCrafted']
            self.hq: int = data['hq']
            self.stain: int = data['stain']
            self.materia: list[MarketResponse.Entry.Matetia] = [MarketResponse.Entry.Materia(d) for d in data['materia']]
            self.materias: int = data['materias']
            self.sellPrice: str = data['sellPrice']
            self.sellRetainerName: str = data['sellRetainerName']
            self.registerTown: int = data['registerTown']

    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.icon: str = data['icon']
        self.iconHq: str = data['iconHq']
        self.eorzeadbItemId: str = data['eorzeadbItemId']
        self.entries: list[self.Entry] = [self.Entry(d) for d in data['entries']]

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class MarketHistoryResponse:
    class History:
        def __init__(self, data: dict):
            self.stack: int = data['stack']
            self.isHQ: int = data['hq']
            self.sellPrice: str = data['sellPrice']
            self.buyCharacterName: str = data['buyCharacterName']
            self.buyRealDate = data['buyRealDate']

    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.icon: str = data['icon']
        self.iconHq: str = data['iconHq']
        self.eorzeadbItemId: str = data['eorzeadbItemId']
        self.history: list[self.History] = [self.History(d) for d in data['history']]

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class Market:
    @staticmethod
    async def get_market(itemid: int, token: Token):
        """GET /market/items/catalog/{itemid}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}market/items/catalog/{itemid}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get(params={'worldName': token.world})
        if res.status == 200:
            return await MarketResponse.init(res), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_history(itemid: int, token: Token):
        """GET /market/items/history/catalog/{itemid}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}market/items/history/catalog/{itemid}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get(params={'worldName': token.world})

        if res.status == 200:
            return await MarketHistoryResponse.init(res), res
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
