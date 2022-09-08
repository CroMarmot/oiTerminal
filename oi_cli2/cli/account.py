import click
import getpass
import logging

from oi_cli2.cli.adaptor.ojman import OJManager
from oi_cli2.core.DI import DI_ACCMAN, DI_HTTP, DI_LOGGER, DI_PROVIDER
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.account import AccountManager


@click.group()
@click.pass_context
def account(ctx):
  """Manage accounts"""
  import oi_cli2.core.provider as provider
  ctx.obj[DI_PROVIDER] = provider


@account.command(name='list')
@click.pass_context
def list_command(ctx):
  """List all account"""
  provider = ctx.obj[DI_PROVIDER]
  am: AccountManager = provider.o.get(DI_ACCMAN)
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
  provider = ctx.obj[DI_PROVIDER]
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  am: AccountManager = provider.o.get(DI_ACCMAN)
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
  provider = ctx.obj[DI_PROVIDER]
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  am: AccountManager = provider.o.get(DI_ACCMAN)
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
  provider = ctx.obj[DI_PROVIDER]
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  am: AccountManager = provider.o.get(DI_ACCMAN)
  if not am.delete(platform=platform, account=account):
    logger.error("Account not found")
    return False
  else:
    logger.info("Success Delete")
  return True


@account.command(name="test")
@click.argument("platform")
@click.argument("account")
@click.pass_context
def valid_account(ctx, platform: str, account: str) -> bool:
  """Test account login

  PLATFORM    Platform Name, (AtCoder,Codeforces)

  ACCOUNT     Account name
  """
  provider = ctx.obj[DI_PROVIDER]
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  am: AccountManager = provider.o.get(DI_ACCMAN)
  http_util: HttpUtil = provider.o.get(DI_HTTP)
  acc = am.get_account(platform=platform, account=account)
  if acc is None:
    logger.error(f'Account [{account}] not found')
    return False

  try:
    oj: BaseOj = OJManager.createOj(platform=platform,account=acc,provider=provider)
  except Exception as e:
    logger.exception(e)
    raise e
  oj.login_website(force=True)
  return True
