class Template:
  platform: str
  alias: str
  # relative
  path: str
  compilation: str
  execute: str
  clean: str
  default: bool
  uplang: str

  def __init__(self):
    self.platform = ''
    self.alias = ''
    self.path = ''
    self.compilation = ''
    self.execute = ''
    self.clean = ''  # deperated
    self.uplang = ''
    self.default = False

  # TODO 改成非 class 的 struct
  def initial(self, platform, alias, path, compilation, execute, uplang, default=False):
    self.platform = platform
    self.alias = alias
    self.path = path
    self.compilation = compilation
    self.execute = execute
    # self.clean = clean
    self.uplang = uplang
    self.default = default
    return self

  def dict_init(self, d):
    for key in ['platform', 'alias', 'path', 'compilation', 'execute', 'uplang']:
      if key not in d:
        d[key] = ''
    self.__dict__ = d
    if not hasattr(self, 'default'):
      self.default = False
    return self

  def __repr__(self):
    return "<Template alias:%s path:%s>" % (self.alias, self.path)

  def __str__(self):
    return f"Template({self.alias},{self.platform},{self.compilation})"
