from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from oiTerminal.utils.HttpUtil import HttpUtil
from oiTerminal.utils.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table
from rich.style import Style

from oiTerminal.utils.utc2local import moscow_to_utc, utc_to_local


def html2json(html):
  soup = BeautifulSoup(html, 'lxml')
  currentContestList = soup.find('div', class_='datatable')
  # print(currentContestList)
  trs: List[BeautifulSoup] = currentContestList.find_all('tr')
  ret = []
  for i in range(1, len(trs)):
    tds = trs[i].find_all('td')
    row = {
        "name": tds[0].get_text().strip(),
        "writers": tds[1].get_text().strip().replace('\n', ',').replace('\r', ',').replace(",,", ",").strip(),
        "start": tds[2].get_text().strip(),
        "length": tds[3].get_text().strip(),
        "beforestart": tds[4].get_text().strip(),
        "reg": "",
        # data-contestId -> lowercase
        "cid": trs[i].attrs['data-contestid']
    }
    if row["beforestart"].startswith("Before start"):
      row["beforestart"] = row["beforestart"][len("Before start"):].strip()

    regText: str = tds[5].get_text().replace('\n', ' ').replace('\r', ' ').strip()
    if regText.startswith('Before registration'):
      row["reg"] = "Before " + regText[len('Before registration'):].strip()
    elif regText.startswith('Register »'):
      regText = regText[len('Register »'):].strip()
      if regText.endswith("*has extra registration"):
        regText = regText[:len(regText)-len("*has extra registration")]
      row["reg"] = regText
    elif regText.startswith("Registration completed"):
      row["reg"] = "Registered " + regText[len("Registration completed"):].strip()
    else:
      row["reg"] = regText
    ret.append(row)
  return ret


def printData(html):
  # print(res.text)
  ret = html2json(html)
  table = Table(title="Current or upcoming contests")
  table.add_column("Name",  style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Length")
  table.add_column("Before Start")
  table.add_column("Reg")
  table.add_column("Id", style="magenta")

  timeFmt = "%b/%d/%Y %H:%M"

  for item in ret:
    table.add_row(
        item["name"],  # tds[0].get_text().strip(),
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        utc_to_local(moscow_to_utc(datetime.strptime(item["start"], timeFmt))).strftime(timeFmt),
        item["length"],  # tds[3].get_text().strip(),
        item["beforestart"],  # tds[4].get_text().strip(),
        item["reg"],  # tds[5].get_text().strip(),
        item["cid"],  # tds[5].get_text().strip(),
        style=Style(bgcolor=None if item["reg"].startswith("Before") else (
            "dark_green" if item["reg"].startswith("Registered") else "grey30"))
    )

  console = Console()
  console.print(table)


def main():
  http_util = MockHttpUtil()
  url = 'https://codeforces.com/contests'
  printData(http_util.get(url).text)


if __name__ == '__main__':
  main()
