# TODO not important support lowercase and more, cf,codeforces,Codeforces -> Codeforces
import logging
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Singleton import Singleton


@Singleton
class OJUtil(object):

  def __init__(self):
    self.short2class = {}

    from oi_cli2.cli.adaptor.Codeforces import Codeforces
    self.reg(Codeforces)
    # TODO atcoder

  def reg(self, oj_class: BaseOj):
    assert False
    # for short_name in oj_class.short_name:
    #   if short_name in self.short2class:
    #     logging.error(f'{short_name} already registered')
    #   else:
    #     self.short2class[short_name] = oj_class
