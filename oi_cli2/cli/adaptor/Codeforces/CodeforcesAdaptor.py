from oi_cli2.core.DI import DI_CFG, DI_LOGGER
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.configFolder import ConfigFolder


def CodeforcesGen(account: Account, provider: Provider2) -> BaseOj:
  from oi_cli2.cli.adaptor.Codeforces.Codeforces import Codeforces
  from codeforces_core.httphelper import HttpHelper
  config_folder: ConfigFolder = provider.get(DI_CFG)
  cookie_jar_path = config_folder.get_config_file_path(account.platform + '_' + account.account + '_cookies')
  # token_path = config_folder.get_config_file_path(account.platform + '_' + account.account + '_tokens')
  http = HttpHelper(token_path='', cookie_jar_path=cookie_jar_path)
  oj: BaseOj = Codeforces(http_util=http, logger=provider.get(DI_LOGGER), account=account)

  return oj
