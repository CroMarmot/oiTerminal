from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
import bs4
from rich.console import Console
from rich.table import Table
from rich.style import Style

# TODO support different type table col
# https://codeforces.com/contest/1633/standings


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


def parseStandingHtml(html) -> Tuple[List[StandingRow], List[str]]:
  soup = BeautifulSoup(html, 'lxml')
  currentContestList = soup.find('div', class_='datatable')
  assert isinstance(currentContestList,bs4.Tag)
  ret: List[StandingRow] = []
  # print(currentContestList)
  trs: List[BeautifulSoup] = currentContestList.find_all('tr')
  ths: List[BeautifulSoup] = trs[0].find_all('th')
  h: List[str] = ['' for i in ths]  # head: get info from th
  for i in range(len(ths)):
    text = ths[i].get_text().strip()
    if text == '#':
      h[i] = 'rank'
    elif text == 'Who':
      h[i] = 'who'
    elif text == '=':
      h[i] = 'score'
    elif text == '*':
      h[i] = 'hack'
    elif text == 'Penalty':
      h[i] = 'penalty'
    else:
      a = ths[i].find('a')
      if a is not None:
        h[i] = a.get_text().strip()
  print(h)

  for i in range(1, len(trs) - 1):  # ignore first(head) and last line(total accepted TODO)
    tds = trs[i].find_all('td')
    row = StandingRow()
    for j in range(len(h)):
      if h[j] == 'rank':
        row.rank = tds[j].get_text().strip()
      elif h[j] == 'who':
        row.who = tds[j].get_text().strip()
      elif h[j] == 'score':
        row.score = tds[j].get_text().strip()
      elif h[j] == 'hack':
        row.hack = tds[j].get_text().strip()
      elif h[j] == 'penalty':
        row.penalty = tds[j].get_text().strip()
      else:  # problems
        passScore = tds[j].find_all('span', class_='cell-passed-system-test')
        problem = StandingProblem(id=h[j])
        if passScore and len(passScore) > 0:
          problem.score = passScore[0].get_text().strip()
          problem.time = tds[j].find('span', class_="cell-time").get_text().strip()
        else:
          problem.score = tds[j].get_text().strip()
        row.problems.append(problem)
    ret.append(row)

  # TODO add pagenation
  return ret, h


def printData(html: str, title: str, handle: str):
  # print(res.text)
  rows, head = parseStandingHtml(html)
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

    table.add_row(*row, style=Style(bgcolor="dark_green" if item.who == handle else None))

  console.print(table)
