from typing import Any, Dict, List
from oi_cli2.model.Contest import Contest
from oi_cli2.model.LangKV import LangKV
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.model.Problem import Problem
from oi_cli2.model.ProblemMeta import ContestMeta 
from oi_cli2.model.Result import Result


class BaseOj(object):
  def __init__(self):
    pass

  def problem(self, problem_id: str) -> ParseProblemResult:
    assert(False)

  def login_website(self, force: bool=False) -> bool:
    assert(False)

  def reg_contest(self, cid: str) -> bool:
    assert(False)

  def get_contest(self, cid: str) -> Contest:
    assert(False)

  def get_problem(self, pid: str) -> Problem:
    assert(False)

  def submit_code(self, pid: str, language: str, code: str) -> bool:
    assert(False)

  def get_result(self, pid) -> Result:
    assert(False)

  def get_result_by_quick_id(self, quick_id: str) -> Result:
    assert(False)

  def get_language(self) -> LangKV:
    assert(False)

  def print_contest_list(self) -> bool:
    assert(False)

  def print_friends_standing(self, cid: str) -> None:
    assert(False)

  def get_contest_meta(self, cid:str) -> ContestMeta:
    assert(False)

  # require account for view problem/contest/fetch result

  @staticmethod
  def account_required() -> bool:
    assert(False)

  @staticmethod
  def support_contest():
    assert(False)

