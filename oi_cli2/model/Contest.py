from typing import Dict

from oi_cli2.model.Problem import Problem


class Contest:

  def __init__(self, oj: str, cid: str):
    self._oj: str = oj
    self._id = cid
    self._url: str = ''
    self._name: str = ''
    self.problems: Dict[str, Problem] = {}

  @property
  def id(self):
    return self._id

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value

  @property
  def url(self):
    return self._url

  @url.setter
  def url(self, value):
    self._url = value

  @property
  def oj(self):
    return self._oj

  @oj.setter
  def oj(self, value):
    self._oj = value
