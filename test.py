#!/usr/bin/python3
import argparse
import datetime
import json
import os
import shutil

from const import *
from oiTerminal.utils import LanguageUtil


def do_test():
    # get problem id
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help="Problem ID example: A")  # TODO all oj list tool # OJUtil
    args = parser.parse_args()
    pid = args.pid

    # get lang config
    if not os.path.isfile(STATE_FILE):
        raise Exception(STATE_FILE + " NOT EXIST!")
    with open(STATE_FILE) as f:
        state_oj = json.load(f)
        lang = state_oj["lang"]

    # makefolder & mv code 2 folder
    os.makedirs(TEST_FOLDER)
    shutil.copy(pid + LanguageUtil.lang2suffix(lang), TEST_FOLDER + "Main" + LanguageUtil.lang2suffix(lang))

    # compile
    os.chdir(TEST_FOLDER)
    if os.system(LanguageUtil.lang2compile(lang, "Main")) is not 0:
        return

    # run  "" not better than 'time' in bash but worse is better :-)
    i = 0
    std_file = "../../" + state_oj["contestId"] + "/" + pid
    while os.path.isfile(std_file + IN_SUFFIX + str(i)):
        std_out_file = std_file + OUT_SUFFIX + str(i)
        user_out_file = pid + OUT_SUFFIX + str(i)
        start_time = datetime.datetime.now()
        os.system(LanguageUtil.lang2exe(lang, "Main", std_file + IN_SUFFIX + str(i), user_out_file))
        end_time = datetime.datetime.now()
        print()
        print("time spend: " + str((end_time - start_time).total_seconds()) + "s")

        # cmp
        diff = os.system("diff --brief -B --ignore-trailing-space " + std_out_file + " " + user_out_file)
        if diff is not 0:
            os.system("diff -B --ignore-trailing-space -y " + std_out_file + " " + user_out_file)

        i += 1

    os.chdir("../")
    shutil.rmtree(TEST_FOLDER)


if __name__ == "__main__":
    do_test()
