import binascii
import hashlib
import re
import urllib.parse
import uuid
from base64 import b64decode, b64encode
from importlib.resources import open_binary

import aiohttp
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from .config import Config
from .request import CompanionRequest
from .response import (SightResponseCharacterLoginStatus, SightResponseError,
                       SightResponseLoginCharacter,
                       SightResponseLoginCharacters, SightResponseLoginToken)


class LoginObj:
    def __init__(self, userId, token, salt):
        self.userId = userId
        self.token = token
        self.salt = salt

    async def get_characters(self) -> SightResponseLoginCharacters:
        req = CompanionRequest(url=f'{Config.GLOBAL_COMPANION_BASE}login/characters',
                               RequestID=str(uuid.uuid1()).upper(),
                               Token=self.token)
        res = await req.get()
        if not res.status == 200:
            raise SightResponseError(res)

        data = await res.json()
        return SightResponseLoginCharacters(**data)

    async def get_region(self, cid: str) -> str:
        req = CompanionRequest(url=f'{Config.GLOBAL_COMPANION_BASE}login/characters/{cid}',
                               RequestID=str(uuid.uuid1()).upper(),
                               Token=self.token)
        res = await req.post(json={"appLocaleType": "JP"})
        if not res.status == 200:
            raise SightResponseError(res)

        res_data = await res.json()

        return res_data['region']

    async def login_character(self) -> SightResponseLoginCharacter:
        req = CompanionRequest(url=f'{Config.GLOBAL_COMPANION_BASE}login/character',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=self.token)
        res = await req.get()
        if not res.status == 200:
            raise SightResponseError(res)

        data = await res.json()
        return SightResponseLoginCharacter(**data)

    async def character_login_status(self) -> SightResponseCharacterLoginStatus:
        req = CompanionRequest(url=f'{Config.GLOBAL_COMPANION_BASE}character/login-status',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=self.token)
        res = await req.get()
        if not res.status == 200:
            raise SightResponseError(res)
        data = await res.json()
        return SightResponseCharacterLoginStatus(**data)

    async def character_worlds(self):
        req = CompanionRequest(url=f'{Config.GLOBAL_COMPANION_BASE}character/worlds',
                               RequestID=str(uuid.uuid4()).upper(),
                               Token=self.token)
        res = await req.get()
        if not res.status == 200:
            raise SightResponseError(res)


class Account:
    @staticmethod
    async def login(sqex_id: str, sqex_pass: str, otp: str = None,
                    *, userId: str = None, token: str = None, salt: str = None):
        userId = str(uuid.uuid4()) if userId is None else userId
        requestId = str(uuid.uuid1()).upper()

        async with aiohttp.ClientSession(trust_env=True,
                                         connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            if token is None or salt is None:
                token, salt = await Account.__get_new_token(userId, session)

            uid = Account.__get_uid(userId, salt)
            loginUrl = Account.__build_login_url(token, uid, requestId)
            await Account.__login_process(sqex_id, sqex_pass, otp, loginUrl, session)
            await Account.__postauth(token, uid, requestId, session)

        return LoginObj(userId=userId, token=token, salt=salt)

    @staticmethod
    async def request_token(userId: str, session: aiohttp.ClientSession = None) -> SightResponseLoginToken:
        with open_binary(__package__, 'public-key.pem') as f:
            key64 = f.read()
        keyDER = b64decode(key64)
        keyPub = RSA.importKey(keyDER)
        cipher = PKCS1_v1_5.new(keyPub)
        uid = b64encode(cipher.encrypt(userId.encode())).decode()
        req = CompanionRequest(url=f'{Config.GLOBAL_COMPANION_BASE}login/token',
                               RequestID=str(uuid.uuid1()).upper())
        res = await req.post(json={"uid": uid, "platform": 2, "appVersion": Config.APP_VERSION}, session=session)

        if not res.status == 200:
            raise SightResponseError(res)

        data = await res.json()
        return SightResponseLoginToken(**data)

    @staticmethod
    async def __get_new_token(userid: str, session: aiohttp.ClientSession):

        res_data = await Account.request_token(userid, session=session)

        return (res_data.token, res_data.salt)

    @staticmethod
    def __get_uid(userid: str, salt: str):
        dk = hashlib.pbkdf2_hmac(hash_name='sha1',
                                 password=userid.encode(),
                                 salt=salt.encode(),
                                 iterations=1000,
                                 dklen=128)
        return binascii.hexlify(dk).decode()

    @staticmethod
    def __build_login_url(token: str, uid: str, request_id: str) -> str:
        def __build_oauth_redirect_url():
            url = f'{Config.GLOBAL_COMPANION_BASE_URL}api/0/auth/callback' + '?'
            url += 'token=' + token + '&'
            url += 'uid=' + uid + '&'
            url += 'request_id=' + request_id
            return urllib.parse.quote(url, safe='')

        url = f'{Config.SECURE_SQUARE_ENIX_URL_BASE}oauth/oa/oauthauth' + '?'
        url += 'client_id=' + 'ffxiv_comapp' + '&'
        url += 'lang=' + 'ja-ja' + '&'
        url += 'response_type=' + 'code' + '&'
        url += 'redirect_uri=' + __build_oauth_redirect_url()
        return url

    @staticmethod
    async def __login_process(username, password, otp, loginurl, session):
        req = CompanionRequest(url=loginurl,
                               UserAgent=CompanionRequest.USER_AGENT_2,
                               Accept=CompanionRequest.ACCEPT_1)
        res = await req.get(session=session)
        if not res.status == 200:
            raise SightResponseError(res)
        text = await res.text()

        if not 'cis_sessid' in text:
            # Login form
            # oauthlogin.send?client_id=...
            action1 = re.search(
                r'(.*)action="(?P<action>[^"]+)">', text).group('action')
            stored = re.search(
                r'(.*)name="_STORED_" value="(?P<stored>[^"]+)">', text).group('stored')
            form_date1 = f'_STORED_={stored}&sqexid={username}&password={password}'

            req = CompanionRequest(url=f'{Config.SECURE_SQUARE_ENIX_URL_BASE}oauth/oa/{action1}',
                                   Origin=Config.SECURE_SQUARE_ENIX_URL_BASE.removesuffix(
                                       '/'),
                                   UserAgent=CompanionRequest.USER_AGENT_2,
                                   Accept=CompanionRequest.ACCEPT_1,
                                   ContentType=CompanionRequest.CONTENT_TYPE_FORM)
            res = await req.post(data=form_date1, session=session, allow_redirects=False)

            if res.status == 200:
                # OTP form
                text = await res.text()
                # oauthlogin.sendOtp?client_id=...
                action2 = re.search(
                    r'(.*)action="(?P<action>[^"]+)" method="post">', text).group('action')
                stored = re.search(
                    r'(.*)name="_STORED_" value="(?P<stored>[^"]+)">', text).group('stored')
                form_date2 = f'_STORED_={stored}&otppw={otp}'
                req = CompanionRequest(url=f'{Config.SECURE_SQUARE_ENIX_URL_BASE}oauth/oa/{action2}',
                                       Origin=Config.SECURE_SQUARE_ENIX_URL_BASE.removesuffix(
                                           '/'),
                                       UserAgent=CompanionRequest.USER_AGENT_2,
                                       Accept=CompanionRequest.ACCEPT_1,
                                       ContentType=CompanionRequest.CONTENT_TYPE_FORM)
                res = await req.post(data=form_date2, session=session, allow_redirects=False)

            if not res.status == 302:
                raise SightResponseError(res)

            redirect = res.headers['Location']
            req = CompanionRequest(url=redirect,
                                   Cookie=f'_rsid="";_si={res.cookies["_si"].value}')
            res = await req.get(session=session)
            if not res.status == 200:
                raise SightResponseError(res)
            text = await res.text()
        else:
            redirect = None

        action = re.search(
            r'(.*)action="(?P<action>[^"]+)">', text).group('action').replace('&amp;', '&')
        cis_sessid = re.search(
            r'(.*)name="cis_sessid" type="hidden" value="(?P<cis_sessid>[^"]+)">', text).group('cis_sessid')
        form_date = f'cis_sessid={cis_sessid}&provision=&_c=1'
        req = CompanionRequest(url=action,
                               UserAgent=CompanionRequest.USER_AGENT_2,
                               Accept=CompanionRequest.ACCEPT_1,
                               ContentType=CompanionRequest.CONTENT_TYPE_FORM,
                               Origin=Config.SECURE_SQUARE_ENIX_URL_BASE.removesuffix(
                                   '/'),
                               Referer=redirect)
        res = await req.post(data=form_date, session=session)
        if not res.status == 200:
            raise SightResponseError(res)

    @staticmethod
    async def __postauth(token, uid, request_id, session):
        url = f'{Config.GLOBAL_COMPANION_BASE}login/auth?'
        url += 'token=' + token + '&'
        url += 'uid=' + uid + '&'
        url += 'request_id=' + request_id

        req = CompanionRequest(url=url, RequestID=request_id, Token=token)
        res = await req.post(session=session)
        if not res.status == 200:
            raise SightResponseError(res)
