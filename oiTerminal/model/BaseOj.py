from oiTerminal.model.Account import Account
from oiTerminal.model.Contest import Contest
from oiTerminal.model.LangKV import LangKV
from oiTerminal.model.ParseProblemResult import ParseProblemResult
from oiTerminal.model.Problem import Problem
from oiTerminal.model.Result import Result


class BaseOj(object):
  short_name = []

  def __init__(self):
    pass

  def problem(self, problem_id) -> ParseProblemResult:
    pass

  # return login cookie effective time in second
  def login_website(self, account: Account) -> int:
    pass

  def reg_contest(self, cid: str) -> bool:
    pass

  def get_contest(self, cid: str) -> Contest:
    pass

  def get_problem(self, pid: str) -> Problem:
    pass

  def submit_code(self, pid: str, language: str, code: str) -> bool:
    pass

  def get_result(self, pid) -> Result:
    pass

  def get_result_by_quick_id(self, quick_id: str) -> Result:
    pass

  def get_language(self) -> LangKV:
    pass

  def print_contest_list(self) -> None:
    pass

  def print_problems_in_contest(self, cid: str) -> None:
    pass

  def print_friends_standing(self, cid: str) -> None:
    pass

  # require account for view problem/contest/fetch result

  @staticmethod
  def account_required() -> bool:
    pass

  @staticmethod
  def support_contest():
    pass
