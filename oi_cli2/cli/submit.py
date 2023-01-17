import json
import logging
import os
import time
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
  table.add_row("Time(s)", f"{res.time_note}")
  table.add_row("Memory(KB)", f"{res.mem_note}")
  if res.msg_txt:
    table.add_row("MSG", f"{res.msg_txt}")
  if res.url:
    table.add_row("Url", f"{res.url}")
  return table


def watch_result(oj: BaseOj, problem_url: str) -> SubmissionResult:
  result = SubmissionResult()
  with Live(auto_refresh=False) as live:
    while result.cur_status in [SubmissionResult.Status.RUNNING, SubmissionResult.Status.PENDING]:
      # console.print(Text.from_ansi(f"Fetching result...({result.state_note})"))
      time.sleep(FETCH_RESULT_INTERVAL)
      if result.quick_key:
        result = oj.get_result_by_quick_id(result.quick_key)
      else:
        result = oj.get_result(problem_url)
      live.update(generate_submission_table(result), refresh=True)

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
def submit_command():
  try:
    logger: logging.Logger = Provider2().get(DI_LOGGER)
    platform, sid, up_lang, account, code_path, problem_url = submit_parser()
    console.print(f"OJ         : {platform}")
    console.print(f"Account    : {account.account}")
    console.print(f"Problem ID : {sid}")
    console.print(f"up_lang    : {up_lang}")

    try:
      oj: BaseOj = OJManager.createOj(platform=platform, account=account, provider=Provider2())
    except Exception as e:
      logger.exception(e)
      raise e

    if not oj.submit_code(problem_url=problem_url, language_id=up_lang, code_path=code_path):
      raise Exception(f'submit failed, account={account.account}')
    console.print("[green]Submitted")
    watch_result(oj, problem_url)
    # console.print(f"Result ID  : {res.id}")
    # console.print(Text.from_ansi(f"Status     : {status_string(res)}"))
    # console.print(f"Time       : {res.time_note}")
    # console.print(f"Memory     : {res.mem_note}")
  except KeyboardInterrupt:
    logger.info("Interrupt by user")
  except Exception:
    logger.error(traceback.format_exc())


@click.command(name="result")
def result_command():
  logger: logging.Logger = Provider2().get(DI_LOGGER)
  platform, sid, up_lang, account, code_path, problem_url = submit_parser()
  console.print(f"OJ         : {platform}")
  console.print(f"Account    : {account.account}")
  console.print(f"Problem ID : {sid}")
  console.print(f"up_lang    : {up_lang}")
  console.print(f"Problem_url: {problem_url}")

  try:
    oj: BaseOj = OJManager.createOj(platform=platform, account=account, provider=Provider2())
  except Exception as e:
    logger.exception(e)
    raise e

  logger.debug(problem_url)

  res = watch_result(oj, problem_url)
  # console.print(f"Result ID  : {res.id}")
  # console.print(Text.from_ansi(f"Status     : {status_string(res)}"))
  # console.print(f"Time(s)    : {res.time_note}")
  # console.print(f"Memory(KB) : {res.mem_note}")