from typing import List
from enum import Enum

from oi_cli2.model.TestCase import TestCase


class ParseProblemResult(object):
    class Status(Enum):
        AC = 'AC'
        FAILED = 'FAILED'
        NOTVIS = 'NOTVIS'

    def __init__(self):
        self.status: ParseProblemResult.Status = ParseProblemResult.Status.NOTVIS
        self.title: str = ''
        self.test_cases: List[TestCase] = []
        self.id: str = ''
        self.oj: str = ''
        self.description: str = ''
        self.time_limit: str = ''
        self.mem_limit: str = ''
        self.url: str = ''
        self.html: str = ''
        self.file_path: str = ''

    def __repr__(self):
        return ParseProblemResult.__name__ + str(self.__dict__)

    def __str__(self):
        return self.__repr__()
