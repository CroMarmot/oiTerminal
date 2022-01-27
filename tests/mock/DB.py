
class FakeDB:
  def __init__(self):
    self.store = {}

  def save(self, col_name: str, obj: any):
    self.store[col_name] = obj

  def load(self, col_name: str):
    return self.store.get(col_name)
