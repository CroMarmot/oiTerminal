import logging
from oi_cli2.cli.constant import CIPHER_KEY, OT_FOLDER
from oi_cli2.custom.Codeforces.CodeforcesParser import CodeforcesParser
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.HttpUtilCookiesHelper import HttpUtilCookiesHelper
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.enc import AESCipher

from ac_core.auth import fetch_login, is_logged_in
from ac_core.contest import parse_tasks


class AtCoder(BaseOj):

  def __init__(self, http_util: HttpUtil, logger: logging.Logger, account: Account,
               html_tag: object) -> None:
    super().__init__()
    assert (account is not None)
    self._base_url = 'https://atcoder.jp/'
    self.logger: logging.Logger = logger
    self.html_tag = html_tag
    self.account: Account = account
    self.http_util = http_util
    self.parser = CodeforcesParser(html_tag=html_tag, logger=logger)
    config_folder = ConfigFolder(OT_FOLDER)
    HttpUtilCookiesHelper.load_cookie(provider=Provider2(),
                                      platform=AtCoder.__name__,
                                      account=account.account)

  def login_website(self, force: bool = False) -> bool:
    if force or not is_logged_in(self.http_util):  # need login
      ok = fetch_login(self.http_util, self.account.account,
                       AESCipher(CIPHER_KEY).decrypt(self.account.password))
      if ok:
        HttpUtilCookiesHelper.save_cookie(provider=Provider2(),
                                          platform=AtCoder.__name__,
                                          account=self.account.account)
      return ok
    return True
