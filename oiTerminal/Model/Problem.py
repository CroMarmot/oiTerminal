from oiTerminal.Model.TestCases import TestCases


class Problem:
    def __init__(self,
                 pid: str,
                 oj: str,
                 description: str = '',
                 test_cases: TestCases = None,
                 time_limit: str = '',
                 mem_limit: str = '',
                 url: str = ''):
        self._id: str = pid
        self._oj: str = oj
        self._description: str = description
        self._test_cases: TestCases = test_cases
        self._time_limit: str = time_limit
        self._mem_limit: str = mem_limit
        self._url: str = url

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
    def test_cases(self) -> TestCases:
        return self._test_cases

    @test_cases.setter
    def test_cases(self, value: TestCases):
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
