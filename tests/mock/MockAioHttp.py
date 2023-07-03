from typing import Any, Callable, Dict, Tuple, AsyncIterator
import aiohttp
from tests.mock.MockHttpUtil import MockHttpUtil

from codeforces_core.interfaces.AioHttpHelper import AioHttpHelperInterface


class MockAioHttp(AioHttpHelperInterface):

  def __init__(self, host: str) -> None:
    self.inner = MockHttpUtil()
    self.host = host

  def create_form(self, form_data: Dict[str, Any]) -> aiohttp.FormData:
    return aiohttp.FormData()

  async def async_get(self, url: str, **kwargs) -> str:
    if not url.startswith('http'):
      url = self.host + url
    return self.inner.get(url=url, **kwargs).text

  async def async_post(self, url: str, data: Any, **kwargs) -> str:
    if not url.startswith('http'):
      url = self.host + url
    return self.inner.post(url=url, data=data, **kwargs).text

  def update_tokens(self, csrf: str, ftaa: str, bfaa: str, uc: str, usmc: str) -> None:
    return

  async def open_session(self) -> aiohttp.ClientSession:
    return

  def get_tokens(self) -> Any:
    return

  async def close_session(self) -> None:
    return

  # TODO move call back out
  async def websockets(self, url: str, callback: Callable[[Any], Tuple[bool, Any]]) -> AsyncIterator[Any]:
    return
