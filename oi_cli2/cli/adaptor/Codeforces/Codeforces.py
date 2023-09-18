import asyncio
import logging
import os
from typing import Any, Tuple, AsyncIterator

from requests.exceptions import ReadTimeout, ConnectTimeout

from oi_cli2.cli.constant import APP_NAME, CIPHER_KEY, GREEN, DEFAULT
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.ParseProblemResult import ParsedProblemResult
from oi_cli2.model.LangKV import LangKV
from oi_cli2.model.Account import Account
from oi_cli2.model.ProblemMeta import ContestMeta, ProblemMeta, E_STATUS
from oi_cli2.model.Result import SubmissionResult
from oi_cli2.model.TestCase import TestCase
# from oi_cli2.utils.async2sync import iter_over_async
from oi_cli2.utils.enc import AESCipher

from codeforces_core.account import async_login, async_fetch_logged_in
from codeforces_core.contest_list import async_contest_list
from codeforces_core.contest_register import async_register, RegisterResultMsg
from codeforces_core.contest_standing import async_friends_standing
from codeforces_core.contest_meta import async_contest_meta, ProblemMeta as InnerProblemMeta
from codeforces_core.interfaces.AioHttpHelper import AioHttpHelperInterface
from codeforces_core.language import async_language
from codeforces_core.problem import async_problem
from codeforces_core.submit import async_submit, transform_submission, async_fetch_submission_page, SubmissionWSResult, SubmissionPageResult
from codeforces_core.url import pid2url, pid2split, problem_url_parse
from codeforces_core.websocket import create_contest_ws_task_yield


class Codeforces(BaseOj):

  def __init__(self, http_util: AioHttpHelperInterface, logger: logging.Logger, account: Account) -> None:
    super().__init__()
    assert (account is not None)
    self._base_url = 'https://codeforces.com/'
    self.logger: logging.Logger = logger
    self.account: Account = account
    self.http = http_util
    self.api_sub_logger: logging.Logger = logging.getLogger(f'{APP_NAME}.yxr-cf-core')

  async def init(self) -> None:
    await self.http.open_session()

  async def deinit(self) -> None:
    await self.http.close_session()

  def pid2url(self, problem_id: str):
    return self._base_url[:-1] + pid2url(problem_id)

  def pid2file_path(self, problem_id: str):
    contest_id, problem_key = pid2split(problem_id)
    return os.path.join(contest_id, problem_key)

  def problem_by_id(self, problem_id: str) -> ParsedProblemResult:
    return self.async_2_sync_session_wrap(lambda: self.async_problem_by_id(problem_id))

  async def async_problem_by_id(self, problem_id: str) -> ParsedProblemResult:
    contest_id, problem_key = pid2split(problem_id)
    self.logger.debug(f'{problem_id} => {contest_id}, {problem_key}')

    result = await async_problem(http=self.http, contest_id=contest_id, level=problem_key)

    return ParsedProblemResult(
        status=ParsedProblemResult.Status.NOTVIS,  # TODO for show progress
        title=result.title,
        test_cases=list(map(lambda x: TestCase(in_data=x.in_data, out_data=x.out_data), result.test_cases)),
        id=problem_id,
        oj=Codeforces.__name__,
        description=result.description,
        time_limit=result.time_limit,
        mem_limit=result.mem_limit,
        url=self.pid2url(problem_id),
        html=result.html,
        file_path=self.pid2file_path(problem_id))

  def problem(self, problem: ProblemMeta) -> ParsedProblemResult:
    return self.problem_by_id(problem.contest_id + problem.id)

  async def async_problem(self, problem: ProblemMeta) -> ParsedProblemResult:
    return await self.async_problem_by_id(problem.contest_id + problem.id)

  def login_website(self, force=False) -> bool:  # return successful
    return self.async_2_sync_session_wrap(lambda: self.async_login_website(force=force))

  # Force: true/false login whatever login before
  # TODO 逻辑还是有点问题，要实现支持
  #  - 未登录 => 登录
  #  - 已登录 => 不操作
  #  强制:
  #   - 未登录 => 登录
  #   - 已登录 => 取消cookies等 强制登录
  async def async_login_website(self, force=False) -> bool:  # return successful
    if not force:
      # try using cookies
      self.logger.info(f"{GREEN}Checking Log in {DEFAULT}")
      try:
        if await self.async_is_login():
          self.logger.info(f"{GREEN}{self.account.account} is Logged in {Codeforces.__name__}{DEFAULT}")
          return True
      except (ReadTimeout, ConnectTimeout) as e:
        self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      except Exception as e:
        self.logger.exception(e)

    try:
      self.logger.debug(f"{GREEN}{self.account.account} Logining {Codeforces.__name__}{DEFAULT}")

      return (await async_login(http=self.http,
                                handle=self.account.account,
                                password=AESCipher(CIPHER_KEY).decrypt(self.account.password))).success
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
    except Exception as e:
      self.logger.exception(e)

    return False

  def _is_login(self) -> bool:
    return self.async_2_sync_session_wrap(lambda: self.async_is_login())

  async def async_is_login(self) -> bool:
    ok, html_data = await async_fetch_logged_in(self.http)
    return ok

  def reg_contest(self, contest_id: str) -> bool:
    return self.async_2_sync_session_wrap(lambda: self.async_reg_contest(contest_id))

  async def async_reg_contest(self, contest_id: str) -> bool:
    if not await self.async_login_website():
      raise Exception('Login Failed')
    result = await async_register(http=self.http, contest_id=contest_id)
    return result.msg == RegisterResultMsg.AlreadyRegistered or result.msg == RegisterResultMsg.HaveBeenRegistered

  def submit_code(self, problem_url: str, language_id: str, code_path: str) -> bool:
    # https://codeforces.com/contest/1740/problem/G
    contest_id, problem_key = problem_url_parse(problem_url)
    sid = contest_id + problem_key
    return self.async_2_sync_session_wrap(lambda: self.async_submit_code(sid, language_id, code_path))

  # TODO move sid out as just Syntactic sugar
  async def async_submit_code(self, sid: str, language_id: str, code_path: str) -> bool:
    if not await self.async_login_website():
      raise Exception('Login Failed')
    contest_id, problem_key = pid2split(sid)
    self.logger.debug(f'{contest_id},{problem_key}')

    submit_id, resp = await async_submit(http=self.http,
                                         contest_id=contest_id,
                                         level=problem_key,
                                         file_path=code_path,
                                         lang_id=language_id,
                                         logger=self.api_sub_logger)
    self.logger.debug(f'submit_id = {submit_id}')
    return bool(submit_id)

  async def async_get_result_yield(self, problem_url: str, time_gap: float = 2) -> AsyncIterator[SubmissionResult]:
    contest_id, problem_key = problem_url_parse(problem_url)

    # TODO move more parse inside codeforces-core ? cf是出错中断形式,状态+数量
    def page_result_transform(res: SubmissionPageResult) -> SubmissionResult:
      self.logger.debug('page res:' + str(res))
      cur_status = SubmissionResult.Status.PENDING
      if res.verdict.startswith('Running'):
        cur_status = SubmissionResult.Status.RUNNING
      elif res.verdict.startswith('In queue'):
        cur_status = SubmissionResult.Status.RUNNING
      elif res.verdict.startswith('Accepted'):
        cur_status = SubmissionResult.Status.AC
      elif res.verdict.startswith('Pretests passed'):
        cur_status = SubmissionResult.Status.AC
      elif res.verdict.startswith('Wrong answer'):
        cur_status = SubmissionResult.Status.WA
      elif res.verdict.startswith('Time limit exceeded'):
        cur_status = SubmissionResult.Status.TLE
      elif res.verdict.startswith('Runtime error'):  # Runtime error on pretest 2
        cur_status = SubmissionResult.Status.RE
      else:
        self.logger.error('NOT HANDLE PAGE:' + str(res.verdict))

      if res.url.startswith('/'):
        res.url = self._base_url[:-1] + res.url

      return SubmissionResult(id=res.id,
                              cur_status=cur_status,
                              time_note=res.time_ms + ' ms',
                              mem_note=str(int(res.mem_bytes) / 1000) + ' kb',
                              url=res.url,
                              msg_txt=res.verdict)

    # TODO move more parse inside codeforces-core ?
    def ws_result_transform(res: SubmissionWSResult) -> SubmissionResult:
      cur_status = SubmissionResult.Status.PENDING
      if res.msg == 'TESTING':
        cur_status = SubmissionResult.Status.RUNNING
      elif res.msg == 'OK':
        cur_status = SubmissionResult.Status.AC
      elif res.msg == 'WRONG_ANSWER':
        cur_status = SubmissionResult.Status.WA
      else:
        self.logger.error('NOT HANDLE WS:' + str(res.msg))

      msg_txt = str(res.testcases)
      if cur_status in [SubmissionResult.Status.AC, SubmissionResult.Status.WA]:
        msg_txt = f'{res.passed}/{res.testcases}'

      return SubmissionResult(
          id=str(res.submit_id),
          cur_status=cur_status,
          time_note=str(res.ms) + ' ms',
          mem_note=str(int(res.mem) / 1000) + ' kb',
          url=f'{self._base_url}contest/{res.contest_id}/submission/{res.submit_id}',
          msg_txt=msg_txt,
      )

    # TODO visit page without ws first
    results = await async_fetch_submission_page(http=self.http, problem_url=problem_url, logger=self.api_sub_logger)
    fix_submit_id = ''
    if len(results) > 0:
      result = page_result_transform(results[0])
      fix_submit_id = result.id
      self.logger.debug(f"fix submit_id = {fix_submit_id}")
      yield result
      if result.cur_status not in [SubmissionResult.Status.PENDING, SubmissionResult.Status.RUNNING]:
        return

    self.logger.debug('after page result, enter ws result')

    # return (end watch?, transform result)
    def custom_handler(result: Any) -> Tuple[bool, SubmissionWSResult]:
      parsed_data = transform_submission(result)
      if fix_submit_id and fix_submit_id != parsed_data.contest_id:  # submit id not match, dont end watch ws
        return False, parsed_data
      if parsed_data.msg != 'TESTING':
        return True, parsed_data
      return False, parsed_data

    # TODO add timeout for ws
    # TODO 可能有别人的? pc/cc?
    async for wsresult in create_contest_ws_task_yield(http=self.http,
                                                       contest_id=contest_id,
                                                       ws_handler=custom_handler,
                                                       logger=self.api_sub_logger):
      self.logger.debug('ws res:' + str(wsresult))
      if fix_submit_id and wsresult.submit_id != fix_submit_id:
        self.logger.debug('[skip]fixed id not match! continue')
        continue
      data = ws_result_transform(wsresult)
      yield data
      if data.cur_status not in [SubmissionResult.Status.PENDING, SubmissionResult.Status.RUNNING]:
        return

    results = await async_fetch_submission_page(http=self.http, problem_url=problem_url)
    assert len(results) > 0
    yield page_result_transform(results[0])

  def get_language(self) -> LangKV:
    return self.async_2_sync_session_wrap(lambda: self.async_get_language())

  async def async_get_language(self) -> LangKV:
    await self.async_login_website()
    res = await async_language(self.http)
    ret: LangKV = {}
    for item in res:
      ret[item.value] = item.text
    return ret

  @staticmethod
  def support_contest() -> bool:
    return True

  def print_contest_list(self) -> bool:
    return self.async_2_sync_session_wrap(lambda: self.async_print_contest_list())

  async def async_print_contest_list(self) -> bool:
    await self.async_login_website()

    result = await async_contest_list(http=self.http)
    from .contestList import printData
    printData(result)
    return True

  def get_contest_meta(self, contest_id: str) -> ContestMeta:
    return self.async_2_sync_session_wrap(lambda: self.async_get_contest_meta(contest_id=contest_id))

  async def async_get_contest_meta(self, contest_id: str) -> ContestMeta:
    await self.async_login_website()

    result = await async_contest_meta(http=self.http, contest_id=contest_id)

    def transform(problem: InnerProblemMeta) -> ProblemMeta:
      return ProblemMeta(
          id=problem.id,
          url=problem.url,
          name=problem.name,
          passed=problem.passed,  # number of passed submission in contest
          score=0,
          status=E_STATUS(problem.status),  # ???? TODO
          time_limit_msec=problem.time_limit_msec,  # ms
          memory_limit_kb=problem.memory_limit_kb,  # mb
          contest_id=problem.contest_id,
      )

    return ContestMeta(id=contest_id, url=result.url, problems=list(map(lambda o: transform(o), result.problems)))

  def async_2_sync_session_wrap(self, fn):

    async def task():
      await self.http.open_session()
      result = await fn()
      await self.http.close_session()
      return result

    return asyncio.run(task())

  def print_friends_standing(self, cid: str) -> None:
    return self.async_2_sync_session_wrap(lambda: self.async_print_friends_standing(cid))

  async def async_print_friends_standing(self, cid: str) -> None:
    result = await async_friends_standing(http=self.http, contest_id=cid)
    from .standing import printData
    printData(result, title=f"Friends standing {result.url}", handle=self.account.account)

  def cid2url(self, cid: str) -> str:
    return f'{self._base_url}contests/{cid}'
