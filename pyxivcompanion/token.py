import uuid

from .account import Account, LoginObj
from .character import Character
from .config import Config
from .login import Login
from .request import CompanionRequest
from .response import SightResponseError, SightResponseLoginCharacter


class Token:
    def __init__(self, login: LoginObj, region: str, cid: str, character_name: str, world: str):
        self.login = login
        self.region = region
        self.cid = cid
        self.character_name = character_name
        self.world = world

    @staticmethod
    async def get_character_info(token: str, region: str) -> SightResponseLoginCharacter:
        req = CompanionRequest(url=f'{region}{Config.SIGHT_PATH}login/character',
                               RequestID=str(uuid.uuid1()).upper(),
                               Token=token)
        res = await req.get()
        if not res.status == 200:
            raise SightResponseError(res)

        data = await res.json()
        return SightResponseLoginCharacter(**data)

    async def refresh(self, sqex_id: str = None, sqex_pass: str = None, otp: str = None):
        res_data = await Account.request_token(self.login.userId)
        if res_data.region == "":
            if sqex_id is None or sqex_pass is None:
                Exception('sqex_id and sqex_password required.')
            login = await Account.login(sqex_id=sqex_id, sqex_pass=sqex_pass, otp=otp,
                                        userId=self.login.userId,
                                        token=res_data.token, salt=res_data.salt)
            region = await login.get_region(self.cid)
            character_info = await self.get_character_info(login.token, region)
        else:
            self.login.token = res_data.token

        # /login/character
        await Login.get_character(token=self)

        # /character/worlds
        await Character.get_worlds(token=self)

    @classmethod
    async def create_new_token(cls, cid: str, sqex_id: str, sqex_pass: str, otp: str = None):
        login = await Account.login(sqex_id, sqex_pass, otp)
        return await cls.create_new_token_from_loginobj(cid=cid, login=login)

    @classmethod
    async def create_new_token_from_loginobj(cls, cid: str, login: LoginObj):
        region = await login.get_region(cid)
        character_info = await cls.get_character_info(login.token, region)

        # /login/character
        await login.login_character()

        # /character/login-status
        await login.character_login_status()

        return cls(login=login, region=region, cid=cid,
                   character_name=character_info.character.name,
                   world=character_info.character.world)

    def to_dict(self):
        return {'userId': self.login.userId,
                'token': self.login.token,
                'salt': self.login.salt,
                'region': self.region,
                'cid': self.cid,
                'character_name': self.character_name,
                'world': self.world}

    @classmethod
    def from_dict(cls, dic: dict):
        return cls(login=LoginObj(userId=dic['userId'], token=dic['token'], salt=dic['salt']),
                   region=dic['region'],
                   cid=dic['cid'],
                   character_name=dic['character_name'],
                   world=dic['world'])
