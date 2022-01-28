# TODO not important support lowercase and more, cf,codeforces,Codeforces -> Codeforces
import logging
from oiTerminal.model.BaseOj import BaseOj
from oiTerminal.utils.Singleton import Singleton


@Singleton
class OJUtil(object):
  def __init__(self):
    self.short2class = {}

    from oiTerminal.custom.Codeforces.Codeforces import Codeforces
    self.reg(Codeforces)
    # TODO atcoder

  def reg(self, oj_class: BaseOj):
    for short_name in oj_class.short_name:
      if short_name in self.short2class:
        logging.error(f'{short_name} already registered')
      else:
        self.short2class[short_name] = oj_class
