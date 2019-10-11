#!/usr/bin/python3
import argparse
import datetime
import json
import shutil
import traceback

from constant import *
from oiTerminal.Model.FolderState import FolderState
from oiTerminal.utils import LanguageUtil, logger


def do_test():
    logger.info("[test] start root path:" + ROOT_PATH)
    # get problem id
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help="Problem ID example: A")
    args = parser.parse_args()
    pid = args.pid

    # get lang config
    if not os.path.isfile(STATE_FILE):
        raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')

    state_oj = FolderState()
    with open(STATE_FILE) as f:
        state_oj.__dict__ = json.load(f)
    lang = state_oj.lang

    # makefolder & mv code 2 folder
    os.makedirs(TEST_FOLDER, exist_ok=True)
    source_file_name = pid + LanguageUtil.lang2suffix(lang)
    logger.info("test source code:" + source_file_name)
    if not os.path.exists(source_file_name):
        raise FileNotFoundError(f"'{source_file_name}' not found!")
    shutil.copy(source_file_name, TEST_FOLDER + "Main" + LanguageUtil.lang2suffix(lang))

    # compile
    os.chdir(TEST_FOLDER)
    if os.system(LanguageUtil.lang2compile(lang)) is not 0:
        return

    # run  "" not better than 'time' in bash but worse is better :-)
    i = 0
    std_file = "../../" + state_oj.id + "/" + pid
    while os.path.isfile(std_file + IN_SUFFIX + str(i)):
        std_in_file = std_file + IN_SUFFIX + str(i)
        std_out_file = std_file + OUT_SUFFIX + str(i)
        user_out_file = pid + OUT_SUFFIX + str(i)
        start_time = datetime.datetime.now()
        os.system(LanguageUtil.lang2exe(lang, std_in_file, user_out_file))
        end_time = datetime.datetime.now()
        logger.info("test std in file:" + std_in_file)
        logger.info("test std out file:" + std_out_file)
        print()
        # TODO COMPARE TIME
        print("Time spend: " + GREEN + str((end_time - start_time).total_seconds()) + "s" + DEFAULT)

        # cmp output
        diff = os.system("diff --brief -B --ignore-trailing-space " + std_out_file + " " + user_out_file)
        if diff is not 0:
            print(RED)
            print("==============================================================================")
            os.system("cat " + std_in_file)
            print("\n-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -")
            os.system("diff -B --ignore-trailing-space -y " + std_out_file + " " + user_out_file)
            print("\n==============================================================================")
            print(DEFAULT)

        i += 1

    os.chdir("../")
    # shutil.rmtree(TEST_FOLDER)
    logger.info('test finished')


if __name__ == "__main__":
    try:
        do_test()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
