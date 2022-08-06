from enum import Enum
from bs4 import element

from oi_cli2.utils.HttpUtil import HttpUtil


class HtmlTagAbstract(object):
    def __init__(self, http_util: HttpUtil):
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

    def update_tag(self, tag: element.Tag, oj_prefix: str, update_style=None) -> element.Tag:
        """

        :param tag: 一个顶级tag，从这个tag递归遍历所有子tag，寻找需要修改url的节点
        :param oj_prefix: 原oj的静态文件前缀
        :param update_style: 不为空的话，递归修改内联style
        :return: 成功返回原tag，失败返回None
        """
        assert False
