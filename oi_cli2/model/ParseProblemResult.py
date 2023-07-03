from dataclasses import dataclass, field
from typing import List
from enum import Enum

from oi_cli2.model.TestCase import TestCase


@dataclass
class ParsedProblemResult(object):

  class Status(Enum):
    AC = 'AC'
    FAILED = 'FAILED'
    NOTVIS = 'NOTVIS'

  status: Status = Status.NOTVIS
  title: str = ''
  test_cases: List[TestCase] = field(default_factory=lambda: [])
  id: str = ''
  oj: str = ''
  description: str = ''
  time_limit: str = ''
  mem_limit: str = ''
  url: str = ''
  html: str = ''
  file_path: str = ''
