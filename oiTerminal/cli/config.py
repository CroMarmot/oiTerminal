#!/usr/bin/env python3
import click
from oiTerminal.core.DI import DI_DB, DI_LOGGER
from oiTerminal.cli.constant import OT_FOLDER, OT_LOG, USER_CONFIG_FILE
from oiTerminal.cli.template import template
from oiTerminal.cli.account import account
from oiTerminal.utils.Logger import getLogger
from oiTerminal.utils.configFolder import ConfigFolder
from oiTerminal.utils.db import JsonFileDB
import logging


@click.group()
@click.pass_context
def config(ctx):
  """Config environment """
  # TODO make it provider?
  config_folder = ConfigFolder(OT_FOLDER)
  try:
    logger: logging = getLogger(config_folder.get_file_path(OT_LOG))
  except Exception as e:
    print(str(e))
    exit(1)
  ctx.obj[DI_LOGGER] = logger
  ctx.obj[DI_DB] = JsonFileDB(config_folder.get_config_file_path(USER_CONFIG_FILE), logger=logger)


config.add_command(account)
config.add_command(template)
