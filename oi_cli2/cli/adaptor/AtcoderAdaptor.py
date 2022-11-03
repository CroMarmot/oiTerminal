from oi_cli2.core.DI import DI_HTTP, DI_LOGGER
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
import oi_cli2.core.provider as provider
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.Provider2 import Provider2


def AtcoderGen(provider: provider, account: Account) -> BaseOj:
  from oi_cli2.custom.AtCoder.AtCoder import AtCoder
  p2 = Provider2()  # TODO receive from args
  http_util = p2.get(DI_HTTP)
  logger= p2.get(DI_LOGGER)
  oj: BaseOj = AtCoder(http_util=http_util,
                       logger=logger,
                       account=account,
                       html_tag=HtmlTag(http_util))
  return oj