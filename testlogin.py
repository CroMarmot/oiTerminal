from ac_core.auth import fetch_login, is_logged_in
from ac_core.interfaces.HttpUtil import HttpRespInterface, HttpUtilInterface


class Helper(HttpRespInterface, HttpUtilInterface):

    def __init__(self, session):
        self.session = session
        self.text = ''
        self.status = 0

    def get(self, url: str, allow_redirects=True) -> HttpRespInterface:
        resp = self.session.get(url=url, allow_redirects=allow_redirects)
        self.status = resp.status_code
        self.text = resp.text
        return self

    def post(self, url: str, data: str) -> HttpRespInterface:
        resp = self.session.post(url=url, data=data)
        self.status = resp.status_code
        self.text = resp.text
        return self


import requests
h = Helper(requests.session())
print(is_logged_in(h))
print(fetch_login(h, 'cromarmot', '2013woyiwangji'))
