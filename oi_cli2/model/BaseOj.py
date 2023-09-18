from typing import Any, Union, AsyncIterator

from oi_cli2.model.LangKV import LangKV
from oi_cli2.model.ParseProblemResult import ParsedProblemResult
from oi_cli2.model.ProblemMeta import ContestMeta, ProblemMeta
from oi_cli2.model.Result import SubmissionResult


class BaseOj(object):

  def __init__(self):
    pass

  async def init(self) -> None:
    pass

  async def deinit(self) -> None:
    pass

  def problem_by_id(self, problem_id: str) -> ParsedProblemResult:
    assert (False)

  async def async_problem(self, problem: ProblemMeta) -> ParsedProblemResult:
    assert (False)

  def problem(self, problem: ProblemMeta) -> ParsedProblemResult:
    assert (False)

  def login_website(self, force: bool = False) -> bool:
    assert (False)

  def reg_contest(self, cid: str) -> bool:
    assert (False)

  def submit_code(self, problem_url: str, language_id: str, code_path: str) -> Union[bool, Any]:
    assert (False)

  async def async_get_result_yield(self, problem_url: str, time_gap: float = 1) -> AsyncIterator[SubmissionResult]:
    raise NotImplementedError
    yield 0

  def get_language(self) -> LangKV:
    assert (False)

  def print_contest_list(self) -> bool:
    assert (False)

  def print_friends_standing(self, cid: str) -> None:
    assert (False)

  async def async_get_contest_meta(self, cid: str) -> ContestMeta:
    assert (False)

  def get_contest_meta(self, cid: str) -> ContestMeta:
    assert (False)

  @staticmethod
  def account_required() -> bool:
    assert (False)

  @staticmethod
  def support_contest():
    assert (False)

  def cid2url(self, cid: str) -> str:
    assert (False)
