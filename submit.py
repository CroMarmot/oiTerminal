import time
import os

from oiTerminal.model import Account
from oiTerminal.model import Problem, Result
from oiTerminal.core import Core
from oiTerminal.utils import OJUtil


def submit(
        oj: str,
        pid: str,
        language: str,
        account: Account,
        file_path: str,
):
    ans = False
    tries = 3
    core = Core(oj)
    while not ans and tries > 0:
        tries -= 1
        ans = core.submit_code(pid=pid, account=account, code=file_path, language=language)
        account.set_cookies(core.get_cookies())
    if ans.status in [Result.Status.STATUS_SUBMIT_ERROR,
                      Result.Status.STATUS_SPIDER_ERROR,
                      Result.Status.STATUS_SYSTEM_ERROR]:
        return "SUBMIT FAILED"
    result = core.get_result(account=account, pid=pid)
    tries = 5
    while result.verdict == Result.Verdict.VERDICT_RUNNING and tries > 0:
        time.sleep(2)
        result = Core(oj).get_result_by_rid_and_pid(rid=result.unique_key, pid=pid)
        tries -= 1

    if result.status == Result.Status.STATUS_RESULT_SUCCESS:
        return str(result.__dict__)
    return result.status.name


def useful():  # TODO
    # for softlink
    print(os.getcwd())
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(os.getcwd())


# ----- TEST -----

def test_submit():
    result = submit(
        oj=OJUtil.short2full("cf"),
        pid="1118A",
        language="54",  # ""GNU G++17 7.3.0",
        account=Account('robot4test', 'robot4test'),
        file_path='dist/Codeforces/1118-C++17/A.cpp',
    )
    print(result)
    print(result['verdict_info'])


if __name__ == '__main__':
    test_submit()
