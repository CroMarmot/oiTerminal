import json
import logging
import os
from typing import Any, Optional


# write through , read through
class JsonFileDB:
  file_path: str

  def __init__(self, file_path: str, logger: logging.Logger):
    # check exist
    # if not exist create
    self.file_path: str = file_path
    self.logger: logging.Logger = logger

  # 不支持class 实例, 需要 调用者处理实例和dict之间转换 出入
  def save(self, col_name: str, obj: Any) -> bool:
    if not os.path.exists(self.file_path):
      os.mknod(self.file_path)

    with open(self.file_path, "r") as json_file:
      try:
        data = json.load(json_file)
      except Exception:
        data = {}

    with open(self.file_path, "w") as json_file:
      data[col_name] = obj
      json.dump(data, json_file, indent=2)
    return True

  def load(self, col_name: str) -> Optional[Any]:
    if not os.path.exists(self.file_path):
      os.mknod(self.file_path)

    with open(self.file_path, "r") as json_file:
      try:
        data = json.load(json_file)
      except json.JSONDecodeError:  # empty file or wrong file, type(e).__name__
        data = {}
      except Exception as e:
        raise e

      return data.get(col_name)
