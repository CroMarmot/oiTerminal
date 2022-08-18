import logging
import os
import traceback

from oi_cli2.utils.Singleton import Singleton


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

    logger = logging.getLogger(__name__)
    # basic level shoud not larger than handler
    logger.setLevel(logging.DEBUG)
    # remove default handler
    logging.getLogger().handlers.clear()

    fileformatter = logging.Formatter('[%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d]%(message)s')
    streamformatter = logging.Formatter('%(process)s: %(filename)s %(lineno)d %(levelname)-8s %(message)s')

    # file
    fh = logging.FileHandler(logger_path)
    fh.setFormatter(fileformatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # stream warning
    sh = logging.StreamHandler()
    sh.setFormatter(streamformatter)
    sh.setLevel(logging.WARNING if LogConfig().is_production() else logging.DEBUG)
    logger.addHandler(sh)

    return logger
