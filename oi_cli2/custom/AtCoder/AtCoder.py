import logging
from typing import List
from rich.console import Console

from oi_cli2.cli.constant import CIPHER_KEY, OT_FOLDER
from oi_cli2.custom.Codeforces.CodeforcesParser import CodeforcesParser
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.model.ProblemMeta import ContestMeta, ProblemMeta
from oi_cli2.model.TestCase import TestCase
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.HttpUtilCookiesHelper import HttpUtilCookiesHelper
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.enc import AESCipher

from ac_core.auth import fetch_login, is_logged_in
from ac_core.contest import fetch_tasks_meta, FetchProblemResult
from ac_core.problem import parse_task

console = Console(color_system='256', style=None)


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

  def get_contest_meta(self, cid: str) -> ContestMeta:
    self.login_website()
    res = fetch_tasks_meta(self.http_util, cid)

    def transform(pm: FetchProblemResult) -> ProblemMeta:
      return ProblemMeta(id=pm.id,
                         url=pm.url,
                         name=pm.name,
                         contest_id=cid,
                         memory_limit_kb=pm.memory_limit_kb,
                         time_limit_msec=pm.time_limit_msec)

    return ContestMeta(id=cid, url=res.url, problems=[transform(pm) for pm in res.problems])

  # Care !! in Atcoder may arc058 C = https://atcoder.jp/contests/arc058/tasks/arc058_a
  def problem(self, pm: ProblemMeta) -> ParseProblemResult:
    html = self.http_util.get(pm.url).text
    res = parse_task(html=html)
    return ParseProblemResult(
        # status=: Status = Status.NOTVI STODO
        id=res.id,
        title=pm.name,
        test_cases=[TestCase(in_data=o.input, out_data=o.output) for o in res.tests],
        oj=AtCoder.__name__,
        # description=res.id,
        time_limit=pm.time_limit_msec,
        mem_limit=pm.memory_limit_kb,
        url=res.url,
    )
