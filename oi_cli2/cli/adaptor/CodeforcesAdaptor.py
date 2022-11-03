from oi_cli2.core.DI import DI_HTTP, DI_LOGGER
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.Provider2 import Provider2


def CodeforcesGen(account:Account,provider: Provider2) -> BaseOj:
  from oi_cli2.custom.Codeforces.Codeforces import Codeforces
  http_util = provider.get(DI_HTTP)
  oj: BaseOj = Codeforces(http_util=http_util,
                          logger=provider.get(DI_LOGGER),
                          account=account,
                          html_tag=HtmlTag(http_util))

  return oj