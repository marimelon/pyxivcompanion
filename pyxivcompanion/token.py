import uuid

from pydantic import BaseModel

from .account import Account, LoginObj
from .character import Character
from .config import Config
from .login import Login
from .request import CompanionRequest
from .response import SightResponseError, SightResponseLoginCharacter


class Token(BaseModel):
    userId: str
    token: str
    salt: str
    region: str
    cid: str
    character_name: str
    world: str

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
        res_data = await Account.request_token(self.userId)
        if res_data.region == "":
            if sqex_id is None or sqex_pass is None:
                Exception('sqex_id and sqex_password required.')
            login = await Account.login(sqex_id=sqex_id, sqex_pass=sqex_pass, otp=otp,
                                        userId=self.userId,
                                        token=res_data.token, salt=res_data.salt)
            region = await login.get_region(self.cid)
            character_info = await self.get_character_info(login.token, region)
        else:
            self.token = res_data.token

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

        return cls(userId=login.userId,
                   token=login.token,
                   salt=login.salt,
                   region=region,
                   cid=cid,
                   character_name=character_info.character.name,
                   world=character_info.character.world)
