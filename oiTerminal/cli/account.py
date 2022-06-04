import argparse
import getpass
import logging
from oiTerminal.cli.constant import CIPHER_KEY

from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.enc import AESCipher


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
