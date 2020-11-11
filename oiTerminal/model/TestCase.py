class TestCase:
    def __init__(self, in_data: str, out_data: str):
        self.in_data: str = in_data
        self.out_data: str = out_data

    def __eq__(self, other: 'TestCase') -> bool:
        return self.in_data == other.in_data and self.out_data == other.out_data

    def __repr__(self):
        return TestCase.__name__ + str(self.__dict__)

    def __str__(self):
        return self.__repr__()
