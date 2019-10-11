#!/usr/bin/python3
import argparse
import json
import traceback

from constant import *
from oiTerminal.core import Core
from oiTerminal.utils import OJUtil, logger

from oiTerminal.Model.Account import Account


# parse parameters
def reg_contest_parser():
    # terminal arg
    parser = argparse.ArgumentParser()
    parser.add_argument('oj', help="example: cf")
    parser.add_argument('contest', help="contest id. Example 1114")
    args = parser.parse_args()

    # config arg
    # TODO all 2 class
    if not os.path.isfile(CONFIG_FILE):
        raise Exception(f'CONFIG_FILE [{CONFIG_FILE}] NOT EXIST!')
    with open(CONFIG_FILE) as f:
        cfg_oj = json.load(f)[OJUtil.short2full(args.oj)]  # OJUtil
        username = cfg_oj['user']
        password = cfg_oj['pass']

    return OJUtil.short2full(args.oj), args.contest, username, password


def reg_main():
    logger.info(f'reg start')
    oj, cid, username, password = reg_contest_parser()
    logger.info(f'reg oj={oj},cid={cid},username={username}')

    ret = Core(oj).set_account(Account(username, password)).reg_contest(cid)
    logger.info(f'reg result:{ret}')

    if ret:
        print('reg success')
    else:
        print('reg failed')


if __name__ == '__main__':
    try:
        reg_main()
    except KeyboardInterrupt:
        print("Interrupt by user")
    except Exception as e:
        print(e)
        logger.error(traceback.format_exc())
