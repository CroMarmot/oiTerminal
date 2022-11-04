from oi_cli2.core.DI import DI_HTTP, DI_LOGGER
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.Provider2 import Provider2


def AtcoderGen(account: Account, provider: Provider2) -> BaseOj:
  from oi_cli2.custom.AtCoder.AtCoder import AtCoder
  http_util = provider.get(DI_HTTP)
  logger = provider.get(DI_LOGGER)
  oj: BaseOj = AtCoder(http_util=http_util, logger=logger, account=account, html_tag=HtmlTag(http_util))
  return oj
