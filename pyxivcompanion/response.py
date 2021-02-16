
import aiohttp
from pydantic import BaseModel


class SightResponseError(Exception):
    """SightResponseStatusCodeError"""

    def __init__(self, response: aiohttp.ClientResponse):
        super().__init__(f'SightError url={response.url}, status={response.status}')


class SightResponseLoginCharactersAccountCharacter(BaseModel):
    cid: str
    name: str
    world: str
    status: int
    faceUrl: str
    bodyUrl: str
    lodestonecid: str
    isRenamed: bool


class SightResponseLoginCharactersAccount(BaseModel):
    accName: str
    contractEndTime: int
    role: int
    xDay: int
    characters: list[SightResponseLoginCharactersAccountCharacter]


class SightResponseLoginCharacters(BaseModel):
    updatedAt: int
    apiParameters: dict
    accounts: list[SightResponseLoginCharactersAccount]


class SightResponseLoginCharacterDomains(BaseModel):
    lodestone: str
    cdn1: str
    cdn2: str
    appWeb: str


class SightResponseLoginCharacterCharacter(BaseModel):
    cid: str
    name: str
    world: str
    portrait: str
    lodestonecid: str


class SightResponseLoginCharacter(BaseModel):
    updatedAt: int
    domains: SightResponseLoginCharacterDomains
    role: int
    character: SightResponseLoginCharacterCharacter


class SightResponseCharacterLoginStatus(BaseModel):
    getBagFlag: bool
    world: str
    currentWorld: str


class SightResponseLoginToken(BaseModel):
    token: str
    salt: str
    region: str


class CompanionErrorResponse(Exception):
    def __init__(self, response: aiohttp.ClientResponse, error_code: int = None, json_data: dict = None):
        self.response = response
        self.status_code = response.status
        self.error_code = error_code
        self.json_data = json_data

    @classmethod
    async def select(cls, response: aiohttp.ClientResponse):
        try:
            json_data: dict = await response.json()
            if error := json_data.get('error'):
                error_code = error['code']
                if error_code == 100000:
                    return CompanipnAppMaintenanceError(response, error_code)
                if error_code == 111001:
                    return AuthorizationError(response, error_code)
                if error_code == 210010:
                    return LoginLobbyError(response, error_code)
                if error_code == 319201:
                    return ServerMaintenanceError(response, error_code)
                if error_code == 340000:
                    return BrokeError(response, error_code)
                return UnKnownCodeError(response, error_code)
            else:
                return cls(response, json_data=json_data)
        except Exception:
            return cls(response)


class UnKnownCodeError(CompanionErrorResponse):
    """UnKnownErrorCode"""


class AuthorizationError(CompanionErrorResponse):
    """AuthorizationError"""


class ServerMaintenanceError(CompanionErrorResponse):
    """ServerMaintenanceError"""


class BrokeError(CompanionErrorResponse):
    """BrokeError"""


class LoginLobbyError(CompanionErrorResponse):
    """LoginLobbyError"""


class CompanipnAppMaintenanceError(CompanionErrorResponse):
    """CompanipnAppMaintenanceError"""
