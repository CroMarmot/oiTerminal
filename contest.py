#!/usr/bin/python3
import argparse
import shutil
import errno
import json
import traceback
import os

from constant import DIST,TEST_PY,SUBMIT_PY,STATE_FILE,CONFIG_FILE
from oiTerminal.core import Core
from oiTerminal.utils import LanguageUtil, OJUtil, logger

from oiTerminal.Model.Contest import Contest
from oiTerminal.Model.Account import Account
from oiTerminal.Model.FolderState import FolderState


def force_symlink(src: str, dst: str):
    try:
        os.symlink(src, dst)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst)
        else:
            raise e


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


# create folder & testcase
def create_contest_files_and_code_files(
        contest: Contest = None,
        lang: str = '',
        up_lang: str = ''
):
    if contest is None:
        raise Exception('contest is None')

    # generate html & in & out
    folder: str = f"{DIST}/{contest.oj}/{contest.id}/"
    os.makedirs(folder, exist_ok=True)
    for problem_id, problem in contest.problems.items():
        with open(f"{folder}{problem_id}.html", "w") as problem_html:
            problem_html.write(problem.html)
            problem_html.close()
        for i, tc in enumerate(problem.test_cases):
            with open(f"{folder}{problem_id}.in.{i}", "w") as tc_in:
                tc_in.write(tc.in_data)
                tc_in.close()
            with open(f"{folder}{problem_id}.out.{i}", "w") as tc_out:
                tc_out.write(tc.out_data)
                tc_out.close()

    # generate code file by copy template file
    folder: str = f"{DIST}/{contest.oj}/{contest.id}-{lang}/"
    os.makedirs(folder, exist_ok=True)
    suffix = LanguageUtil.lang2suffix(lang)
    template_file = LanguageUtil.lang2template(lang)
    for problem_id in contest.problems.keys():
        dst_filename = f"{folder}{problem_id}{suffix}"
        if os.path.isfile(dst_filename):
            print(f"{dst_filename} Exist")  # DO NOT COVER EXIST CODE
            continue
        if os.path.isfile(template_file):  # if template file exist copy it
            shutil.copy(LanguageUtil.lang2template(lang), dst_filename)
        else:  # create new file
            touch(dst_filename)

    # symlink test.py submit.py
    force_symlink(f"../../../{TEST_PY}", f"{folder}{TEST_PY}")
    force_symlink(f"../../../{SUBMIT_PY}", f"{folder}{SUBMIT_PY}")

    # generate state.json
    folder_state = FolderState(
        oj=contest.oj,
        sid=contest.id,
        lang=lang,
        up_lang=up_lang
    )
    with open(f"{folder}{STATE_FILE}", "w") as statejson:
        json.dump(folder_state.__dict__, statejson)
        statejson.close()

    start_terminal(folder)


def start_terminal(folder: str):
    os.chdir(folder)
    os.system("$SHELL")


# parse parameters
def contest_parser():
    # terminal arg
    parser = argparse.ArgumentParser()
    parser.add_argument('oj', help="example: cf")
    parser.add_argument('contest', help="contest id. Example 1114")
    parser.add_argument(
        '--lang', '-l', help="The programming language you want to use c++17 / c++11 / Java8")
    parser.add_argument(
        '--remotelang', '-r', help="The programming language submit you want to use ")
    args = parser.parse_args()

    # config arg
    # TODO all 2 class
    if not os.path.isfile(CONFIG_FILE):
        raise Exception(f'CONFIG_FILE [{CONFIG_FILE}] NOT EXIST!')
    with open(CONFIG_FILE) as f:
        print(OJUtil.short2full(args.oj))
        oj_full_name = OJUtil.short2full(args.oj)
        cfg_data = json.load(f)
        if oj_full_name not in cfg_data:
            print(f"'{oj_full_name}' not found in `config.json`")
            raise Exception(f"'{oj_full_name}' not found in `config.json`")
        cfg_oj = cfg_data[oj_full_name]  # OJUtil
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
        user_input = input(f"Template file ({template_file}) not find ! Keep going? (Y/N) :")
        if user_input == 'Y' or user_input == 'y' or user_input == '':
            pass
        else:
            exit(0)
    else:
        print(f"Template file found:{template_file}")

    return OJUtil.short2full(args.oj), args.contest, username, password, lang, up_lang


def contest_main():
    oj, cid, username, password, lang, up_lang = contest_parser()

    _contest: Contest = Core(oj).set_account(Account(username, password)).get_contest(cid)
    create_contest_files_and_code_files(_contest, lang, up_lang)


if __name__ == '__main__':
    try:
        contest_main()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
