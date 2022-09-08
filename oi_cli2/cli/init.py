import os
import sys
import click
from oi_cli2.cli.constant import OT_FOLDER, USER_CONFIG_FILE
from oi_cli2.utils.configFolder import ConfigFolder


@click.command()
def init():
  """Init oi folder"""
  folder = OT_FOLDER
  config_folder = ConfigFolder(folder).get_root_folder()
  if config_folder is None:
    os.makedirs(folder)
    print(folder + ' Created, oi folder inited.')
    with open(".gitignore", 'a') as f:
      f.write(os.path.join(folder, USER_CONFIG_FILE))
  else:
    print(config_folder + '/.oiTerminal Exist', file=sys.stderr)
