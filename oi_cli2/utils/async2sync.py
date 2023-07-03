import asyncio
from typing import Any, AsyncGenerator

# def iter_over_async(
#     async_generator: AsyncGenerator,
#     loop: asyncio.AbstractEventLoop = None,
# ):
#   ait = async_generator.__aiter__()
#   if loop == None:
#     loop = asyncio.get_event_loop()
#
#   async def get_next():
#     try:
#       obj = await ait.__anext__()
#       print('obj = ', obj)
#       return False, obj
#     except StopAsyncIteration:
#       return True, None
#
#   while True:
#     done, obj = loop.run_until_complete(get_next())
#     if done:
#       break
#     print('iter yield obj = ', obj)
#     yield obj
#
#   # ait = async_generator.__aiter__()
#
#   # async def get_next() -> tuple[bool, Any]:
#   #   try:
#   #     obj = await ait.__anext__()
#   #     done = False
#
#   #   except StopAsyncIteration:
#   #     obj = None
#   #     done = True
#
#   #   return done, obj
#
#   # while True:
#   #   done, obj = asyncio.run_coroutine_threadsafe(get_next(), loop).result()
#
#   #   if done:
#   #     break
#   #  yield obj
#
