from typing import Callable, Dict, List
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Provider2 import Provider2

T_OJFn = Callable[[Account, Provider2], BaseOj]


class OJManager:
  _ojFn: Dict[str, T_OJFn] = {}
  # _ojObj: Dict[str, BaseOj] = {}

  @staticmethod
  def regOj(platform: str, fn: T_OJFn) -> bool:
    if platform in OJManager._ojFn:
      return False
    OJManager._ojFn[platform] = fn
    return True

  @staticmethod
  def createOj(platform: str, account: Account, provider: Provider2) -> BaseOj:
    if platform in OJManager._ojFn:
      return OJManager._ojFn[platform](account, provider)
    else:
      raise Exception(f'Unknown Platform [{platform}]')
