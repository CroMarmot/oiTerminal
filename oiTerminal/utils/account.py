from typing import List, Optional

# Account 是紧密依赖 不采用依赖注入？
from oiTerminal.model.Account import Account
# 依赖注入
from oiTerminal.utils.db import JsonFileDB
from oiTerminal.utils.enc import AESCipher
# 静态配置
from oiTerminal.utils.consts.ids import Ids


class AccountManager:

    def __init__(self, db: JsonFileDB, cipher: AESCipher):
        self.db = db
        self.cipher = cipher

    def _get_account_list(self) -> List[Account]:
        acc_list: List[dict] = self.db.load(Ids.account) or []
        return list(map(lambda d: Account().dict_init(d), acc_list))

    def _set_account_list(self, acc_list: List[Account]):
        acc_list.sort(key=lambda acc0: (acc0.platform, -
                      acc0.default, acc0.account, acc0.password))
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

    def get_default_account(self, platform: str) -> Optional[Account]:
        accs: List[Account] = self._get_account_list()
        for i in range(len(accs)):
            if accs[i].platform == platform and accs[i].default:
                return accs[i]

        return None

    def modify_name(self, index: int, name: str):
        accs: List[Account] = self._get_account_list()
        assert 0 <= index < len(accs)
        accs[index].account = name
        self._set_account_list(accs)

    def modify_password(self, index, password):
        accs: List[Account] = self._get_account_list()
        assert 0 <= index < len(accs)
        accs[index].password = self.cipher.encrypt(password)
        self._set_account_list(accs)

    def modify_cf_rcpc(self, index, cf_rcpc):
        accs: List[Account] = self._get_account_list()
        assert 0 <= index < len(accs)
        accs[index].cf_rcpc = self.cipher.encrypt(cf_rcpc)
        self._set_account_list(accs)

    def delete_account(self, index):
        accs: List[Account] = self._get_account_list()
        assert 0 <= index < len(accs)
        if accs[index].default:
            for i in range(len(accs)):
                if i == index:
                    continue
                if accs[i].platform == accs[index].platform:
                    accs[i].default = True
                    break

        del accs[index]
        self._set_account_list(accs)

    # set default if no platform there
    def add_account(self, platform, account, password, cf_rcpc=None):
        accs: List[Account] = self._get_account_list()
        is_default = True
        for item in accs:
            if item.platform == platform:
                is_default = False
                break

        accs.append(Account().initial(platform, account,
                                      self.cipher.encrypt(password), default=is_default, cf_rcpc=None if cf_rcpc is None else self.cipher.encrypt(cf_rcpc)))

        self._set_account_list(accs)
