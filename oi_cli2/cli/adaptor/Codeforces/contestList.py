from datetime import datetime, timedelta
# from tests.mock.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table
from rich.style import Style

from codeforces_core.contest_list import ContestList

timeFmt = "%b/%d/%Y %H:%M"


def printData(cl: ContestList):
  # print(html)
  cur = cl.upcomming
  his = cl.history
  console = Console()

  table = Table(title="Current or upcoming contests")
  table.add_column("Name", style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Length")
  table.add_column("Before Start")
  table.add_column("Registered")
  table.add_column("Id", style="magenta")

  for item in cur:
    startTime = datetime.fromtimestamp(item.start)
    timediff = startTime - datetime.now()
    if not item.participants:  # 未开放注册
      bgcolor = None
    elif item.registered:  # 已注册
      bgcolor = 'dark_green'
    else:  # 开放注册,未注册
      bgcolor = 'grey30'
    table.add_row(
        item.title,
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        startTime.strftime(timeFmt),
        item.length,  # tds[3].get_text().strip(),
        str(timedelta(days=timediff.days, seconds=timediff.seconds)) if timediff.days >= 0 else 'Started',
        item.participants,  # tds[5].get_text().strip(),
        str(item.id),  # tds[5].get_text().strip(),
        style=Style(bgcolor=bgcolor))

  console.print(table)

  # history
  table = Table(title="History contests (Recent 10)")
  table.add_column("Name", style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Length")
  table.add_column("Registered")
  table.add_column("Id", style="magenta")

  for i in range(min(10, len(his))):
    item = his[i]
    table.add_row(
        item.title,  # tds[0].get_text().strip(),
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        datetime.fromtimestamp(item.start).strftime(timeFmt),
        item.length,  # tds[3].get_text().strip(),
        item.participants,  # tds[5].get_text().strip(),
        str(item.id),  # tds[5].get_text().strip(),
    )

  console.print(table)
