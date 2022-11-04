from enum import Enum
from bs4 import element

from oi_cli2.utils.HttpUtil import HttpUtil


class HtmlTagAbstract(object):

  def __init__(self, http_util: HttpUtil) -> None:
    self.http_util = http_util

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
