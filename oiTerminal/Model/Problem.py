from oiTerminal.Model.TestCase import TestCase
from typing import List
from enum import Enum


class Problem:
    class Status(Enum):
        AC = 'AC'
        FAILED = 'FAILED'
        NOTVIS = 'NOTVIS'

    title: str
    status: Status
    _test_cases: List[TestCase]

    def __init__(self,
                 pid: str,
                 oj: str,
                 description: str = '',
                 test_cases: List[TestCase] = None,
                 time_limit: str = '',
                 mem_limit: str = '',
                 url: str = '',
                 html: str = ''):
        self._id: str = pid
        self._oj: str = oj
        self._description: str = description
        if test_cases is None:
            self._test_cases = []
        else:
            self._test_cases = test_cases
        self._time_limit: str = time_limit
        self._mem_limit: str = mem_limit
        self._url: str = url
        self._html: str = html

    @property
    def id(self) -> str:
        return self._id

    @property
    def oj(self) -> str:
        return self._oj

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def test_cases(self) -> List[TestCase]:
        return self._test_cases

    @test_cases.setter
    def test_cases(self, value: List[TestCase]):
        self._test_cases = value

    @property
    def time_limit(self) -> str:
        return self._time_limit

    @time_limit.setter
    def time_limit(self, value: str):
        self._time_limit = value

    @property
    def mem_limit(self) -> str:
        return self._mem_limit

    @mem_limit.setter
    def mem_limit(self, value: str):
        self._mem_limit = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def html(self) -> str:
        return self._html

    @html.setter
    def html(self, value: str):
        self._html = value

    def __repr__(self):
        return Problem.__name__ + str(self.__dict__)

    def __str__(self):
        return self.__repr__()
