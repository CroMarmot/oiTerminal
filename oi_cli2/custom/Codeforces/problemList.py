from typing import Any, Dict, List
from bs4 import BeautifulSoup
from tests.mock.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table
from rich.style import Style
from typing import TypedDict


class JsonResult(TypedDict):
  id: str
  name: str
  limit: str
  passed: str
  status: str


def html2json(html) -> List[Dict[str, Any]]: # TODO fix with JsonResult
  soup = BeautifulSoup(html, 'lxml')
  currentContestList = soup.find('div', class_='datatable')
  # print(currentContestList)
  trs: List[BeautifulSoup] = currentContestList.find_all('tr')
  ret = []
  for i in range(1, len(trs)):
    tds = trs[i].find_all('td')
    namediv = tds[1].div.div
    row = {
        "id": tds[0].get_text().strip(),
        "name": namediv.get_text().strip(),
        "limit": tds[1].find('div', class_="notice").get_text().strip(),
        "passed": tds[3].get_text().strip(),
        "status": ""
    }

    if 'class' in trs[i].attrs:
      classes: List[str] = trs[i].attrs['class']
      if 'accepted-problem' in classes:
        row["status"] = "AC"
      elif 'rejected-problem' in classes:
        row["status"] = "ERROR"

    if row['limit'].startswith('standard input/output'):
      row['limit'] = row['limit'][len('standard input/output'):].strip()

    ret.append(row)
  return ret


def printData(html: str, title: str):
  ret = html2json(html)
  table = Table(title=title)
  table.add_column("ID",  style="cyan", no_wrap=False)
  table.add_column("Name")
  table.add_column("Limit")
  table.add_column("Passed")
  for item in ret:
    style = Style()
    if item["status"] == "AC":
      style = Style(bgcolor="dark_green")
    elif item["status"] == "ERROR":
      style = Style(bgcolor="dark_red")
    table.add_row(
        item["id"],  # tds[0].get_text().strip(),
        item["name"],  # tds[0].get_text().strip(),
        item["limit"],  # tds[0].get_text().strip(),
        item["passed"],  # tds[0].get_text().strip(),
        style=style
    )

  console = Console()
  console.print(table)


def main(argv):
  http_util = MockHttpUtil()
  url = f'https://codeforces.com/contest/{argv[0]}'
  print(html2json(http_util.get(url).text))
  printData(http_util.get(url).text, title=f"Contest {url}")


if __name__ == '__main__':
  main(['1628'])
