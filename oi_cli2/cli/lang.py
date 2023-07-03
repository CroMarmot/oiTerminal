import logging
import click
from requests import ConnectTimeout, ReadTimeout
from rich.console import Console
from rich.table import Table

from oi_cli2.cli.adaptor.ojman import OJManager
from oi_cli2.core.DI import DI_ACCMAN, DI_LOGGER
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.account import AccountManager

console = Console(color_system='256', style=None)


@click.command(name="lang")
@click.argument('platform')
def lang_command(platform) -> None:
  logger: logging.Logger = Provider2().get(DI_LOGGER)
  am: AccountManager = Provider2().get(DI_ACCMAN)

  try:
    oj: BaseOj = OJManager.createOj(platform=platform,
                                    account=am.get_default_account(platform=platform),
                                    provider=Provider2())
  except Exception as e:
    logger.exception(e)
    raise e

  try:
    languages = oj.get_language()
  except (ReadTimeout, ConnectTimeout) as e:
    logger.error(f'Http Timeout[{type(e).__name__}]: {e.request.url}')
    return
  except Exception as e:
    logger.exception(e)
    return

  table = Table().grid()
  table.add_column('Lang')
  table.add_column('value')
  for k, v in languages.items():
    table.add_row(v, k)
  console.print(table)
