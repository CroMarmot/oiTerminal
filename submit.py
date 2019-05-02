#!/usr/bin/python3
import argparse
import json
import time

from const import *
from oiTerminal.model import Account, Result
from oiTerminal.core import Core
from oiTerminal.utils import OJUtil, LanguageUtil


def submit(
        oj: str,
        pid: str,
        language: str,
        account: Account,
        file_path: str,
):
    result: Result = None
    tries = 3
    core = Core(oj)
    while result is None and tries > 0:
        tries -= 1
        print("Submitting...")
        # TODO in submit cookies should be set into account
        result = core.submit_code(pid=pid, account=account, code=file_path, language=language)
        account.set_cookies(core.get_cookies())
    if result.status in [Result.Status.STATUS_SUBMIT_ERROR,
                         Result.Status.STATUS_SPIDER_ERROR,
                         Result.Status.STATUS_SYSTEM_ERROR]:
        return "SUBMIT FAILED"
    print("Submitted")
    while result.verdict == Result.Verdict.VERDICT_RUNNING:
        print("Fetching result...")
        # TODO add percent/cnt
        #      add waiting
        time.sleep(2)
        result = core.get_result_by_rid_and_pid(account=account, pid=pid, unique_key=result.unique_key)

    return result.__dict__


def submit_worker():
    # get problem id
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help="Problem ID example: A")
    args = parser.parse_args()
    pid = args.pid

    # get lang config
    if not os.path.isfile(STATE_FILE):
        raise Exception(STATE_FILE + " NOT EXIST!")
    with open(STATE_FILE) as f:
        state_oj = json.load(f)
        oj = state_oj["oj"]
        contestId = state_oj["contestId"]
        lang = state_oj["lang"]
        up_lang = state_oj["up_lang"]

    config_file = CONFIG_FILE
    if not os.path.isfile(config_file):
        raise Exception(config_file + " NOT EXIST!")
    with open(config_file) as f:
        oj_config = json.load(f)[oj]
        username = oj_config["user"]
        password = oj_config["pass"]

    code_file = os.getcwd() + "/" + pid + LanguageUtil.lang2suffix(lang)
    if not os.path.isfile(code_file):
        raise Exception(code_file + " NOT EXIST!")

    result = submit(
        oj=oj,
        pid=contestId + pid,
        language=up_lang,  # "54",  means ""GNU G++17 7.3.0",
        account=Account(username, password),  # Account('robot4test', 'robot4test'),
        file_path=code_file,  # 'dist/Codeforces/1118-C++17/A.cpp',
    )
    print(result['verdict_info'])
    print(result['execute_time'] + " | " + result['execute_memory'])


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


if __name__ == '__main__':
    submit_worker()
