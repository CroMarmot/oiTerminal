import importlib
import time

from oiTerminal.model import Problem, Result, Contest, Account
from oiTerminal.utils import logger, OJUtil
from oiTerminal.platforms.base import Base


class OJBuilder(object):
    @staticmethod
    def build_oj(name, *args, **kwargs):
        if name:
            try:
                module_meta = importlib.import_module(f'oiTerminal.platforms.{str(name).lower()}')
                class_meta = getattr(module_meta, name)
                print(class_meta)
                oj = class_meta(*args, **kwargs)
                return oj
            except ModuleNotFoundError as e:
                logger.exception(e)
        return None


class Core(object):
    def __init__(self, oj_name, proxies=None, timeout=5):
        if not self.is_support(oj_name):
            raise Exception("oj name error or not supported")
        self._remote_oj = oj_name
        self._oj: Base = OJBuilder.build_oj(oj_name, proxies=proxies, timeout=timeout)

    # 判断当前是否支持
    @staticmethod
    def is_support(oj_name):
        return oj_name in OJUtil.get_supports()

    def get_home_page_url(self):
        if not self._oj:
            return None
        return self._oj.home_page_url()

    def get_cookies(self):
        if not self._oj:
            return None
        return self._oj.get_cookies()

    # 获取题面的时候是否需要登录状态
    def account_required(self):
        return self._oj.account_required()

    # 获取比赛 以及所有比赛题面
    def get_contest(self, cid, account):
        if not self._oj or not self.is_support_contest():
            return Contest(oj=self._remote_oj, cid=cid, status=Contest.Status.STATUS_ERROR)
        return self._oj.get_contest(cid=cid, account=account)

    # 获取题面
    def get_problem(self, pid, account):
        if not self._oj:
            return Problem(oj=self._remote_oj, pid=pid, status=Problem.Status.STATUS_ERROR)
        self._oj.set_cookies(account.cookies)
        return self._oj.get_problem(pid=pid, account=account)

    # 提交代码
    def submit_code(self, account, pid, language, code):
        if not self._oj:
            return Result(Result.Status.STATUS_SYSTEM_ERROR)
        self._oj.set_cookies(account.cookies)
        if self._oj.submit_code(account, pid, language, code):
            time.sleep(2)
            return self.get_result(account=account, pid=pid)
        else:
            return Result(Result.Status.STATUS_SUBMIT_ERROR)

    # 获取结果
    def get_result(self, account: Account, pid):
        if not self._oj:
            return Result(Result.Status.STATUS_SYSTEM_ERROR)
        self._oj.set_cookies(account.cookies)
        result = None
        try:
            result = self._oj.get_result(account=account, pid=pid)
        except Exception as e:
            print(e)
            pass
        if result is not None:
            if self._oj.is_accepted(result.verdict_info):
                result.verdict = Result.Verdict.VERDICT_AC
            elif self._oj.is_running(result.verdict_info):
                result.verdict = Result.Verdict.VERDICT_RUNNING
            elif self._oj.is_compile_error(result.verdict_info):
                result.verdict = Result.Verdict.VERDICT_CE
            else:
                result.verdict = Result.Verdict.VERDICT_WA
            return result
        return Result(Result.Status.STATUS_RESULT_ERROR)

    # 通过运行id获取结果
    def get_result_by_rid_and_pid(self, account: Account, pid, unique_key):
        if not self._oj:
            return Result(Result.Status.STATUS_SYSTEM_ERROR)
        result = None
        try:
            result = self._oj.get_result_by_rid_and_pid(account, pid, unique_key)
        except:
            pass
        if result is not None:
            if self._oj.is_accepted(result.verdict_info):
                result.verdict = Result.Verdict.VERDICT_AC
            elif self._oj.is_running(result.verdict_info):
                result.verdict = Result.Verdict.VERDICT_RUNNING
            elif self._oj.is_compile_error(result.verdict_info):
                result.verdict = Result.Verdict.VERDICT_CE
            else:
                result.verdict = Result.Verdict.VERDICT_WA
            return result
        return Result(Result.Status.STATUS_RESULT_ERROR)

    # 获取源OJ语言
    def find_language(self, account):
        if not self._oj:
            return None
        self._oj.set_cookies(account.cookies)
        return self._oj.find_language(account=account)

    # 判断源OJ的网络连接是否良好
    def is_working(self):
        if not self._oj:
            return None
        return self._oj.is_working()

    # 判断结果是否AC
    def is_accepted(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_accepted(verdict)

    # 判断是否运行中或者排队中
    def is_running(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_running(verdict)

    # 判断是否编译错误
    def is_compile_error(self, verdict):
        if not self._oj:
            return None
        return self._oj.is_compile_error(verdict)

    # 判断爬虫账号是否可以正常登陆
    def is_account_valid(self, account):
        if self._oj and account and self._oj.login_website(account=account):
            return True
        return False

    def is_support_contest(self):
        if not self._oj:
            return None
        return self._oj.support_contest()
