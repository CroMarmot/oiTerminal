from dataclasses import dataclass, field
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.style import Style

# TODO support different type table col
# https://codeforces.com/contest/1633/standings
from codeforces_core.contest_standing import Standing


@dataclass
class StandingProblem:
  id: str = ''
  score: str = ''
  time: str = ''


@dataclass
class StandingRow:
  rank: str = ''
  who: str = ''
  passed: Optional[str] = None
  score: str = ''
  hack: str = ''
  penalty: str = ''
  problems: List[StandingProblem] = field(default_factory=lambda: [])


def printData(result: Standing, title: str, handle: str):
  # print(res.text)
  head = result.head
  rows = result.rows
  console = Console()

  table = Table(title=title)
  for h in head:
    if h == 'rank':
      table.add_column(h, style="cyan")
    else:
      table.add_column(h)

  for item in rows:
    row: List[str] = []
    for i in range(len(head)):
      # TODO reconstruct
      if head[i] == "rank":
        row.append(item.rank)
      elif head[i] == "who":
        row.append(item.who)
      elif head[i] == "hack":
        row.append(item.hack)
      elif head[i] == "score":
        row.append(item.score)
      elif head[i] == "penalty":
        row.append(item.penalty)

    for p in item.problems:
      if p.time:
        row.append(f"{p.score}({p.time})")
      else:
        row.append(p.score)

    table.add_row(*row, style=Style(bgcolor="dark_green" if item.who == handle or item.who == f'* {handle}' else None))

  console.print(table)
