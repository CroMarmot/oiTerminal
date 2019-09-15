#!/usr/bin/python3
import argparse
import json

from const import *
from oiTerminal.core import Core
from oiTerminal.utils import OJUtil

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
        raise Exception(CONFIG_FILE + " NOT EXIST!")
    with open(CONFIG_FILE) as f:
        cfg_oj = json.load(f)[OJUtil.short2full(args.oj)]  # OJUtil
        username = cfg_oj['user']
        password = cfg_oj['pass']

    return OJUtil.short2full(args.oj), args.contest, username, password


def contest_main():
    oj, cid, username, password = reg_contest_parser()

    ret = Core(oj).set_account(Account(username, password)).reg_contest(cid)
    print(ret)


if __name__ == '__main__':
    try:
        contest_main()
    except KeyboardInterrupt:
        print("Interrupt by user")
