import logging
from typing import List, Optional

from oi_cli2.model.Account import Account
# 依赖注入
from oi_cli2.utils.db import JsonFileDB
from oi_cli2.utils.enc import AESCipher
# 静态配置
from oi_cli2.utils.consts.ids import Ids


class AccountManager:

  def __init__(self, db: JsonFileDB, cipher: AESCipher, logger=logging):
    self.db = db
    self.cipher = cipher
    self.logger = logger

  def _get_account_list(self) -> List[Account]:
    acc_list: List[dict] = self.db.load(Ids.account) or []
    return list(map(lambda d: Account().dict_init(d), acc_list))

  def _set_account_list(self, acc_list: List[Account]):
    acc_list.sort(key=lambda acc0: (acc0.platform, -acc0.default, acc0.account, acc0.password))
    self.db.save(Ids.account, list(map(lambda d: d.__dict__, acc_list)))

  def get_list(self) -> List[Account]:
    return self._get_account_list()

  def set_default(self, index: int):
    accs: List[Account] = self._get_account_list()
    assert 0 <= index < len(accs)
    for i in range(len(accs)):
      if i == index:
        accs[i].default = True
      elif accs[i].platform == accs[index].platform:
        accs[i].default = False

    self._set_account_list(accs)

  def get_default_account(self, platform: str) -> Account:
    accs: List[Account] = self._get_account_list()
    for i in range(len(accs)):
      if accs[i].platform == platform and accs[i].default:
        return accs[i]
    raise Exception(f'Account Not Found int Platform [{platform}]')

  def get_account(self, platform: str, account: str) -> Optional[Account]:
    accs: List[Account] = self._get_account_list()
    for i in range(len(accs)):
      if accs[i].platform == platform and accs[i].account == account:
        return accs[i]

    return None

  def modify(self, platform: str, account: str, password=None, default=None) -> bool:
    modified = False
    accs: List[Account] = self._get_account_list()
    for item in accs:
      if item.platform == platform:
        if item.account == account:
          if password is not None:
            item.password = self.cipher.encrypt(password)
          if default:
            item.default = True
          modified = True
        elif default:
          item.default = False
    self._set_account_list(accs)
    return modified

  # Delete
  def delete(self, platform: str, account: str) -> bool:
    accs: List[Account] = self._get_account_list()
    for i in range(len(accs)):
      acc = accs[i]
      if acc.account != account or acc.platform != platform:
        continue
      if acc.default:
        # set new default
        for j in range(len(accs)):
          if j == i:
            continue
          if accs[i].platform == accs[j].platform:
            accs[i].default = True
            break
      del accs[i]
      self._set_account_list(accs)
      return True

    return False

  def new(self, platform, account, password, default=False) -> bool:
    accs: List[Account] = self._get_account_list()
    self.logger.debug("platform = %s, account = %s, default = %s", platform, account, default)
    has_default = False
    for item in accs:
      if item.platform == platform and item.account == account:
        return False
    for item in accs:
      if item.platform == platform and item.default:
        has_default = True
        break
    # first account in platform
    if not has_default:
      default = True
    accs.append(Account().initial(platform=platform,
                                  account=account,
                                  password=self.cipher.encrypt(password),
                                  default=default))
    if default:
      for item in accs:
        if item.platform == platform and item.account != account:
          item.default = False

    self._set_account_list(accs)
    return True
