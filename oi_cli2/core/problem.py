from typing import List

from oi_cli2.model.ParseProblemResult import ParsedProblemResult
from oi_cli2.model.TestCase import TestCase
from oi_cli2.utils.FileUtil import FileUtil


class problem:

  def __init__(self, oj):
    self.oj = oj

  # file_util can be any thing , everything is file
  def parse(self, problem_id: str, file_util: FileUtil):
    result = self.oj.parse(problem_id)
    # html: str = result.html
    test_cases: List[TestCase] = result.test_cases

    # TODO switch directory

    for i in range(len(test_cases)):
      file_util.write(f'in.{i}', test_cases[i].in_data)
      file_util.write(f'out.{i}', test_cases[i].in_data)
