import logging
from typing import List
from rich.console import Console
from rich.table import Table
from rich.style import Style

from oi_cli2.cli.constant import CIPHER_KEY, OT_FOLDER
from oi_cli2.custom.Codeforces.CodeforcesParser import CodeforcesParser
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.model.ProblemMeta import ContestMeta, ProblemMeta
from oi_cli2.model.Result import SubmissionResult
from oi_cli2.model.TestCase import TestCase
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.HttpUtilCookiesHelper import HttpUtilCookiesHelper
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.enc import AESCipher
from oi_cli2.abstract.HtmlTagAbstract import HtmlTagAbstract
from oi_cli2.core.DI import DI_ACCMAN, DI_HTTP, DI_LOGGER, DI_PROVIDER

from ac_core.auth import fetch_login, is_logged_in
from ac_core.contest import fetch_tasks_meta, ParserProblemResult, fetch_standing
from ac_core.problem import parse_task
from ac_core.submit import fetch_submit
from ac_core.interfaces.HttpUtil import HttpRespInterface
from ac_core.result import fetch_result, fetch_result_by_url, SubmissionResult as CORE_SUB_RES

console = Console(color_system='256', style=None)


def s2str(sec: int) -> str:
  if sec < 60:
    return str(sec)
  if sec < 60 * 60:
    return f"{sec//60}:{(sec%60):02d}"
  return f"{sec // 60 // 60}:{((sec // 60) % 60):02d}:{(sec % 60):02d}"


def transform_Result(res: CORE_SUB_RES) -> SubmissionResult:
  mapdict = {
      CORE_SUB_RES.Status.AC: SubmissionResult.Status.AC,
      CORE_SUB_RES.Status.PENDING: SubmissionResult.Status.PENDING,
      CORE_SUB_RES.Status.RUNNING: SubmissionResult.Status.RUNNING,
      CORE_SUB_RES.Status.INIT: SubmissionResult.Status.PENDING,
      CORE_SUB_RES.Status.RE: SubmissionResult.Status.RE,
      CORE_SUB_RES.Status.TLE: SubmissionResult.Status.TLE,
      CORE_SUB_RES.Status.WA: SubmissionResult.Status.WA,
      CORE_SUB_RES.Status.CE: SubmissionResult.Status.CE,
  }
  if res.status in list(mapdict.keys()):
    status = mapdict[res.status]
  else:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
    logger.error(f'Unknown status {res.status}')
    status = SubmissionResult.Status.UNKNOWN

  return SubmissionResult(
      id=res.id,
      cur_status=status,
      quick_key=res.url,  # for refetch result
      url=res.url,  # TODO change to webpage url
      state_note=str(res.score),
      time_note=str(res.time_cost_ms / 1000),
      mem_note=str(res.mem_cost_kb),
      msg_txt=res.msg_txt,
  )


class AtCoder(BaseOj):

  def __init__(self, http_util: HttpUtil, logger: logging.Logger, account: Account,
               html_tag: HtmlTagAbstract) -> None:
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

    def transform(pm: ParserProblemResult) -> ProblemMeta:
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
        time_limit=str(pm.time_limit_msec),
        mem_limit=str(pm.memory_limit_kb),
        url=res.url,
    )

  def submit_code(self, problem_url: str, language_id: str, code_path: str) -> HttpRespInterface:
    if not self.login_website():
      raise Exception('Login Failed')

    return fetch_submit(self.http_util,
                        problem_url=problem_url,
                        lang_id=language_id,
                        source_code=open(code_path, 'r').read())

  def get_result_by_quick_id(self, quick_id: str) -> SubmissionResult:
    res = fetch_result_by_url(self.http_util, quick_id)
    return transform_Result(res)

  def get_result(self, problem_url: str) -> SubmissionResult:
    # problem_url https://atcoder.jp/contests/abc275/tasks/abc275_f
    res = fetch_result(self.http_util, problem_url)
    return transform_Result(res)

  # TODO fav control ?
  def print_friends_standing(self, cid: str) -> None:
    if not self.login_website():
      raise Exception('Login Failed')

    standing = fetch_standing(self.http_util, contest_id=cid)

    table = Table(title=f"Binary standing {cid}")
    table.add_column("rank", style="cyan")
    table.add_column("handle")
    for task in standing.TaskInfo:
      table.add_column(task.Assignment)

    for i in range(len(standing.StandingsData)):
      row: List[str] = []
      d = standing.StandingsData[i]
      is_self = d.UserName == self.account.account
      if is_self or (i & (i + 1)) == 0:  # care 0-index
        row.append(str(d.Rank))
        row.append(d.UserScreenName)
        for task in standing.TaskInfo:
          if task.TaskScreenName in d.TaskResults:
            # score = d.TaskResults[task.TaskScreenName].Score // 100
            penalty = d.TaskResults[task.TaskScreenName].Penalty
            elapsed_s = d.TaskResults[task.TaskScreenName].Elapsed // 1000 // 1000 // 1000
            row.append(f"+{penalty}\n{s2str(elapsed_s)}")
          else:
            row.append("")
        table.add_row(*row, style=Style(bgcolor="dark_green" if is_self else None))
        if is_self:
          break

    console.print(table)


def AtcoderGen(account: Account, provider: Provider2) -> BaseOj:
  http_util = provider.get(DI_HTTP)
  logger = provider.get(DI_LOGGER)
  oj: BaseOj = AtCoder(http_util=http_util,
                       logger=logger,
                       account=account,
                       html_tag=HtmlTag(http_util))
  return oj
