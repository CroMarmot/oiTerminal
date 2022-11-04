class Account:
  platform: str
  account: str
  password: str
  default: bool

  def __init__(self):
    self.platform = ''
    self.account = ''
    self.password = ''
    self.default = False

  def initial(self, platform, account, password, default=False):
    self.platform = platform
    self.account = account
    self.password = password
    self.default = default
    return self

  def dict_init(self, d):
    self.__dict__ = d
    if not hasattr(self, 'platform'):
      self.platform = ''
    if not hasattr(self, 'account'):
      self.account = ''
    if not hasattr(self, 'password'):
      self.password = ''
    if not hasattr(self, 'default'):
      self.default = False
    return self

  def __repr__(self):
    return "<Account platform:%s username:%s>" % (self.platform, self.account)

  def __str__(self):
    return f"Account({self.platform},{self.account},{self.default})"
