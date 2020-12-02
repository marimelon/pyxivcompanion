import uuid

import aiohttp
from typing import Optional

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class Inventory:
    class Item:
        class Matetia:
            def __init__(self, data: dict):
                self.key: int = data['key']
                self.grade: str = data['grade']

        def __init__(self, data: dict):
            self.itemId: str = data['itemId']
            self.stack: int = data['stack']
            self.catalogId: int = data['catalogId']
            self.signatureName: str = data['signatureName']
            self.isCrafted: bool = data['isCrafted']
            self.hq: int = data['hq']
            self.masterpiece: int = data['masterpiece']
            self.durability: int = data['durability']
            self.refine: int = data['refine']
            self.materia: list = [Inventory.Item.Matetia(v) for v in data['materia']]
            self.stain: int = data['stain']
            self.pattern: int = data['pattern']
            self.eorzeadbItemId: str = data['eorzeadbItemId']
            self.icon: str = data['icon']

    class Gil:
        def __init__(self, data: dict):
            self.itemId: str = data['itemId']
            self.stack: int = data['stack']
            self.catalogId: int = data['catalogId']

    class Crystal:
        def __init__(self, data: dict):
            self.itemId: str = data['itemId']
            self.stack: int = data['stack']
            self.catalogId: int = data['catalogId']
            self.eorzeadbItemId: str = data['eorzeadbItemId']
            self.icon: str = data['icon']

    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        self.raw = raw
        self.updatedAt: int = data['updatedAt']
        self.bag: list[self.Item] = [self.Item(d) for d in data['bag']]
        self.gil: self.Gil = self.Gil(data['gil'])
        self.crystal: list[self.Crystal] = [self.Crystal(d) for d in data['crystal']]
        self.equipment: list[self.Item] = [self.Item(d) for d in data['equipment']]


class CharacterInventory(Inventory):
    class RecycledItem(Inventory.Item):
        def __init__(self, data: dict):
            super().__init__(data)
            self.itemType: int = data['itemType']
            self.dateLastModified: int = data['dateLastModified']
            self.sellPrice: str = data['sellPrice']

    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        super().__init__(data, raw=raw)
        self.armoryChest: list[Inventory.Item] = [self.Item(d) for d in data['armoryChest']]
        self.recycle: list[self.RecycledItem] = [self.RecycledItem(d) for d in data['recycle']]
        self.chocoboBagFree: Optional[list[Inventory.Item]] = [self.Item(d) for d in data['chocoboBagFree']] if 'chocoboBagFree' in data else None
        self.chocoboBagPaid: Optional[list[Inventory.Item]] = [self.Item(d) for d in data['chocoboBagPaid']] if 'chocoboBagPaid' in data else None

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class RetainerInventory(Inventory):
    def __init__(self, data: dict, *, raw: aiohttp.ClientResponse = None):
        super().__init__(data, raw=raw)
        self.soldPrice: int = data['soldPrice']
        self.totalExhibitionPrice: int = data['totalExhibitionPrice']

    @classmethod
    async def init(cls, response: aiohttp.ClientResponse):
        body = await response.json()
        return cls(body, raw=response)


class Items:
    @staticmethod
    async def get_character(token: Token):
        """GET /items/character"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}items/character',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            return await CharacterInventory.init(res)
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_retainer(retainer_id: str, token: Token):
        """GET /items/retainers/{retainer_id}"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}items/retainers/{retainer_id}',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.login.token)
        res = await req.get()
        if res.status == 200:
            return await RetainerInventory.init(res)
        else:
            raise await CompanionErrorResponse.select(res)
