from typing import List


class TestCase:
    def __init__(self, in_data: str, out_data: str):
        self._in: str = in_data
        self._out: str = out_data

    @property
    def in_data(self) -> str:
        return self._in

    @property
    def out_data(self) -> str:
        return self._out

    def __eq__(self, other: 'TestCase') -> bool:
        return self._in == other._in and self._out == other._out


class TestCases:
    testpaths = ./tests
python_files = test_*.py
    def __init__(self):
        self._tc: List[TestCase] = []

    def append(self, data: TestCase):
        self._tc.append(data)

    @property
    def data(self):
        return self._tc

    def __eq__(self, other: 'TestCases') -> bool:
        return self._tc == other._tc
