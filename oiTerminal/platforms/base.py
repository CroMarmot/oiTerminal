from oiTerminal.Model.Account import Account
from oiTerminal.Model.Contest import Contest
from oiTerminal.Model.LangKV import LangKV
from oiTerminal.Model.Problem import Problem
from oiTerminal.Model.Result import Result


class BaseParser(object):
    def contest_parse(self, contest: Contest, response: str):
        pass

    def problem_parse(self, problem: Problem, response: str):
        pass

    def result_parse(self, response: str) -> Result:
        pass


class Base(object):
    # return login cookie effective time in second
    def login_website(self, account: Account) -> int:
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

    # require account for view problem/contest/fetch result
    @staticmethod
    def account_required() -> bool:
        pass

    @staticmethod
    def support_contest():
        pass
