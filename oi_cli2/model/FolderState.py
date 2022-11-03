class FolderState:
  _oj: str
  _id: str # string id 
  cid: str # contest id
  pid: str # problem id
  _up_lang: str
  _template_alias: str

  def __init__(self,
               oj: str = '',
               sid: str = '',
               cid: str = '',
               pid: str = '',
               lang: str = '',
               up_lang: str = '',
               template_alias: str = ''):
    self._oj = oj
    self._id = sid
    self.cid = cid
    self.pid = pid 
    self._up_lang = up_lang
    self._template_alias = template_alias

  @property
  def oj(self):
    return self._oj

  @oj.setter
  def oj(self, value):
    self._oj = value

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, value):
    self._id = value

  @property
  def up_lang(self):
    return self._up_lang

  @up_lang.setter
  def up_lang(self, value):
    self._up_lang = value

  @property
  def template_alias(self):
    return self._template_alias

  def __repr__(self):
    return "<Folder State: %s >" % (str(self.__dict__))

  def __str__(self):
    return "<Folder State: %s >" % (str(self.__dict__))
