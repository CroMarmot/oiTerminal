from dataclasses import dataclass, field
from enum import Enum
from typing import List

from oi_cli2.model.ParseProblemResult import ParsedProblemResult


class E_STATUS(str, Enum):
  NOT_SUBMITTED = ""
  AC = "AC"
  ERROR = "ERROR"


@dataclass
class ProblemMeta:
  id: str = ''
  url: str = ''
  name: str = ''
  passed: str = ''  # number of passed submission in contest
  score: int = 0
  status: E_STATUS = E_STATUS.NOT_SUBMITTED
  time_limit_msec: int = 0  # ms
  memory_limit_kb: int = 0  # mb
  contest_id: str = ''

  def __repr__(self) -> str:
    res = ''
    res += '{'
    for key in self.__dict__:
      res += f'[{key}:{self.__dict__[key]}]'
    res += '}'
    return res
    


@dataclass
class ContestMeta:
  id: str = ''
  url: str = ''
  problems: List[ProblemMeta] = field(default_factory=lambda: [])
