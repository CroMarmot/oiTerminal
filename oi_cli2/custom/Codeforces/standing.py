from typing import List

from bs4 import BeautifulSoup
from oi_cli2.utils.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table
from rich.style import Style

# TODO support different type table col
# https://codeforces.com/contest/1633/standings


def html2json(html):
  soup = BeautifulSoup(html, 'lxml')
  currentContestList = soup.find('div', class_='datatable')
  ret = []
  # print(currentContestList)
  trs: List[BeautifulSoup] = currentContestList.find_all('tr')
  ths = trs[0].find_all('th')
  problems = []
  for i in range(4, len(ths)):
    a = ths[i].find('a')
    if a is not None:
      problems.append(a.get_text().strip())

  for i in range(1, len(trs)-1):  # ignore last line
    tds = trs[i].find_all('td')
    row = {
        "rank": tds[0].get_text().strip(),
        "who": tds[1].get_text().strip(),
        "score": tds[2].get_text().strip(),
        "hack": tds[3].get_text().strip(),
    }
    for i in range(4, len(tds)):
      passScore = tds[i].find_all('span', class_='cell-passed-system-test')
      if i - 4 >= len(problems):
        break
      if passScore and len(passScore) > 0:
        row[problems[i - 4]] = passScore[0].get_text().strip()
        row["time_"+problems[i - 4]] = tds[i].find('span', class_="cell-time").get_text().strip()
        if row["time_"+problems[i - 4]] == "":
          del row["time_"+problems[i - 4]]
      else:
        row[problems[i - 4]] = tds[i].get_text().strip()

    ret.append(row)

  # TODO add pagenation
  return ret, problems


def printData(html: str, title: str, handle: str):
  # print(res.text)
  ret, problems = html2json(html)
  console = Console()

  table = Table(title=title)
  table.add_column("Rank",  style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Who")
  table.add_column("Score")
  table.add_column("Hack")
  for p in problems:
    table.add_column(p)

  for item in ret:
    args = [
        item["rank"],
        item["who"],
        item["score"],
        item["hack"],
    ]
    for p in problems:
      if "time_"+p in item:
        args.append(item[p]+"(" + item["time_"+p]+")")
      else:
        args.append(item[p])

    table.add_row(* args, style=Style(bgcolor="dark_green" if item["who"] == handle else None))

  console.print(table)


def main(argv):
  http_util = MockHttpUtil()
  url = f'https://codeforces.com/contest/{argv[0]}/standings/friends/true'
  printData(http_util.get(url).text, title="Friends Standing", handle="YeXiaoRain")


if __name__ == '__main__':
  main()
