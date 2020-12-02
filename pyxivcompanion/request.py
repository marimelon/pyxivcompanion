import asyncio
import copy

import aiohttp
from .config import Config

class CompanionRequest():
    APP_VERSION = Config.APP_VERSION

    ACCEPT_ALL = '*/*'
    ACCEPT_1 = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    ACCEPT_LANGUAGE_JP = 'ja-jp'
    KEEP_ALIVE = 'keep-alive'
    CONTENT_TYPE_JSON = 'application/json;charset=utf-8'
    CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded'
    USER_AGENT = f'xivcompanion-JP/{APP_VERSION} Device/1'
    USER_AGENT_2 = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) XIV-Companion for iPhone'
    ACCEPTENCODING = "br, gzip, deflate-alive"

    proxy_url = None

    def __init__(self, url,
                 Accept=ACCEPT_ALL,
                 ContentType=CONTENT_TYPE_JSON,
                 Connection=KEEP_ALIVE,
                 AcceptLanguage=ACCEPT_LANGUAGE_JP,
                 UserAgent=USER_AGENT,
                 AcceptEncoding=ACCEPTENCODING,
                 Origin=None,
                 Referer=None,
                 RequestID=None,
                 Token=None,
                 Cookie=None):
        self.url = url
        self.Accept = Accept
        self.ContentType = ContentType
        self.Connection = Connection
        self.AcceptLanguage = AcceptLanguage
        self.UserAgent = UserAgent
        self.AcceptEncoding = AcceptEncoding
        self.Origin = Origin
        self.Referer = Referer
        self.RequestID = RequestID
        self.Token = Token
        self.Cookie = Cookie

    def create_headers(self) -> dict:
        dic = {"Accept": self.Accept,
               "Content-Type": self.ContentType,
               "Connection": self.Connection,
               "Accept-Language": self.AcceptLanguage,
               "User-Agent": self.UserAgent,
               "Accept-Encoding": self.AcceptEncoding,
               "Origin": self.Origin,
               "Referer": self.Referer,
               "request-id": self.RequestID,
               "token": self.Token,
               "Cookie": self.Cookie}

        def delete_if_none(dic):
            for k in list(dic):
                if dic.get(k) is None:
                    del(dic[k])
            return dic

        return copy.copy(delete_if_none(dic))

    async def post(self, json: dict = None, data=None, session: aiohttp.ClientSession = None, process_accepted=True, allow_redirects=True) -> aiohttp.ClientResponse:
        if session is None:
            _session = aiohttp.ClientSession(trust_env=True,
                                             connector=aiohttp.TCPConnector(verify_ssl=False))
        else:
            _session = session

        try:
            res = await _session.post(url=self.url,
                                      data=data,
                                      json=json,
                                      headers=self.create_headers(),
                                      allow_redirects=allow_redirects)
            if process_accepted and res.status == 202:
                await asyncio.sleep(2)
                return await self.post(json=json, session=session, process_accepted=process_accepted, allow_redirects=allow_redirects)
            else:
                await res.read()
                return res
        finally:
            if session is None:
                await _session.close()

    async def get(self, params: dict = None, session: aiohttp.ClientSession = None, process_accepted=True, allow_redirects=True) -> aiohttp.ClientResponse:
        if session is None:
            _session = aiohttp.ClientSession(trust_env=True,
                                             connector=aiohttp.TCPConnector(verify_ssl=False))
        else:
            _session = session

        try:
            res = await _session.get(url=self.url,
                                     headers=self.create_headers(),
                                     allow_redirects=allow_redirects,
                                     params=params)
            if process_accepted and res.status == 202:
                await asyncio.sleep(2)
                return await self.get(params=params, session=_session, process_accepted=process_accepted)
            else:
                await res.read()
                return res
        finally:
            if session is None:
                await _session.close()
