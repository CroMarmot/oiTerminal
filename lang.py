#!/usr/bin/python3
import argparse

from oiTerminal.core import Core
from oiTerminal.Model.Account import Account
from oiTerminal.utils import LanguageUtil, OJUtil


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

    if oj_full_name is not None:
        lang_kv_pair = Core(oj_full_name).set_account(Account('robot4test', 'robot4test')).get_language()
        for (k, v) in lang_kv_pair.items():
            print(k + "\t" + v)
    else:
        print("oj name error! Supported oj:", OJUtil.get_supports())


if __name__ == '__main__':
    lang_main()
