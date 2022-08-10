#!/usr/bin/python3
import argparse
import datetime
import json
import shutil
import traceback
import os

from constant import ROOT_PATH,STATE_FILE,TEST_FOLDER,IN_SUFFIX,OUT_SUFFIX,GREEN,RED,DEFAULT
from oiTerminal.Model.FolderState import FolderState
from oiTerminal.utils import LanguageUtil, logger

# mac os 的命令似乎不支持 --ignore-trailing-space
diff_cmd="diff --brief -B --ignore-trailing-space" # 用于比较
show_diff_cmd="diff -B --ignore-trailing-space -y" # 用于展示差异

def do_test():
    logger.info(f"[test] start root path:{ROOT_PATH}")
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
    source_file_name = f"{pid}{LanguageUtil.lang2suffix(lang)}"
    logger.info(f"test source code:{source_file_name}")
    if not os.path.exists(source_file_name):
        raise FileNotFoundError(f"'{source_file_name}' not found!")
    shutil.copy(source_file_name, f"{TEST_FOLDER}Main{LanguageUtil.lang2suffix(lang)}")

    # compile
    os.chdir(TEST_FOLDER)
    if os.system(LanguageUtil.lang2compile(lang)) != 0:
        return

    std_folder = f"../../{state_oj.id}/"
    files = os.listdir(std_folder)
    test_in_out = []
    for f_in in files:
        if not os.path.isfile(os.path.join(std_folder, f_in)):
            continue
        if f_in.startswith(f"{pid}{IN_SUFFIX}"):
            f_out = f"{pid}{OUT_SUFFIX}" + f_in[len(f"{pid}{IN_SUFFIX}"):]
            if not os.path.isfile(os.path.join(std_folder, f_out)):
                print(f"File out [ {f_out} ] Not Found")
                continue
            test_in_out.append((f_in, f_out))
    # run  "" not better than 'time' in bash but worse is better :-)
    for f_in, f_out in test_in_out:
        std_in_file = os.path.join(std_folder, f_in)
        std_out_file = os.path.join(std_folder, f_out)
        user_out_file = os.path.join(f"user_{f_out}")  # 在当前文件夹输出
        start_time = datetime.datetime.now()
        r = os.system(LanguageUtil.lang2exe(lang, std_in_file, user_out_file))
        print("r:"+str(r))
        end_time = datetime.datetime.now()
        logger.info(f"test std in file:{std_in_file}")
        logger.info(f"test std out file:{std_out_file}")
        print()
        # TODO COMPARE TIME
        print(f"TestCase {f_in} => {f_out} Time spend: {GREEN}{(end_time - start_time).total_seconds()}s{DEFAULT}")

        # cmp output
        diff = os.system(f"{diff_cmd} {std_out_file} {user_out_file}")
        if diff != 0:
            print(RED)
            print("==============================================================================")
            os.system(f"cat {std_in_file}")
            print("\n-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -")
            os.system(f"{show_diff_cmd} {std_out_file} {user_out_file}")
            print("\n==============================================================================")
            print(DEFAULT)

    os.chdir("../")
    # shutil.rmtree(TEST_FOLDER)
    logger.info('Test finished')


if __name__ == "__main__":
    try:
        do_test()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
