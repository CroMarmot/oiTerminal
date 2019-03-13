#!/usr/bin/python3
import argparse

from oiTerminal.core import Core
from oiTerminal.model import Account
from oiTerminal.utils import LanguageUtil, OJUtil


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--oj', help="example: cf , display key-value in remote server")
    args = parser.parse_args()
    oj_full_name: str = None
    if args.oj is None:
        print("Local Language supported : ", LanguageUtil.local_lang())
        return
    elif OJUtil.short2full(args.oj) is not None:
        oj_full_name = OJUtil.short2full(args.oj)
    elif Core.is_support(args.oj):
        oj_full_name = args.oj

    if oj_full_name is not None:
        lang_kv_pair: dict = Core(oj_full_name).find_language(account=Account('robot4test', 'robot4test'))
        for (k, v) in lang_kv_pair.items():
            print(k + "\t" + v)
    else:
        print("oj name error! Supported oj:", OJUtil.get_supports())


if __name__ == '__main__':
    parser()
