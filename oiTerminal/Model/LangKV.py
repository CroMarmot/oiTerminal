# Language Key Value List
from typing import Dict


class LangKV:
    _data: Dict[str, str]

    def __init__(self):
        self._data = {}

    def set(self, k: str, v: str):
        assert (isinstance(k, str))
        assert (isinstance(v, str))
        self._data[k] = v

    def get(self, k: str) -> str:
        assert (isinstance(k, str))
        return self._data[k]

    @property
    def data(self):
        return self._data

