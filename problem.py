#!/usr/bin/python3
import argparse
import shutil
import errno
import json
import traceback

from constant import *
from oiTerminal.core import Core
from oiTerminal.utils import LanguageUtil, OJUtil, logger

from oiTerminal.Model.Contest import Contest
from oiTerminal.Model.Account import Account
from oiTerminal.Model.Problem import Problem
from oiTerminal.Model.FolderState import FolderState

# TODO contest.py & problem.py merge function


def force_symlink(src: str, dst: str):
    try:
        os.symlink(src, dst)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst)


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def get_problem(oj: str, pid: str, account: Account) -> Problem:
    _problem = Core(oj).get_problem(pid=pid, account=account)
    return _problem


def create_problem_files(problem: Problem = None):
    if problem is None:
        raise Exception('problem is None')
    folder: str = DIST + "/" + problem.oj + "/" + problem.id + "/"
    os.makedirs(folder, exist_ok=True)
    # generate html & in & out
    with open(folder + problem_id + '.html', "w") as problem_html:
        problem_html.write(problem.html)
        problem_html.close()
    for i, tc in range(len(problem.test_cases)):
        with open(folder + problem_id + '.in.' + str(i), "w") as tc_in:
            tc_in.write(tc.in_data)
            tc_in.close()
        with open(folder + problem_id + '.out.' + str(i), "w") as tc_out:
            tc_out.write(tc.out_data)
            tc_out.close()


def create_problem_code_file(
        contest: Contest,  # contest
        lang: str,  # language
        up_lang: str  # submit lang
):
    if contest is None:
        raise Exception('contest is None')
    folder = DIST + "/" + contest.oj + "/" + contest.id + '-' + lang + "/"
    os.makedirs(folder, exist_ok=True)
    suffix = LanguageUtil.lang2suffix(lang)
    template_file = LanguageUtil.lang2template(lang)
    for problem_id in contest.problems.keys():
        dst_filename = folder + problem_id + suffix
        if os.path.isfile(dst_filename):
            print(dst_filename + " Exist")  # DO NOT COVER EXIST CODE
            continue
        if os.path.isfile(template_file):  # if template file exist copy it
            shutil.copy(LanguageUtil.lang2template(lang), dst_filename)
        else:  # create new file
            touch(dst_filename)

    force_symlink('../../../' + TEST_PY, folder + TEST_PY)
    force_symlink('../../../' + SUBMIT_PY, folder + SUBMIT_PY)

    folder_state = FolderState(
        oj=contest.oj,
        sid=contest.id,
        lang=lang,
        up_lang=up_lang
    )
    with open(folder + STATE_FILE, "w") as statejson:
        json.dump(folder_state.__dict__, statejson)
        statejson.close()

    start_terminal(folder)


def start_terminal(folder: str):
    os.chdir(folder)
    os.system("$SHELL")


# parse parameters
def problem_parser():
    # terminal arg
    parser = argparse.ArgumentParser()
    parser.add_argument('oj', help="example: cf")
    parser.add_argument('problem', help="problem id. Example 1114A")
    parser.add_argument(
        '--lang', '-l', help="The programming language you want to use c++17 / c++11 / Java8")
    parser.add_argument(
        '--remotelang', '-r', help="The programming language submit you want to use ")
    args = parser.parse_args()

    # config arg
    if not os.path.isfile(CONFIG_FILE):
        raise Exception(f'CONFIG_FILE {CONFIG_FILE} NOT EXIST!')
    with open(CONFIG_FILE) as f:
        cfg_oj = json.load(f)[OJUtil.short2full(args.oj)]  # OJUtil
        lang = cfg_oj['lang']
        up_lang = cfg_oj['up_lang']
        username = cfg_oj['user']
        password = cfg_oj['pass']

    # terminal args > config arg
    if args.lang is not None:
        lang = args.lang
    if args.remotelang is not None:
        up_lang = args.remotelang

    # check if template file exist?
    template_file = LanguageUtil.lang2template(lang)
    if not os.path.isfile(template_file):
        user_input = input("Template file (" + template_file + ") not find ! Keep going? (Y/N) :")
        if user_input == 'Y' or user_input == 'y' or user_input == '':
            pass
        else:
            exit(0)
    else:
        raise FileExistsError('Template file found:' + template_file)

    return OJUtil.short2full(args.oj), args.problem, username, password, lang, up_lang


def problem_main():
    oj, pid, username, password, lang, up_lang = problem_parser()

    _problem = get_problem(
        oj=oj,
        pid=pid,
        account=Account(username, password))
    create_problem_files(_problem)
    create_problem_code_file(_problem, lang, up_lang)


if __name__ == '__main__':
    try:
        problem_main()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
