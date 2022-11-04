class Analyze:
  # TODO platform
  platform: str
  submit_lang: str
  template_alias: str
  class_path: str  # 实例class 文件
  default: bool

  def __init__(self):
    self.platform = ''
    self.submit_lang = ''
    self.template_alias = ''
    self.class_path = ''  # 实例class 文件
    self.default = False

  def initial(self, platform, submit_lang, template_alias, class_path, default=False):
    self.platform = platform
    self.submit_lang = submit_lang
    self.template_alias = template_alias
    self.class_path = class_path  # 实例class 文件
    self.default = default
    return self

  def dict_init(self, d):
    for key in ['platform', 'submit_lang', 'template_alias', 'class_path']:
      if key not in d:
        d[key] = ''
    self.__dict__ = d
    if not hasattr(self, 'default'):
      self.default = False
    return self

  def __repr__(self):
    return "<Analyze platform:%s template:%s>" % (self.platform, self.template_alias)

  def __str__(self):
    return f"Analyze({self.platform},{self.template_alias})"
