# TODO remove full file replace with new implement
import typing
from bs4 import element

from oi_cli2.abstract.HtmlTagAbstract import HtmlTagAbstract
from oi_cli2.utils.HttpUtil import HttpUtil


class HtmlTag(HtmlTagAbstract):

  def __init__(self, http_util: HttpUtil):
    super().__init__(http_util)

  @typing.no_type_check
  def update_tag(self, tag, oj_prefix: str, update_style=None):
    """
        :param tag: 一个顶级tag，从这个tag递归遍历所有子tag，寻找需要修改url的节点
        :param oj_prefix: 原oj的静态文件前缀
        :param update_style: 不为空的话，递归修改内联style
        :return: 成功返回原tag，失败返回None
        """
    if type(tag) == element.Tag:
      for child in tag.descendants:
        if type(child) != element.Tag:
          continue
        if update_style:
          child['style'] = update_style
        if child.name == 'a' and child.get('href'):
          if not child.get('class'):
            child['class'] = ()
          child['class'] += (HtmlTag.TagDesc.ANCHOR.value, )
          child['target'] = ('_blank', '_parent')
          child['href'] = self.http_util.abs_url(child.get('href'), oj_prefix=oj_prefix)[-1]
        if child.name == 'img' and child.get('src'):
          if not child.get('class'):
            child['class'] = ()
          child['class'] += (HtmlTag.TagDesc.IMAGE.value, )
          child['src'] = self.http_util.abs_url(child.get('src'), oj_prefix=oj_prefix)[-1]
    return tag
