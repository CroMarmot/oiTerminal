def Singleton(cls):
  __instances = {}

  def wrapper(*args, **kwargs):
    if cls not in __instances:
      __instances[cls] = cls(*args, **kwargs)
    return __instances[cls]

  return wrapper
