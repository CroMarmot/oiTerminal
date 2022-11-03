from oi_cli2.core.DI import DI_DB_COOKIES, DI_HTTP
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.consts.ids import DB_COOKIES_ID
from oi_cli2.utils.db import JsonFileDB
from requests.utils import dict_from_cookiejar, cookiejar_from_dict


class HttpUtilCookiesHelper:

  def __init__(self) -> None:
    pass

  @staticmethod
  def save_cookie(provider: Provider2, platform: str, account: str) -> None:
    http_util: HttpUtil = provider.get(DI_HTTP)
    db: JsonFileDB = provider.get(DI_DB_COOKIES)
    data = db.load(DB_COOKIES_ID.cookies) or {}
    if platform not in data:
      data[platform] = {}
    data[platform][account] = dict_from_cookiejar(http_util.cookies)

    db.save(DB_COOKIES_ID.cookies, data)

  @staticmethod
  def load_cookie(provider: Provider2, platform: str, account: str) -> bool:
    http_util: HttpUtil = provider.get(DI_HTTP)
    db: JsonFileDB = provider.get(DI_DB_COOKIES)
    data = db.load(DB_COOKIES_ID.cookies) or {}
    if platform in data:
      if account in data[platform]:
        http_util.cookies.update(cookiejar_from_dict(data[platform][account]))
        return True
    return False
