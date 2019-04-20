class Account:
    def __init__(self, username: str, password: str, cookie: str = None):
        self._u = username
        self._p = password
        self._c = cookie

    @property
    def username(self) -> str:
        return self._u

    @property
    def password(self) -> str:
        return self._p

    @property
    def cookie(self) -> str:
        return self._c

    @cookie.setter
    def cookie(self, value: str):
        self._c = value

    @cookie.deleter
    def cookie(self):
        self._c = None
