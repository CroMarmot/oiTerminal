from oi_cli2.core.DI import DI_HTTP, DI_LOGGER
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
import oi_cli2.core.provider as provider
from oi_cli2.utils.HtmlTag import HtmlTag


def CodeforcesGen(provider: provider, account: Account) -> BaseOj:
  from oi_cli2.custom.Codeforces.Codeforces import Codeforces
  http_util = provider.o.get(DI_HTTP)
  oj: BaseOj = Codeforces(http_util=http_util,
                          logger=provider.o.get(DI_LOGGER),
                          account=account,
                          html_tag=HtmlTag(http_util))

  return oj