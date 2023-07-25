import asyncio
import json
import logging
import os
import traceback
from typing import Tuple, cast
import click
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.live import Live

from oi_cli2.cli.adaptor.ojman import OJManager
from oi_cli2.cli.constant import FETCH_RESULT_INTERVAL, STATE_FILE
from oi_cli2.core.DI import DI_ACCMAN, DI_LOGGER, DI_TEMPMAN
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.FolderState import FolderState
from oi_cli2.model.Result import SubmissionResult, status_string
from oi_cli2.utils.Provider2 import Provider2
from oi_cli2.utils.account import AccountManager
from oi_cli2.utils.template import TemplateManager

console = Console(color_system='256', style=None)


def generate_submission_table(res: SubmissionResult) -> Table:
  """Make a new submission table."""
  table = Table().grid()
  table.add_column(min_width=12)
  table.add_column()
  table.add_row("Result ID", f"{res.id}")
  # "[red]ERROR" if value < 50 else "[green]SUCCESS"
  table.add_row("Status", Text.from_ansi(f"{status_string(res)}"))
  table.add_row("Time", f"{res.time_note}")
  table.add_row("Memory", f"{res.mem_note}")
  if res.msg_txt:
    table.add_row("MSG", f"{res.msg_txt}")
  if res.url:
    table.add_row("Url", f"{res.url}")
  return table


def watch_result(oj: BaseOj, problem_url: str) -> SubmissionResult:
  return asyncio.run(async_watch_result(oj, problem_url))


async def async_watch_result(oj: BaseOj, problem_url: str) -> SubmissionResult:
  await oj.init()
  try:
    result = SubmissionResult()
    with Live(auto_refresh=False) as live:
      async for result in oj.async_get_result_yield(problem_url, time_gap=FETCH_RESULT_INTERVAL):
        live.update(generate_submission_table(result), refresh=True)
  except Exception as e:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
    logger.exception(e)
  await oj.deinit()
  return result


def submit_parser() -> Tuple[str, str, str, Account, str, str]:
  logger: logging.Logger = Provider2().get(DI_LOGGER)
  am: AccountManager = Provider2().get(DI_ACCMAN)
  tm: TemplateManager = Provider2().get(DI_TEMPMAN)
  # get lang config
  if not os.path.isfile(STATE_FILE):
    raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')
  state_oj = FolderState()
  with open(STATE_FILE) as f:
    state_oj.__dict__ = json.load(f)

  oj = state_oj.oj
  up_lang = cast(str, state_oj.up_lang)

  template = tm.get_template_by_name(state_oj.oj, state_oj.template_alias)

  if template is None:
    raise Exception(f'Template not found by [{state_oj.oj},{state_oj.template_alias}]')
  source_file_name = os.path.basename(template.path)
  code_file = os.path.join('.', source_file_name)
  if not os.path.isfile(code_file):
    raise Exception(f"code_file [{code_file}] NOT EXIST!")

  account = am.get_default_account(oj)
  return oj, state_oj.id, up_lang, account, code_file, state_oj.problem_url


@click.command(name="submit")
def submit_command() -> None:
  try:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
    platform, sid, up_lang, account, code_path, problem_url = submit_parser()

    table = Table().grid()
    table.add_column(min_width=12)
    table.add_column()
    table.add_row("OJ", f"{platform}")
    table.add_row("Account", f"{account.account}")
    table.add_row("Problem ID", f"{sid}")
    table.add_row("up_lang", f"{up_lang}")
    console.print(table)

    try:
      oj: BaseOj = OJManager.createOj(platform=platform, account=account, provider=Provider2())
    except Exception as e:
      logger.exception(e)
      raise e

    if not oj.submit_code(problem_url=problem_url, language_id=up_lang, code_path=code_path):
      raise Exception(f'submit failed, account={account.account}')
    console.print("[green]Submitted")
    watch_result(oj, problem_url)
  except KeyboardInterrupt:
    logger.info("Interrupt by user")
  except Exception:
    logger.error(traceback.format_exc())


@click.command(name="result")
def result_command() -> None:
  logger: logging.Logger = Provider2().get(DI_LOGGER)
  platform, sid, up_lang, account, code_path, problem_url = submit_parser()
  table = Table().grid()
  table.add_column(min_width=12)
  table.add_column()
  table.add_row("OJ", f"{platform}")
  table.add_row("Account", f"{account.account}")
  table.add_row("Problem ID", f"{sid}")
  table.add_row("up_lang", f"{up_lang}")
  table.add_row("Problem Url", f"{problem_url}")
  console.print(table)

  try:
    oj: BaseOj = OJManager.createOj(platform=platform, account=account, provider=Provider2())
  except Exception as e:
    logger.exception(e)
    raise e

  logger.debug(problem_url)

  watch_result(oj, problem_url)
