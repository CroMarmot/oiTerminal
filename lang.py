#!/usr/bin/python3
import argparse

import json
import traceback

from constant import *
from oiTerminal.core import Core
from oiTerminal.Model.Account import Account
from oiTerminal.utils import LanguageUtil, OJUtil, logger


def getUserAndPwd(oj):
    if not os.path.isfile(CONFIG_FILE):
        raise Exception(f'CONFIG_FILE [{CONFIG_FILE}] NOT EXIST!')
    with open(CONFIG_FILE) as f:
        oj_config = json.load(f)[oj]
        username = oj_config['user']
        password = oj_config['pass']

    return username, password


def lang_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--oj', help="example: cf , display key-value in remote server")
    args = parser.parse_args()
    oj_full_name: str = None
    if args.oj is None:
        print("Local Language supported : ", LanguageUtil.local_lang())
        return
    elif OJUtil.short2full(args.oj) is not None:
        oj_full_name = OJUtil.short2full(args.oj)
    elif args.oj in OJUtil.get_supports():
        oj_full_name = args.oj

    username, pwd = getUserAndPwd(OJUtil.short2full(args.oj))

    if oj_full_name is None:
        raise Exception("oj name error! Supported oj:", OJUtil.get_supports())
    lang_kv_pair = Core(oj_full_name).set_account(Account(username, pwd)).get_language()
    for (k, v) in lang_kv_pair.items():
        print(k + "\t" + v)


if __name__ == '__main__':
    try:
        lang_main()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
