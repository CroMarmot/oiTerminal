# Language Key Value List
from typing import Dict


class LangKV(Dict[str, str]):
  pass

  def set(self, k, v):
    self[k] = v

  @property
  def data(self):
    return self
