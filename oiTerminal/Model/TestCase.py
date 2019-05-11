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

    def __repr__(self):
        return TestCase.__name__ + str(self.__dict__)

    def __str__(self):
        return self.__repr__()
