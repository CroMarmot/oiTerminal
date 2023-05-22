import requests


class HttpUtil(object):

  def __init__(self, headers=None, logger=None):
    self._headers = headers or {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    self._request = requests.Session()
    self._timeout = (10, 20)  # connect timeout , read timeout
    self._logger = logger
    if self._headers:
      self._request.headers.update(self._headers)

  def get(self, url, allow_redirects: bool = True):
    # TODO ? fix kwargs timeout 优先级大于内置_timeout ?
    return self._request.get(url, timeout=self._timeout, allow_redirects=allow_redirects)

  def post(self, url, data=None, allow_redirects: bool = True):
    try:
      return self._request.post(url, data, timeout=self._timeout, allow_redirects=allow_redirects)
    except Exception as e:
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
