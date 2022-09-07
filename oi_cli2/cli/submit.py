import json
import logging
import os
import time
import traceback
import click
from rich.console import Console
from rich.text import Text
from oi_cli2.cli.constant import DEFAULT, FETCH_RESULT_INTERVAL, GREEN, STATE_FILE
import oi_cli2.core.provider as provider
from oi_cli2.core.DI import DI_ACCMAN,  DI_HTTP, DI_LOGGER, DI_TEMPMAN
from oi_cli2.model.Account import Account
from oi_cli2.model.Analyze import Analyze
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.model.FolderState import FolderState
from oi_cli2.model.Result import Result
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.HttpUtil import HttpUtil
from oi_cli2.utils.account import AccountManager
from oi_cli2.utils.consts.platforms import Platforms
from oi_cli2.utils.template import TemplateManager

console = Console(color_system='256', style=None)


def submit(
    core: BaseOj,
    pid: str,
    language: str,
    account: Account,
    file_path: str,
) -> Result:
  if not core.submit_code(pid=pid, language=language, code=file_path):
    raise Exception(f'submit failed, account={account.account}')
  print(f"{GREEN}Submitted{DEFAULT}")

  result = Result(Result.Status.PENDING)
  while result.cur_status in [Result.Status.RUNNING, Result.Status.PENDING]:
    print(f"Fetching result...({result.state_note})")
    time.sleep(FETCH_RESULT_INTERVAL)
    if result.quick_key != '':
      result = core.get_result_by_quick_id(result.quick_key)
    else:
      result = core.get_result(pid)
  return result


def submit_parser():
  am: AccountManager = provider.o.get(DI_ACCMAN)
  tm: TemplateManager = provider.o.get(DI_TEMPMAN)
  # get lang config
  if not os.path.isfile(STATE_FILE):
    raise Exception(f'STATE_FILE [{STATE_FILE}] NOT EXIST!')
  state_oj = FolderState()
  with open(STATE_FILE) as f:
    state_oj.__dict__ = json.load(f)

  oj = state_oj.oj
  up_lang = state_oj.up_lang

  template = tm.get_template_by_name(state_oj.oj, state_oj.template_alias)

  if template is None:
    logging.error(f'Template not found by [{state_oj.oj},{state_oj.template_alias}]')
    return False
  source_file_name = os.path.basename(template.path)
  code_file = os.path.join('.', source_file_name)
  if not os.path.isfile(code_file):
    raise Exception(f"code_file [{code_file}] NOT EXIST!")

  account = am.get_default_account(oj)
  return oj, state_oj.id, up_lang, account, code_file


def submit_main():
  logger: logging.Logger = provider.o.get(DI_LOGGER)
  ojname, pid, up_lang, account, code_path = submit_parser()
  http_util: HttpUtil = provider.o.get(DI_HTTP)
  console.print(f"OJ         : {ojname}")
  console.print(f"Account    : {account.account}")
  console.print(f"Problem ID : {pid}")
  console.print(f"up_lang    : {up_lang}")
  if ojname == Platforms.codeforces:
    try:
      from oi_cli2.custom.Codeforces.Codeforces import Codeforces
      oj: BaseOj = Codeforces(http_util=http_util, logger=logger, account=account, analyze=Analyze(), html_tag=HtmlTag(http_util))
    except Exception as e:
      logger.exception(e)
      raise e
  _result = submit(
      core=oj,
      pid=pid,
      language=up_lang,
      account=account,
      file_path=code_path,
  )
  console.print(f"Result ID  : {_result.id}")
  console.print(Text.from_ansi(f"Status     : {_result.status_string}"))
  console.print(f"Time       : {_result.time_note}")
  console.print(f"Memory     : {_result.mem_note}")


@click.command(name="submit")
def submit_command():
  try:
    logger: logging.Logger = provider.o.get(DI_LOGGER)
    submit_main()
  except KeyboardInterrupt:
    logger.info("Interrupt by user")
  except Exception:
    logger.error(traceback.format_exc())
