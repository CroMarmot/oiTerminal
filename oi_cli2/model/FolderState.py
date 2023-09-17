# TODO dataclasses, for better debug


class FolderState:
  oj: str
  id: str  # string id
  cid: str  # contest id
  pid: str  # problem id
  problem_url: str
  up_lang: str
  template_alias: str

  def __init__(self,
               oj: str = '',
               sid: str = '',
               cid: str = '',
               pid: str = '',
               problem_url='',
               up_lang: str = '',
               template_alias: str = ''):
    self.oj = oj
    self.id = sid
    self.cid = cid
    self.pid = pid
    self.problem_url = problem_url
    self.up_lang = up_lang
    self.template_alias = template_alias
