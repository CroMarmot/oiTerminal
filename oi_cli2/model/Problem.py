from typing import List
from enum import Enum

from oi_cli2.model.TestCase import TestCase


class Problem:

  class Status(Enum):
    AC = 'AC'
    FAILED = 'FAILED'
    NOTVIS = 'NOTVIS'

  title: str
  status: Status
  test_cases: List[TestCase]

  def __init__(self,
               pid: str,
               oj: str,
               description: str = '',
               test_cases: List[TestCase] = None,
               time_limit: str = '',
               mem_limit: str = '',
               url: str = '',
               html: str = ''):
    self.id: str = pid
    self.oj: str = oj
    self.description: str = description
    if test_cases is None:
      # don't place it on arguments
      self.test_cases = []
    else:
      self.test_cases = test_cases
    self.time_limit: str = time_limit
    self.mem_limit: str = mem_limit
    self.url: str = url
    self.html: str = html

  def __repr__(self):
    return Problem.__name__ + str(self.__dict__)

  def __str__(self):
    return self.__repr__()
