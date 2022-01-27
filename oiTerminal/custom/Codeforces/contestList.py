from typing import List
from urllib import request

from bs4 import BeautifulSoup
from oiTerminal.utils.HttpUtil import HttpUtil
from oiTerminal.utils.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table


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
    else:
      row["reg"] = regText
    ret.append(row)
  return ret


def getData(http_util: HttpUtil, url: str):
  res = http_util.get(url)
  # print(res.text)
  ret = html2json(res.text)
  table = Table(title="Current or upcoming contests")
  table.add_column("Name",  style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start", style="green")
  table.add_column("Length", style="green")
  table.add_column("Before Start", style="green")
  table.add_column("Reg", style="green")
  table.add_column("Cid", style="magenta")
  for item in ret:
    table.add_row(
        item["name"],  # tds[0].get_text().strip(),
        # item["writers"],  # tds[1].get_text().strip(),
        item["start"],  # tds[2].get_text().strip(),
        item["length"],  # tds[3].get_text().strip(),
        item["beforestart"],  # tds[4].get_text().strip(),
        item["reg"],  # tds[5].get_text().strip(),
        item["cid"],  # tds[5].get_text().strip(),
    )

  console = Console()
  console.print(table)


def main():
  # TODO
  getData(http_util=MockHttpUtil(), url='https://codeforces.com/contests')


if __name__ == '__main__':
  main()
