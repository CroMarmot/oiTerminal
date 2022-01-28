import os
import re
import requests
from requests import RequestException, Response

# 配置url regex 和 mock文件
url2file = {
    '^https://codeforces.com/contests$': "codeforces_contests",
    '^https://codeforces.com/contest/\d*/problem/.*$': 'codeforces_problem',
    '^https://codeforces.com/contest/\d*$': 'codeforces_contest',
    '^https://codeforces.com/contest/\d*/standings/friends/true$': 'codeforces_standing'
}


class MockHttpUtil(object):
  def __init__(self, headers=None, code_type=None, cookies=None, logger=None, *args, **kwargs):
    self._headers = headers
    self._request = requests.session()
    self._code_type = code_type
    self._timeout = (7, 12)
    self._response = None
    self._advanced = False
    self._proxies = None
    self._logger = logger
    if kwargs.get('proxies'):
      self._proxies = {
          'http': kwargs.get('proxies'),
          'https': kwargs.get('proxies')
      }
    if self._headers:
      self._request.headers.update(self._headers)
    if cookies:
      self._request.cookies.update(cookies)

  def get(self, url, **kwargs):
    for key in url2file:
      if re.match(key, url):
        file = open(os.path.join(os.path.dirname(__file__), f'.mock/{url2file[key]}'), mode='r')
        all_of_it = file.read()
        file.close()
        resp = Response()
        resp._content = all_of_it.encode()
        resp.status_code = 200
        return resp
    else:
      return None

  def post(self, url, data=None, json=None, **kwargs):
    try:
      self._response = self._request.post(url, data, json, timeout=self._timeout, proxies=self._proxies, **kwargs)
      if self._code_type and self._response:
        self._response.encoding = self._code_type
      return self._response
    except RequestException as e:
      self._logger.exception(e)
      return None

  @property
  def headers(self):
    return self._request.headers

  @property
  def cookies(self):
    return self._request.cookies

  @staticmethod
  def abs_url(remote_path, oj_prefix):
    """

    :param remote_path: 原本的文件路径，可能是相对路径也可能是http或https开始的路径
    :param oj_prefix: oj的static文件前缀
    :return: 文件名，原本的补全之后的路径
    """
    if not remote_path.startswith('http://') and not remote_path.startswith('https://'):
      remote_path = oj_prefix.rstrip('/') + '/' + remote_path.lstrip('/')
    file_name = str(str(remote_path).split('/')[-1])
    return file_name, remote_path
