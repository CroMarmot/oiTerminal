from collections import namedtuple
from oi_cli2.cli.account import valid_account
from oi_cli2.core.DI import DI_PROVIDER


def test_valid_account():

  ctx = namedtuple("obj", {})
  # ctx.obj[DI_PROVIDER] = fake provider

  # valid_account(ctx, platform: str, account: str) -> bool:

  # provider = ctx.obj[DI_PROVIDER]
  # logger: logging.Logger = provider.o.get(DI_LOGGER)
  # am: AccountManager = provider.o.get(DI_ACCMAN)
  # http_util: HttpUtil = provider.o.get(DI_HTTP)
  # acc = am.get_account(platform=platform, account=account)
  # if acc is None:
  #   logger.error(f'Account [{account}] not found')
  #   return False

  # try:
  #   oj: BaseOj = OJManager.createOj(platform=platform,account=acc,provider=provider)
  # except Exception as e:
  #   logger.exception(e)
  #   raise e
  # oj.login_website()
