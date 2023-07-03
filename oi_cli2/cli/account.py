import click
import getpass
import logging
from rich.console import Console

from oi_cli2.cli.adaptor.ojman import OJManager
from oi_cli2.core.DI import DI_ACCMAN, DI_LOGGER, DI_PROVIDER
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.account import AccountManager

console = Console(color_system='256', style=None)


@click.group()
@click.pass_context
def account(ctx):
  """Manage accounts"""
  from oi_cli2.utils.Provider2 import Provider2
  ctx.obj[DI_PROVIDER] = Provider2()


@account.command(name='list')
@click.pass_context
def list_command(ctx) -> None:
  """List all account"""
  provider = ctx.obj[DI_PROVIDER]
  am: AccountManager = provider.get(DI_ACCMAN)
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
def new(ctx, platform, account, default_) -> None:
  """Create new account


  PLATFORM    Platform Name, (AtCoder,Codeforces)

  ACCOUNT     Account name
  """
  provider = ctx.obj[DI_PROVIDER]
  logger: logging.Logger = provider.get(DI_LOGGER)
  am: AccountManager = provider.get(DI_ACCMAN)
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
  logger: logging.Logger = provider.get(DI_LOGGER)
  am: AccountManager = provider.get(DI_ACCMAN)
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
  logger: logging.Logger = provider.get(DI_LOGGER)
  am: AccountManager = provider.get(DI_ACCMAN)
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
  logger: logging.Logger = provider.get(DI_LOGGER)
  logger.debug(f'platform:{platform}')
  am: AccountManager = provider.get(DI_ACCMAN)
  acc = am.get_account(platform=platform, account=account)
  if acc is None:
    console.print(f'[red bold]Account [{account}] not found')
    return False

  try:
    oj: BaseOj = OJManager.createOj(platform=platform, account=acc, provider=provider)
  except Exception as e:
    logger.exception(e)
    raise e
  console.print(f"[green bold]{platform} Logging with {acc.account} ...")
  ok = oj.login_website(force=True)
  if ok:
    console.print(f"[green bold]Successful login.")
  else:
    console.print(f"[red bold]Login failed.")
  return ok
