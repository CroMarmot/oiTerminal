from datetime import datetime, timedelta
# from tests.mock.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table
from rich.style import Style

from ac_core.contest import ContestListPage

timeFmt = "%b/%d/%Y %H:%M"


def min2str(min: int) -> str:

  # prefix0
  _ = lambda v: f'0{v}'[-2:]

  if min <= 60:
    return _(min)
  if min <= 24 * 60:
    return f'{_(min//60)}:{_(min%60)}'
  return f'{min//60//24} day {_((min//60)%24)}:{_(min%60)}'


def full_url(url: str) -> str:
  return ('https://atcoder.jp' + url) if url.startswith('/') else url


def printData(cl: ContestListPage):
  # print(html)
  cur = cl.up_comming
  his = cl.recent
  console = Console()

  table = Table(title="Upcoming")
  table.add_column("Name", style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Before Start")
  table.add_column("Length")
  table.add_column("url", style="magenta")

  for item in cur:
    startTime = datetime.fromtimestamp(item.start_timestamp)
    timediff = startTime - datetime.now()
    table.add_row(
        item.name,
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        startTime.strftime(timeFmt),
        str(timedelta(days=timediff.days, seconds=timediff.seconds)) if timediff.days >= 0 else 'Started',
        min2str(item.duration),  # tds[3].get_text().strip(),
        full_url(item.url),  # tds[5].get_text().strip(),
    )

  console.print(table)

  # history
  table = Table(title="History contests (Recent 10)")
  table.add_column("Name", style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Length")
  table.add_column("url", style="magenta")

  for i in range(min(10, len(his))):
    item = his[i]
    table.add_row(
        item.name,  # tds[0].get_text().strip(),
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        datetime.fromtimestamp(item.start_timestamp).strftime(timeFmt),
        min2str(item.duration),  # tds[3].get_text().strip(),
        full_url(item.url),  # tds[5].get_text().strip(),
    )

  console.print(table)
