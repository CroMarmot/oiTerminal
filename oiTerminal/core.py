import importlib
import time

from oiTerminal.Model.LangKV import LangKV
from oiTerminal.utils import logger, OJUtil
from oiTerminal.platforms.base import Base

from oiTerminal.Model.Problem import Problem
from oiTerminal.Model.Result import Result
from oiTerminal.Model.Contest import Contest
from oiTerminal.Model.Account import Account


class OJBuilder(object):
    @staticmethod
    def build_oj(name, *args, **kwargs):
        if name:
            try:
                module_meta = importlib.import_module(f'oiTerminal.platforms.{str(name).lower()}')
                class_meta = getattr(module_meta, name)
                print('Load Class:' + str(class_meta))
                oj = class_meta(*args, **kwargs)
                return oj
            except ModuleNotFoundError as e:
                logger.exception(e)
        return None


class Core(object):
    _account: Account

    def __init__(self, oj_name: str, proxies=None, timeout=5, account: Account = None):
        if oj_name not in OJUtil.get_supports():
            raise Exception("oj name error or not supported")
        self._oj: Base = OJBuilder.build_oj(oj_name, proxies=proxies, timeout=timeout)
        self._out_date: int = time.time() - 1

    def set_account(self, account: Account) -> 'Core':
        self._account = account
        return self

    # 获取比赛 以及所有比赛题面
    def get_contest(self, cid: str) -> Contest:
        if not self._oj or not self._oj.support_contest():
            raise Exception('get_contest: ERROR')
        if self._oj.account_required():
            self._login()
        return self._oj.get_contest(cid=cid)

    # 获取题面
    def get_problem(self, pid: str) -> Problem:
        if not self._oj:
            raise Exception('get_problem: ERROR')
        if self._oj.account_required():
            self._login()
        return self._oj.get_problem(pid=pid)

    # 提交代码
    def submit_code(self, pid: str, language: str, code: str) -> bool:
        if not self._oj:
            raise Exception('submit_code: ERROR')
        self._login()
        return self._oj.submit_code(pid=pid, language=language, code=code)

    # 获取结果
    def get_result(self, pid: str) -> Result:
        if not self._oj:
            raise Exception('get_result: ERROR')
        self._login()
        return self._oj.get_result(pid=pid)

    # 通过运行id获取结果
    def get_result_by_rid_and_pid(self, quick_id: str) -> Result:
        if not self._oj:
            raise Exception('get_result_by_quick_id: ERROR')
        assert (self._is_login())
        return self._oj.get_result_by_quick_id(quick_id=quick_id)

    # 获取源OJ语言
    def get_language(self) -> LangKV:
        if not self._oj:
            raise Exception('get_language: ERROR')
        self._login()
        return self._oj.get_language()

    def _login(self):
        if not self._is_login():
            self._out_date = time.time() + self._oj.login_website(self._account)

    def _is_login(self) -> bool:
        return time.time() < self._out_date
