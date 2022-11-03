import logging
from typing import Any, Dict, List 

import os
import re
import threading

from requests.exceptions import ReadTimeout, ConnectTimeout
from bs4 import BeautifulSoup

from oi_cli2.cli.constant import CIPHER_KEY, GREEN, DEFAULT, OT_FOLDER
from oi_cli2.core import provider
from oi_cli2.custom.Codeforces.CodeforcesParser import CodeforcesParser
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.model.LangKV import LangKV
from oi_cli2.model.Account import Account
from oi_cli2.model.Problem import Problem
from oi_cli2.model.Contest import Contest
from oi_cli2.model.Result import Result
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.HttpUtilCookiesHelper import HttpUtilCookiesHelper
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.enc import AESCipher


class Codeforces(BaseOj):

  def __init__(self,
               http_util: HttpUtil,
               logger: logging.Logger,
               account: Account,
               html_tag: object) -> None:
    super().__init__()
    assert (account is not None)
    self._base_url = 'https://codeforces.com/'
    self.logger:logging.Logger = logger
    self.html_tag = html_tag
    self.account: Account = account
    self.http_util = http_util
    self.parser = CodeforcesParser(html_tag=html_tag, logger=logger)
    config_folder = ConfigFolder(OT_FOLDER)
    HttpUtilCookiesHelper.load_cookie(provider=provider.o,
                                      platform=Codeforces.__name__,
                                      account=account.account)
    # write codeforces RCPC cookie in .oiTerminal/CF_RCPC
    with open(config_folder.get_config_file_path("CF_RCPC")) as f:
      rcpc = f.read().strip()
      self.http_util.cookies.set("RCPC", rcpc, domain="codeforces.com")

  def pid2url(self, problem_id: str):
    result = re.match('^(\\d+)([A-Z]\\d?)$', problem_id)
    if result is None:
      raise Exception('problem id[' + problem_id + '] ERROR')
    return f'{self._base_url}contest/{result.group(1)}/problem/{result.group(2)}'

  def pid2file_path(self, problem_id: str):
    result = re.match('^(\\d+)([A-Z]\\d?)$', problem_id)
    if result is None:
      raise Exception('problem id[' + problem_id + '] ERROR')
    return os.path.join(result.group(1), result.group(2))

  def problem(self, problem_id: str) -> ParseProblemResult:
    # problem_id parse
    url = self.pid2url(problem_id)
    self.logger.debug(url)

    # http_util.get url
    response = self.http_util.get(url=url)
    if response.status_code != 200 or response.text is None:
      raise Exception(f"Fetch Problem Error, problem id={problem_id}")
    problem = self.parser.problem_parse(response.text)

    problem.id = problem_id
    problem.url = url
    problem.oj = Codeforces.__name__
    problem.file_path = self.pid2file_path(problem_id)
    return problem

  # TODO msg chan
  # Force: true/false login whatever login before
  def login_website(self, force=False) -> bool:  # return successful
    if not force:
      # try using cookies
      logging.debug(f"{GREEN}Checking Log in {DEFAULT}")
      try:
        if self._is_login():
          logging.debug(f"{GREEN}{self.account.account} is Logged in {Codeforces.__name__}{DEFAULT}")
          return True
      except (ReadTimeout, ConnectTimeout) as e:
        self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      except Exception as e:
        self.logger.exception(e)

    try:
      logging.debug(f"{GREEN}{self.account.account} Logining {Codeforces.__name__}{DEFAULT}")
      url = f'{self._base_url}enter?back=%2F'
      self.logger.debug(f"get {url}")
      res = self.http_util.get(url)
      soup = BeautifulSoup(res.text, 'lxml')
      csrf_token = soup.find(attrs={'name': 'X-Csrf-Token'}).get('content')
      post_data = {
          'csrf_token': csrf_token,
          'action': 'enter',
          'ftaa': '',
          'bfaa': '',
          'handleOrEmail': self.account.account,
          'password': AESCipher(CIPHER_KEY).decrypt(self.account.password),
          'remember': 'on'
      }
      self.http_util.post(url=f'{self._base_url}enter', data=post_data)
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
    except Exception as e:
      self.logger.exception(e)

    try:
      if self._is_login():
        logging.debug(f"{GREEN}{self.account.account} Logined {Codeforces.__name__}{DEFAULT}")
        HttpUtilCookiesHelper.save_cookie(provider=provider.o,
                                          platform=Codeforces.__name__,
                                          account=self.account.account)
        return True
      else:
        return False
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      return False
    except Exception as e:
      self.logger.exception(e)
      return False

  def _is_login(self) -> bool:
    res = self.http_util.get(self._base_url)
    return bool(res and re.search(r'logout">Logout</a>', res.text))

  def get_tta(self) -> str:
    """
    This calculates protection value (_tta)
    Reversed from js
    """
    hstr = self.http_util.cookies.get('39ce7')
    total = 0
    for i, ch in enumerate(hstr):
      total = (total + (i + 1) * (i + 2) * ord(ch)) % 1009
      if i % 3 == 0:
        total += 1
      if i % 2 == 0:
        total *= 2

      if i > 0:
        total -= ord(hstr[i // 2]) // 2 * (total % 5)
      total = total % 1009
    return str(total)

  def reg_contest(self, cid: str) -> bool:
    if re.match('^\\d+$', cid) is None:
      raise Exception('contest id [' + cid + '] ERROR')
    response = self.http_util.get(url=f'{self._base_url}contestRegistration/{cid}')
    if response is None or response.status_code != 200 or response.text is None:
      raise Exception(f"Reg Contest Error, cid={cid}")
    print("reg contest:" + cid)

    soup = BeautifulSoup(response.text, 'lxml')

    csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
    _tta = self.get_tta()
    post_data = {
        'csrf_token': csrf_token,
        'action': 'formSubmitted',
        'backUrl': '',
        'takePartAs': 'personal',
        '_tta': _tta,
    }
    self.http_util.post(url=f'{self._base_url}contestRegistration/' + cid, data=post_data)
    # return True except network error
    # TODO get more detail
    return True

  def get_contest(self, cid: str) -> Contest:
    if re.match('^\\d+$', cid) is None:
      raise Exception(f'contest id "{cid}" ERROR')

    response = self.http_util.get(url=f'{self._base_url}contest/' + cid)
    ret = Contest(oj=Codeforces.__name__, cid=cid)
    if response is None or response.status_code != 200 or response.text is None:
      raise Exception(f"Fetch Contest Error,cid={cid}")
    print("get contest:" + cid)
    self.parser.contest_parse(contest=ret, response=response.text)
    threads = []
    for pid in ret.problems.keys():
      # self.get_problem(pid=cid + pid, problem=ret.problems[pid])
      t = threading.Thread(target=self.get_problem, args=(cid + pid, ret.problems[pid]))
      threads.append(t)
      t.start()
    for t in threads:
      t.join()
    return ret

  def get_problem(self, pid: str, problem: Problem = None) -> Problem:
    result = re.match('^(\\d+)([A-Z]\\d?)$', pid)
    if result is None:
      raise Exception('problem id[' + pid + '] ERROR')
    url = f'{self._base_url}contest/{result.group(1)}/problem/{result.group(2)}'
    if problem is None:
      problem = Problem(oj=Codeforces.__name__, pid=pid, url=url)
    else:
      problem.url = url
    response = self.http_util.get(url=url)
    if response is None or response.status_code != 200 or response.text is None:
      raise Exception(f"Fetch Problem Error, pid={pid}")
    self.parser.problem_parse(response=response.text)
    return problem

  def submit_code(self, pid: str, language: str, code: str) -> bool:
    if not self.login_website():
      raise Exception('Login Failed')

    result = re.match('^(\\d+)([A-Z]\\d?)$', pid)
    if result is None:
      raise Exception("submit_code: WRONG pid[" + pid + "]")

    try:
      res = self.http_util.get(f'{self._base_url}contest/{result.group(1)}/submit')
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      return False
    except Exception as e:
      self.logger.exception(e)
      return False
    soup = BeautifulSoup(res.text, 'lxml')
    csrf_token = soup.find(attrs={'name': 'X-Csrf-Token'}).get('content')
    post_data = {
        'csrf_token': csrf_token,
        'ftaa': '',
        'bfaa': '',
        'action': 'submitSolutionFormSubmitted',
        'contestId': result.group(1),
        'submittedProblemIndex': result.group(2),
        'programTypeId': language,
        'source': open(code, 'rb').read(),
        'tabSize': 0,
        'sourceFile': '',
    }
    url = f'{self._base_url}contest/{result.group(1)}/submit?csrf_token={csrf_token}'
    try:
      res = self.http_util.post(url, data=post_data)
      if res and res.status_code == 200:
        return True
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      return False
    except Exception as e:
      self.logger.exception(e)
      return False
    return False

  def get_result(self, pid: str) -> Result:
    self.logger.info(f'{self._base_url}api/user.status?handle=' + self.account.account + '&count=1')
    return self._get_result_by_url(f'{self._base_url}api/user.status?handle=' +
                                   self.account.account + '&count=1')

  def get_result_by_quick_id(self, quick_id: str) -> Result:
    return self._get_result_by_url(quick_id)

  def _get_result_by_url(self, url: str) -> Result:
    try:
      response = self.http_util.get(url=url)
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      raise Exception(f'get result Failed,url={url}')
    except Exception as e:
      self.logger.exception(e)
      raise Exception(f'get result Failed,url={url}')
    if response.status_code != 200 or response.text is None:
      raise Exception(f'get result Failed,url={url}')
    ret = self.parser.result_parse(response=response.text)
    ret.quick_key = url
    return ret

  def get_language(self) -> LangKV:
    res = self.http_util.get(f'{self._base_url}problemset/submit')
    ret: LangKV = LangKV()
    if res.text:
      soup = BeautifulSoup(res.text, 'lxml')
      tags = soup.find('select', attrs={'name': 'programTypeId'})
      if tags:
        for child in tags.find_all('option'):
          ret[child.get('value')] = child.string
    return ret

  def _assert_working(self):
    if self.http_util.get(self._base_url).status_code != 200:
      raise Exception(f'{self._base_url} not working')

  @staticmethod
  def accounthttp_utiluired() -> bool:
    return False

  @staticmethod
  def support_contest() -> bool:
    return True

  def print_contest_list(self) -> bool:
    self.login_website()
    # when in contest, without complete=true, will redirect to running contest page
    try:
      url = f'{self._base_url}contests?complete=true'
      resp = self.http_util.get(url)
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
      return False
    except Exception as e:
      self.logger.exception(e)
    from .contestList import printData
    printData(resp.text)
    return True

  def print_problems_in_contest(self, cid: str) -> None:
    self.login_website()
    from .problemList import printData
    url = f'{self._base_url}contest/{cid}'
    printData(self.http_util.get(url).text, title=f"Contest {url}")

  def get_problemids_in_contest(self, cid: str) -> List[Dict[str, Any]]:
    self.login_website()
    from .problemList import html2json
    url = f'{self._base_url}contest/{cid}'
    return html2json(self.http_util.get(url).text)

  def print_friends_standing(self, cid: str) -> None:
    if not self.login_website():
      raise Exception('Login Failed')
    from .standing import printData
    url = f'{self._base_url}contest/{cid}/standings/friends/true'
    try:
      printData(self.http_util.get(url).text,
                title=f"Friends standing {url}",
                handle=self.account.account)
    except (ReadTimeout, ConnectTimeout) as e:
      self.logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
    except Exception as e:
      self.logger.exception(e)

  # wss://pubsub.codeforces.com/ws/s_44e079e878db3d6cd8130358e638715d84b9b7e2/s_0b4b2a8c82dc858a100c4b1bcb927492039a8efd?_=1639017481660&tag=&time=&eventid=
  #
  # channel: "s_0b4b2a8c82dc858a100c4b1bcb927492039a8efd"
  # id: 28
  # text: "{\"t\":\"s\",\"d\":[2673242382570391613,138492951,1613,1209361,\"TESTS\",null,\"OK\",61,61,31,0,124336641,\"21220\",\"09.12.2021 5:38:00\",\"09.12.2021 5:38:00\",2147483647,54,0]}"
