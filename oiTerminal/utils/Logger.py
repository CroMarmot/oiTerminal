import logging
import os
import traceback

from oiTerminal.utils.Singleton import Singleton


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
    # production log to log/oiTerminal.log, develop log to stdout
    formatter = logging.Formatter('[%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d]%(message)s')

    # 生产 输出到文件， stream 只输出问题
    if LogConfig().is_production():
        fh = logging.FileHandler(logger_path)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.WARNING)
        logger.addHandler(sh)
    else:
        # dev stream only
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG)
        logger.addHandler(sh)

    return logger
