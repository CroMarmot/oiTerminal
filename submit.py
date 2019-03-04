import time

from oiTerminal.model import Account
from oiTerminal.model import Problem, Result
from oiTerminal.core import Core


def submit(
        oj_name: str,
        problem: Problem,
        language: str,
        account: Account,
        file: file,
):
    source_code = get_code_from_file()
    ans = False
    tries = 3
    while ans is False and tries > 0:
        tries -= 1
        core = Core(str(remote_oj))
        ans = core.submit_code(pid=remote_id, account=account, code=source_code.read(), language=language)
        account.set_cookies(core.get_cookies())
    if ans.status in [Result.Status.STATUS_SUBMIT_ERROR, Result.Status.STATUS_SPIDER_ERROR,
                      Result.Status.STATUS_SYSTEM_ERROR]:
        return "SUBMIT FAILED"
    core = Core(remote_oj)
    result = core.get_result(account=account, pid=remote_id)
    account.set_cookies(core.get_cookies())
    tries = 5
    while result.verdict == Result.Verdict.VERDICT_RUNNING and tries > 0:
        time.sleep(2)
        result = Core(remote_oj).get_result_by_rid_and_pid(rid=result.unique_key, pid=remote_id)
        tries -= 1

    if result.status == Result.Status.STATUS_RESULT_SUCCESS:
        return str(result.__dict__)
    return result.status.name
