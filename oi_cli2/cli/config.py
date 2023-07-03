#!/usr/bin/env python3
import click
from oi_cli2.core.DI import DI_DB, DI_LOGGER
from oi_cli2.cli.constant import OT_FOLDER, USER_CONFIG_FILE
from oi_cli2.cli.template import template
from oi_cli2.cli.account import account
from oi_cli2.utils.configFolder import ConfigFolder
from oi_cli2.utils.db import JsonFileDB
from oi_cli2.utils.Provider2 import Provider2
import logging


@click.group()
@click.pass_context
def config(ctx) -> None:
  """Config environment """
  # TODO make it provider?
  config_folder = ConfigFolder(OT_FOLDER)
  try:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
  except Exception as e:
    print(str(e))
    exit(1)
  ctx.obj[DI_LOGGER] = logger
  ctx.obj[DI_DB] = JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE), logger=logger)


config.add_command(account)
config.add_command(template)
