#!/usr/bin/python3
import argparse
import shutil
import errno
import os
import json

from const import *
from oiTerminal.core import Core
from oiTerminal.model import Account, Problem, Contest, TestCase
from oiTerminal.utils import LanguageUtil, OJUtil


def force_symlink(src: str, dst: str):
    try:
        os.symlink(src, dst)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst)


def get_problem(oj: str, pid: str, account: Account):
    _problem = Core(oj).get_problem(pid=pid, account=account)
    return _problem


def get_contest(oj: str, cid: str, account: Account):
    _oj = Core(oj)
    if not _oj.is_support_contest():
        return None
    return _oj.get_contest(cid, account=account)


def create_contest_files(contest: Contest = None):
    if contest is None:
        print("contest is None")
        return
    folder = DIST + "/" + contest.oj + "/" + contest.id + "/"
    os.makedirs(folder, exist_ok=True)  # TODO rm exist ok = true
    for problem_id, problem_detail in contest.problem_set.items():
        pd: Problem = problem_detail
        with open(folder + problem_id + '.html', "w") as problem_html:
            problem_html.write(pd.html)
            problem_html.close()
        for i in range(len(pd.test_case)):
            tc: TestCase = pd.test_case[i]
            with open(folder + problem_id + '.in.' + str(i), "w") as tc_in:
                tc_in.write(tc.sample_in)
                tc_in.close()
            with open(folder + problem_id + '.out.' + str(i), "w") as tc_out:
                tc_out.write(tc.sample_out)
                tc_out.close()


def create_contest_code_file(
        contest: Contest,  # contest
        lang: str,  # language
        up_lang: str  # submit lang
):
    if contest is None:
        print("contest is None")
        return
    folder = DIST + "/" + contest.oj + "/" + contest.id + '-' + lang + "/"
    os.makedirs(folder, exist_ok=True)  # TODO rm exist ok = true

    suffix = LanguageUtil.lang2suffix(lang)

    for problem_id in contest.problem_set.keys():
        shutil.copy(LanguageUtil.lang2template(lang), folder + problem_id + suffix)

    # soft link test.py && submit.py
    force_symlink('../../../' + TEST_PY, folder + TEST_PY)
    force_symlink('../../../' + SUBMIT_PY, folder + SUBMIT_PY)

    contest_state = {
        "oj": contest.oj,
        "contestId": contest.id,
        "lang": lang,
        "up_lang": up_lang,
    }
    with open(folder + STATE_FILE, "w") as statejson:
        json.dump(contest_state, statejson)
        statejson.close()

    start_terminal(folder)


def start_terminal(folder: str):
    os.chdir(folder)
    os.system("$SHELL")


# ret.
# oj full name :                        eg. Codeforces
# contestID                             eg. 1118
# username                              eg. robot4test
# password                              eg. robot4test
# cfg_lang for local template / test,   eg. lang
# cfg_uplang for submit,                eg. 54
#
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('oj', help="example: cf")  # TODO all oj list tool # OJUtil
    parser.add_argument('contest', help="contest id. Example 1114")
    parser.add_argument(
        '--lang', '-l', help="The programming language you want to use c++17 / c++11 / Java8")
    parser.add_argument(
        '--remotelang', '-r', help="The programming language submit you want to use ")
    args = parser.parse_args()

    if not os.path.isfile(CONFIG_FILE):
        raise Exception(CONFIG_FILE + " NOT EXIST!")
    with open(CONFIG_FILE) as f:
        cfg_oj = json.load(f)[OJUtil.short2full(args.oj)]
        lang = cfg_oj['lang']
        up_lang = cfg_oj['up_lang']
        username = cfg_oj['user']
        password = cfg_oj['pass']
    # args > cfg
    if args.lang is not None:
        lang = args.lang
    if args.remotelang is not None:
        up_lang = args.remotelang
    return OJUtil.short2full(args.oj), args.contest, username, password, lang, up_lang


# ----- TEST -----

def test_contest():
    _contest = get_contest(
        oj=OJUtil.short2full("cf"),
        cid='1118',
        account=Account('robot4test', 'robot4test'))
    print(vars(_contest))
    create_contest_files(_contest)
    create_contest_code_file(_contest, "C++14", "54")


def test_problem():
    _problem = get_problem(
        oj=OJUtil.short2full("cf"),
        cid='1118',
        account=Account('robot4test', 'robot4test'))
    print(vars(_problem))


def test_parser():
    oj, cid, user, password, lang, up_lang = parser()
    _contest = get_contest(
        oj=oj,
        cid=cid,
        account=Account(user, password))
    create_contest_files(_contest)
    create_contest_code_file(_contest, lang, up_lang)


if __name__ == '__main__':
    test_parser()
