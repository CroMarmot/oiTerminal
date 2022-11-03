import logging
from typing import Callable, Dict
from oi_cli2.model.Account import Account

from oi_cli2.model.BaseOj import BaseOj

T_OJFn = Callable[[object, Account], BaseOj]


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
  def createOj(platform: str, account: Account, provider: object) -> BaseOj:
    if platform in OJManager._ojFn:
      return OJManager._ojFn[platform](provider=provider, account=account)
    else:
      raise Exception(f'Unknown Platform [{platform}]')
