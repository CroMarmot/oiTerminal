import os
from shutil import copyfile


class FileUtil:

  @staticmethod
  def write(out_path: str, data: str):
    # if no folder create folder

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
      os.makedirs(directory)
    with open(out_path, "w") as file_ins:
      file_ins.write(data)
      file_ins.close()

  @staticmethod
  def copy(source_path: str, dest_path: str):
    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
      os.makedirs(directory)
    copyfile(source_path, dest_path)

  @staticmethod
  def read(out_path: str) -> str:
    assert False
    return f'TODO {out_path}'
