import json
import logging
import os


# write through , read through
class JsonFileDB:
  file_path: str

  def __init__(self, file_path: str, logger: logging):
    # check exist
    # if not exist create
    self.file_path: str = file_path
    self.logger: logging = logger

  # 不支持class 实例, 需要 调用者处理实例和dict之间转换 出入
  def save(self, col_name: str, obj: any) -> bool:
    if not os.path.exists(self.file_path):
      os.mknod(self.file_path)

    with open(self.file_path, "r") as json_file:
      try:
        data = json.load(json_file)
      except Exception as e:
        self.logger.exception(e)
        data = {}

    with open(self.file_path, "w") as json_file:
      data[col_name] = obj
      json.dump(data, json_file, indent=2)
    return True

  def load(self, col_name: str) -> any:
    if not os.path.exists(self.file_path):
      os.mknod(self.file_path)

    with open(self.file_path, "r") as json_file:
      try:
        data = json.load(json_file)
      except Exception as e:
        self.logger.exception(e)
        data = {}

      return data.get(col_name)
