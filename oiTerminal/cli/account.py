import argparse
import getpass
import logging
from oiTerminal.cli.constant import CIPHER_KEY

from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.enc import AESCipher


def add_parser_account(parser_sub: argparse.ArgumentParser, func_prefix: str) -> None:
  p_account = parser_sub.add_parser('account', help='account help')
  p_account_sub = p_account.add_subparsers(help='sub-command help')

  p_account_list = p_account_sub.add_parser('list', help='list help')
  p_account_list.set_defaults(func=func_prefix+'account.list')

  p_account_new = p_account_sub.add_parser('new', help='new help')
  p_account_new.add_argument('platform', type=str, help='platform')
  p_account_new.add_argument('account', type=str, help='account')
  p_account_new.add_argument('-d', '--default', action="store_true", help='platform')
  p_account_new.set_defaults(func=func_prefix+'account.new')

  p_account_modify = p_account_sub.add_parser('modify', help='modify help')
  p_account_modify.add_argument('platform', type=str, help='platform')
  p_account_modify.add_argument('account', type=str, help='account')
  p_account_modify.add_argument('-p', '--password', action="store_true", help='platform')
  p_account_modify.add_argument('-d', '--default', action="store_true", help='platform')
  p_account_modify.set_defaults(func=func_prefix+'account.modify')

  p_account_delete = p_account_sub.add_parser('delete', help='delete help')
  p_account_delete.add_argument('platform', type=str, help='platform')
  p_account_delete.add_argument('account', type=str, help='account')
  p_account_delete.set_defaults(func=func_prefix+'account.delete')

  # logintest TODO


def account_list(am: AccountManager):
  acc_list = am.get_list()
  for i in range(len(acc_list)):
    if i == 0 or acc_list[i].platform != acc_list[i-1].platform:
      print(acc_list[i].platform)
    mark = ' '
    if acc_list[i].default:
      mark = '*'
    print(f'\t {mark} {acc_list[i].account}')
  if len(acc_list) == 0:
    print("Account List is empty.")


def account(db, args: argparse.Namespace, logger: logging) -> bool:
  logger.debug(args)

  am = AccountManager(db=db, cipher=AESCipher(CIPHER_KEY), logger=logger)
  if args.func == 'list':
    account_list(am)
  elif args.func == 'new':
    password = getpass.getpass("Password:")
    if not am.new(platform=args.platform, account=args.account, password=password, default=args.default):
      logger.info('New Account Failed.')
    else:
      logger.info('Success')
  elif args.func == 'modify':
    password = None
    if args.password:
      password = getpass.getpass("Password:")
    if not am.modify(platform=args.platform, account=args.account, password=password, default=args.default):
      logger.info('Modify Account Failed.')
    else:
      logger.info('Success Modify')
  elif args.func == 'delete':
    if not am.delete(platform=args.platform, account=args.account):
      logger.info("Account not found")
      return False
    else:
      logger.info("Success Delete")
  else:
    return False

  return True


# TODO clear RCPC
