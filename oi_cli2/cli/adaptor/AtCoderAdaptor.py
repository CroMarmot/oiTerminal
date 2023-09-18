import logging
import time
from typing import List, AsyncIterator
from rich.console import Console
from rich.table import Table
from rich.style import Style

from oi_cli2.model.LangKV import LangKV

from ...cli.constant import CIPHER_KEY
from ...model.Account import Account
from ...model.BaseOj import BaseOj
from ...model.ParseProblemResult import ParsedProblemResult
from ...model.ProblemMeta import ContestMeta, ProblemMeta
from ...model.Result import SubmissionResult
from ...model.TestCase import TestCase
from ...utils.HtmlTag import HtmlTag
from ...utils.HttpUtil import HttpUtil
from ...utils.HttpUtilCookiesHelper import HttpUtilCookiesHelper
from ...utils.Provider2 import Provider2
from ...utils.enc import AESCipher
from ...abstract.HtmlTagAbstract import HtmlTagAbstract
from ...core.DI import DI_ACCMAN, DI_HTTP, DI_LOGGER, DI_PROVIDER

from ac_core.auth import fetch_login, is_logged_in
from ac_core.contest import fetch_tasks_meta, ParserProblemResult, fetch_standing, fetch_list
from ac_core.problem import parse_task
from ac_core.submit import fetch_submit
from ac_core.interfaces.HttpUtil import HttpRespInterface
from ac_core.result import fetch_result, SubmissionResult as CORE_SUB_RES
from ac_core.language import fetch_language

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
      time_note=str(res.time_cost_ms / 1000) + ' ms',
      mem_note=str(res.mem_cost_kb) + ' kb',
      msg_txt=res.msg_txt,
  )


class AtCoder(BaseOj):

  def __init__(self, http_util: HttpUtil, logger: logging.Logger, account: Account, html_tag: HtmlTagAbstract) -> None:
    super().__init__()
    assert (account is not None)
    self._base_url = 'https://atcoder.jp/'
    self.logger: logging.Logger = logger
    self.html_tag = html_tag
    self.account: Account = account
    self.http_util = http_util
    HttpUtilCookiesHelper.load_cookie(provider=Provider2(), platform=AtCoder.__name__, account=account.account)

  def login_website(self, force: bool = False) -> bool:
    if force or not is_logged_in(self.http_util):  # need login
      if force:
        self.http_util._request.cookies.clear()
      ok = fetch_login(self.http_util, self.account.account, AESCipher(CIPHER_KEY).decrypt(self.account.password))
      # if ok:
      # always save cookie
      HttpUtilCookiesHelper.save_cookie(provider=Provider2(), platform=AtCoder.__name__, account=self.account.account)
      return ok
    return True

  async def async_get_contest_meta(self, cid: str) -> ContestMeta:
    return self.get_contest_meta(cid)

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

  async def async_problem(self, problem: ProblemMeta) -> ParsedProblemResult:
    return self.problem(problem)

  # Care !! in Atcoder may arc058 C = https://atcoder.jp/contests/arc058/tasks/arc058_a
  def problem(self, pm: ProblemMeta) -> ParsedProblemResult:
    html = self.http_util.get(pm.url).text
    res = parse_task(html=html)
    return ParsedProblemResult(
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

  async def async_get_result_yield(self, problem_url: str, time_gap: float = 1) -> AsyncIterator[SubmissionResult]:
    while True:
      res = transform_Result(fetch_result(self.http_util, problem_url))
      yield res
      if res.cur_status not in [SubmissionResult.Status.PENDING, SubmissionResult.Status.RUNNING]:
        break
      time.sleep(time_gap)

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

  def get_language(self) -> LangKV:
    results = fetch_language(self.http_util)
    ret: LangKV = {}
    for item in results:
      ret[item.value] = item.text
    return ret

  def print_contest_list(self) -> bool:
    # self.login_website()
    result = fetch_list(self.http_util)
    from .AtCoder_printList import printData
    printData(result)
    return True

  def cid2url(self, cid: str) -> str:
    return f'{self._base_url}contests/{cid}'


def AtcoderGen(account: Account, provider: Provider2) -> BaseOj:
  http_util = provider.get(DI_HTTP)
  logger = provider.get(DI_LOGGER)
  oj: BaseOj = AtCoder(http_util=http_util, logger=logger, account=account, html_tag=HtmlTag(http_util))
  return oj
