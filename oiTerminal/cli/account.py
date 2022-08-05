import click
import getpass
import logging

from oiTerminal.core.DI import DI_ACCMAN, DI_DB, DI_LOGGER
from oiTerminal.cli.constant import CIPHER_KEY
from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.enc import AESCipher


@click.group()
@click.pass_context
def account(ctx):
  """Manage accounts"""
  ctx.obj[DI_ACCMAN] = AccountManager(db=ctx.obj[DI_DB], cipher=AESCipher(CIPHER_KEY), logger=ctx.obj[DI_LOGGER])


@account.command(name='list')
@click.pass_context
def list_command(ctx):
  """List all account"""
  am: AccountManager = ctx.obj[DI_ACCMAN]
  acc_list = am.get_list()
  for i in range(len(acc_list)):
    if i == 0 or acc_list[i].platform != acc_list[i - 1].platform:
      print(acc_list[i].platform)
    mark = ' '
    if acc_list[i].default:
      mark = '*'
    print(f'  {mark} {acc_list[i].account}')
  if len(acc_list) == 0:
    print("Account List is empty.")


@account.command()
@click.argument("platform")
@click.argument("account")
@click.option("-d", "--default", "default_", is_flag=True, help='Set account as default account in the oj platform.')
@click.pass_context
def new(ctx, platform, account, default_):
  """Create new account
  
  PLATFORM    Platform Name, (AtCoder,Codeforces)

  ACCOUNT     Account name
  """
  am: AccountManager = ctx.obj[DI_ACCMAN]
  logger: logging.Logger = ctx.obj[DI_LOGGER]
  password = getpass.getpass("Password:")
  if not am.new(platform=platform, account=account, password=password, default=default_):
    logger.error('New Account Failed.')
  else:
    logger.info('Success')

  # TODO support password in arg???


@account.command()
@click.argument("platform")
@click.argument("account")
@click.option("-p", "--password", "changepassword", is_flag=True, help='Change account password.')
@click.option("-d", "--default", "default_", is_flag=True, help='Set account as default account in the oj platform.')
@click.pass_context
def modify(ctx, platform, account, changepassword: bool, default_):
  """Modify a specific account default status or change password

  PLATFORM    Platform Name, (AtCoder,Codeforces)

  ACCOUNT     Account name
  """
  am: AccountManager = ctx.obj[DI_ACCMAN]
  logger: logging.Logger = ctx.obj[DI_LOGGER]
  if changepassword:
    password = getpass.getpass("Password:")
  else:
    password = None

  if not am.modify(platform=platform, account=account, password=password, default=default_):
    logger.error('Modify Account Failed.')
  else:
    logger.info('Success Modify')


@account.command()
@click.argument("platform")
@click.argument("account")
@click.pass_context
def delete(ctx, platform, account) -> bool:
  """Delete a specific account

  PLATFORM    Platform Name, (AtCoder,Codeforces)

  ACCOUNT     Account name
  """
  am: AccountManager = ctx.obj[DI_ACCMAN]
  logger: logging.Logger = ctx.obj[DI_LOGGER]
  if not am.delete(platform=platform, account=account):
    logger.error("Account not found")
    return False
  else:
    logger.info("Success Delete")
