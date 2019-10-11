import logging
import json
from functools import wraps
from enum import Enum

from constant import *
import requests
from bs4 import element
from requests import RequestException
import traceback

from . import platformsClassName


def singleton(cls):
    __instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]

    return get_instance


# logger start -----------------------------

@singleton
class LogConfig:
    def __init__(self):
        self.env = os.getenv('OITERMINAL_ENV')
        if self.env is None:
            self.env = 'production'  # default

    def is_production(self):
        return self.env == 'production'

    def is_dev(self):
        return self.env == 'dev'


LOG_BASE = 'log'  # just a tiny tool don't put log in /log
LOG_LEVEL = logging.WARNING if LogConfig().is_production() else logging.INFO
SPIDER_LOG_PATH = os.path.join(LOG_BASE, 'oiTerminal.log')
try:
    os.makedirs(LOG_BASE)
except FileExistsError:
    pass
except Exception as e:
    print(e)
    traceback.print_exc()
logger = logging.getLogger(__name__)
handler = logging.FileHandler(SPIDER_LOG_PATH) if LogConfig().is_production() else logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# logger end -----------------------------


class HttpUtil(object):
    def __init__(self, headers=None, code_type=None, cookies=None, *args, **kwargs):
        self._headers = headers
        self._request = requests.session()
        self._code_type = code_type
        self._timeout = (7, 12)
        self._response = None
        self._advanced = False
        self._proxies = None
        if kwargs.get('proxies'):
            self._proxies = {
                'http': kwargs.get('proxies'),
                'https': kwargs.get('proxies')
            }
        if self._headers:
            self._request.headers.update(self._headers)
        if cookies:
            self._request.cookies.update(cookies)

    def get(self, url, **kwargs):
        try:
            self._response = self._request.get(url, timeout=self._timeout, proxies=self._proxies, **kwargs)
            if self._code_type and self._response:
                self._response.encoding = self._code_type
            return self._response
        except RequestException as e:
            logger.exception(e)
            return None

    def post(self, url, data=None, json=None, **kwargs):
        try:
            self._response = self._request.post(url, data, json, timeout=self._timeout, proxies=self._proxies, **kwargs)
            if self._code_type and self._response:
                self._response.encoding = self._code_type
            return self._response
        except RequestException as e:
            logger.exception(e)
            return None

    @property
    def headers(self):
        return self._request.headers

    @property
    def cookies(self):
        return self._request.cookies

    @staticmethod
    def abs_url(remote_path, oj_prefix):
        """

        :param remote_path: 原本的文件路径，可能是相对路径也可能是http或https开始的路径
        :param oj_prefix: oj的static文件前缀
        :return: 文件名，原本的补全之后的路径
        """
        if not remote_path.startswith('http://') and not remote_path.startswith('https://'):
            remote_path = oj_prefix.rstrip('/') + '/' + remote_path.lstrip('/')
        file_name = str(str(remote_path).split('/')[-1])
        return file_name, remote_path


class HtmlTag(object):
    class TagDesc(Enum):
        """
        给html的tag加上相应的class

        TITLE = 'vj-title'
        CONTENT = 'vj-content'
        IMAGE = 'vj-image'
        FILE = 'vj-file'
        ANCHOR = 'vj-anchor'

        """
        TITLE = 'vj-title'
        CONTENT = 'vj-content'
        IMAGE = 'vj-image'
        FILE = 'vj-file'
        ANCHOR = 'vj-anchor'

    class TagStyle(Enum):
        """
        TITLE 和 CONTENT 需要加额外的 Style 保证网页风格一致
        """
        TITLE = 'font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB"' \
                ',"Microsoft YaHei","微软雅黑",Arial,sans-serif; font-size: 16px;font-weight: bold;color:#000000;'
        CONTENT = 'font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB",' \
                  '"Microsoft YaHei","微软雅黑",Arial,sans-serif; font-size: 16px;color:#495060;'

    @staticmethod
    def update_tag(tag, oj_prefix, update_style=None):
        """

        :param tag: 一个顶级tag，从这个tag递归遍历所有子tag，寻找需要修改url的节点
        :param oj_prefix: 原oj的静态文件前缀
        :param update_style: 不为空的话，递归修改内联style
        :return: 成功返回原tag，失败返回None
        """
        if type(tag) == element.Tag:
            for child in tag.descendants:
                if type(child) == element.Tag and update_style:
                    child['style'] = update_style
                if child.name == 'a' and child.get('href'):
                    if not child.get('class'):
                        child['class'] = ()
                    child['class'] += (HtmlTag.TagDesc.ANCHOR.value,)
                    child['target'] = ('_blank', '_parent')
                    child['href'] = HttpUtil.abs_url(child.get('href'), oj_prefix=oj_prefix)[-1]
                if child.name == 'img' and child.get('src'):
                    if not child.get('class'):
                        child['class'] = ()
                    child['class'] += (HtmlTag.TagDesc.IMAGE.value,)
                    child['src'] = HttpUtil.abs_url(child.get('src'), oj_prefix=oj_prefix)[-1]
        return tag


class LanguageUtil(object):
    _lang_cfg = None

    @staticmethod
    def init() -> map:
        if LanguageUtil._lang_cfg is not None:
            return LanguageUtil._lang_cfg
        if not os.path.isfile(LANG_CONFIG_FILE):
            raise Exception(f'LANG_CONFIG_FILE [{LANG_CONFIG_FILE}] NOT EXIST!')
        with open(LANG_CONFIG_FILE) as f:
            LanguageUtil._lang_cfg = json.load(f)
        return LanguageUtil._lang_cfg

    @staticmethod
    def local_lang() -> list:
        return list(LanguageUtil.init().keys())

    @staticmethod
    def lang2suffix(lang) -> str:
        return LanguageUtil.init().get(lang).get('suffix')

    @staticmethod
    def lang2template(lang) -> str:
        return TEMPLATEFOLDER + LanguageUtil.init().get(lang).get('template')

    @staticmethod
    def lang2compile(lang) -> str:
        return LanguageUtil.init().get(lang).get('compile')

    @staticmethod
    def lang2exe(lang, input_file, output_file):
        return LanguageUtil.init().get(lang).get('exe') + " < " + input_file + " > " + output_file


# TODO not important support lowercase and more, cf,codeforces,Codeforces -> Codeforces
class OJUtil(object):
    @staticmethod
    def short2full(short_name) -> str:
        ret = {
            "cf": platformsClassName.Codeforces,
            "ac": platformsClassName.AtCoder,
        }.get(short_name)
        if ret is None:
            raise Exception(f'not support oj short name "{short_name}"')
        return ret

    @staticmethod
    def get_supports():
        return [
            # 'Aizu',
            # 'HDU',
            # 'FZU', FZU 体验太差老是访问不了，还是不要支持好了
            # 'POJ',
            # 'WUST',
            # 'ZOJ',
            platformsClassName.Codeforces,
            platformsClassName.AtCoder,
        ]
