import os

# recursive search folder_name in dirpath and it's parent path


class ConfigFolder(object):

  def __init__(self, folder_name: str):
    self.folder_name = folder_name

  def get_root_folder(self):
    abs_path = os.path.abspath("./")
    while True:
      test_dir_path = os.path.join(abs_path, self.folder_name)
      if os.path.isdir(test_dir_path):
        return abs_path
      parent_path = os.path.abspath(os.path.join(abs_path, os.pardir))
      # Root folder's parent = Root folder
      if parent_path == abs_path:
        return None
      abs_path = parent_path

  def get_config_file_path(self, file_path: str):
    abs_folder = self.get_root_folder()
    if abs_folder is None:
      raise Exception('Not a oi folder, please run `oi init` first')
    return os.path.join(abs_folder, self.folder_name, file_path)

  def get_file_path(self, file_path: str):
    abs_folder = self.get_root_folder()
    if abs_folder is None:
      raise Exception('Not a oi folder, please run `oi init` first')

    return os.path.join(abs_folder, file_path)
