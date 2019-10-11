#!/usr/bin/python3
import argparse
import json
import time
import traceback

from constant import *
from oiTerminal.Model.FolderState import FolderState
from oiTerminal.core import Core
from oiTerminal.utils import OJUtil, LanguageUtil, logger

from oiTerminal.Model.Account import Account
from oiTerminal.Model.Result import Result


def submit(
        oj: str,
        pid: str,
        language: str,
        account: Account,
        file_path: str,
) -> Result:
    core = Core(oj).set_account(account)
    if not core.submit_code(pid=pid, language=language, code=file_path):
        raise Exception(f'submit failed,account={account.username}')
    print(GREEN + 'Submitted' + DEFAULT)

    result = Result(Result.Status.PENDING)
    while result.cur_status in [Result.Status.RUNNING, Result.Status.PENDING]:
        print('Fetching result...(' + result.state_note + ')')
        time.sleep(FETCH_RESULT_INTERVAL)
        if result.quick_key is not '':
            result = core.get_result_by_quick_id(result.quick_key)
        else:
            result = core.get_result(pid)
    return result


# TODO design for  single problem and contest
def submit_parser():
    # get problem id
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help='Problem ID example: A')
    args = parser.parse_args()
    pid = args.pid

    # get lang config
    if not os.path.isfile(STATE_FILE):
        raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')
    state_oj = FolderState()
    with open(STATE_FILE) as f:
        state_oj.__dict__ = json.load(f)

    oj = state_oj.oj
    lang = state_oj.lang
    up_lang = state_oj.up_lang

    if not os.path.isfile(CONFIG_FILE):
        raise Exception(f'CONFIG_FILE [{CONFIG_FILE}] NOT EXIST!')
    with open(CONFIG_FILE) as f:
        oj_config = json.load(f)[oj]
        username = oj_config['user']
        password = oj_config['pass']

    code_file = os.getcwd() + '/' + pid + LanguageUtil.lang2suffix(lang)
    if not os.path.isfile(code_file):
        raise Exception(f'code_file [{code_file}] NOT EXIST!')

    return oj, state_oj.id + pid, up_lang, username, password, code_file


# ----- TEST -----

def test_submit():
    result = submit(
        oj=OJUtil.short2full('cf'),
        pid='1118A',
        language='54',  # ''GNU G++17 7.3.0',
        account=Account('robot4test', 'robot4test'),
        file_path='dist/Codeforces/1118-C++17/A.cpp',
    )
    print(result)


def submit_main():
    oj, pid, up_lang, username, password, code_path = submit_parser()
    _result = submit(
        oj=oj,
        pid=pid,
        language=up_lang,
        account=Account(username, password),
        file_path=code_path,
    )
    print('SUBMIT[' + str(_result.id) + ']:' + _result.status_string)
    print(_result.time_note + ' | ' + _result.mem_note)


if __name__ == '__main__':
    try:
        submit_main()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
