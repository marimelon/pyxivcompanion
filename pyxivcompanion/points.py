import uuid
from typing import Literal

from pydantic import BaseModel

from .config import Config
from .request import CompanionRequest
from .response import CompanionErrorResponse
from .token import Token


class KupoNut(BaseModel):
    createdAt: int
    expiredAt: int


class MogCoin(BaseModel):
    free: int
    paid: int


class PointsStatus(BaseModel):
    updatedAt: int
    kupoNuts: list[KupoNut]
    mogCoins: MogCoin
    role: int


class MogCoinProduct(BaseModel):
    productId: str
    coinPaid: int
    coinFree: int
    sortOrder: int


class MogCoinProducts(BaseModel):
    products: list[MogCoinProduct]


class PointsHistoryEntity(BaseModel):
    typeName: str
    amount: int
    createdAt: int


class PointsHistory(BaseModel):
    updatedAt: int
    history: list[PointsHistoryEntity]


class Points:
    @staticmethod
    async def get_status(token: Token):
        """GET /points/status"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}points/status',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return PointsStatus(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_mogcoin_products(token: Token):
        """GET /points/products"""
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}points/products',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get()
        if res.status == 200:
            data = await res.json()
            return MogCoinProducts(**data), res
        else:
            raise await CompanionErrorResponse.select(res)

    @staticmethod
    async def get_points_history(type: Literal[1, 2, 3], token: Token):
        """
            GET /points/history

            type:
                1 Consume KupoNuts
                2 Recive MogCoins
                3 Consume MogCoins
        """
        req = CompanionRequest(url=f'{token.region}{Config.SIGHT_PATH}points/history',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=token.token)
        res = await req.get(params={'type': type})
        if res.status == 200:
            data = await res.json()
            return PointsHistory(**data), res
        else:
            raise await CompanionErrorResponse.select(res)
