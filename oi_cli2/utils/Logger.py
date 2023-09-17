import logging
import os
import traceback

from oi_cli2.utils.Singleton import Singleton

from oi_cli2.cli.constant import APP_NAME


@Singleton
class LogConfig:

  def __init__(self):
    self.env = os.getenv('OITERMINAL_ENV')
    if self.env is None:
      self.env = 'production'  # default

  def is_production(self):
    return self.env == 'production'

  def is_dev(self):
    return self.env == 'dev'


def getLogger(logger_path):
  try:
    os.makedirs(os.path.dirname(logger_path))
  except FileExistsError:
    pass
  except Exception as e:
    print(e)
    traceback.print_exc()

  # 调用库的 logging 名是 {APP_NAME}.xxx
  logger = logging.getLogger(APP_NAME)
  # basic level shoud not larger than handler
  logger.setLevel(logging.DEBUG)
  # remove default handler
  logging.getLogger().handlers.clear()

  # file
  fh = logging.FileHandler(logger_path)
  fileformatter = logging.Formatter(
      '[%(asctime)s %(name)s %(levelname)s %(filename)s %(funcName)s %(lineno)d]: %(message)s')
  fh.setFormatter(fileformatter)
  fh.setLevel(logging.DEBUG)
  logger.addHandler(fh)

  # stream warning
  sh = logging.StreamHandler()
  streamformatter = logging.Formatter('[%(levelname)s]: %(message)s')
  sh.setFormatter(streamformatter)
  sh.setLevel(logging.INFO if LogConfig().is_production() else logging.DEBUG)
  logger.addHandler(sh)

  return logger
