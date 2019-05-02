from oiTerminal.Model.Account import Account
from oiTerminal.Model.Contest import Contest
from oiTerminal.Model.LangKV import LangKV
from oiTerminal.Model.Problem import Problem
from oiTerminal.Model.Result import Result


class BaseParser(object):
    def contest_parse(self, response):
        pass

    def problem_parse(self, response, pid, url):
        pass

    def result_parse(self, response):
        pass


class Base(object):
    # return login effective time in second
    def login_website(self, account: Account) -> int:
        print('Base login_website')
        return -1

    # 检查登录状态
    def is_login(self) -> bool:
        print('Base is_login')
        return False

    # 获取题目
    def get_contest(self, cid: str) -> Contest:
        pass

    # 获取题目
    def get_problem(self, pid: str) -> Problem:
        pass

    # 提交代码
    def submit_code(self, pid: str, language: str, code: str) -> bool:
        pass

    def get_result(self, pid) -> Result:
        pass

    def get_result_by_quick_id(self, quick_id: str) -> Result:
        pass

    def get_language(self) -> LangKV:
        print('Base get_language')
        pass

    def is_working(self) -> bool:
        pass

    # require account for view problem/contest/fetch result
    @staticmethod
    def account_required() -> bool:
        pass

    @staticmethod
    def support_contest():
        pass

    # TODO 把这个判断内置到 结果的struct中而不是oj的
    #  判断结果是否正确
    @staticmethod
    def is_accepted(verdict):
        pass

    # 判断是否编译错误
    @staticmethod
    def is_compile_error(verdict):
        pass

    # 判断是否运行中
    @staticmethod
    def is_running(verdict):
        pass
