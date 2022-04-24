from datetime import datetime, timedelta
from typing import List

from bs4 import BeautifulSoup
from oiTerminal.utils.MockHttpUtil import MockHttpUtil
from rich.console import Console
from rich.table import Table
from rich.style import Style

from oiTerminal.utils.utc2local import moscow_to_utc, utc_to_local

timeFmt = "%b/%d/%Y %H:%M"


def html2json(html):
  soup = BeautifulSoup(html, 'lxml')
  currentContestList = soup.find('div', class_='datatable')
  hisContests = soup.find('div', class_="contests-table").find('div', class_='datatable')
  cur = []
  if currentContestList != hisContests:
    # print(currentContestList)
    trs: List[BeautifulSoup] = currentContestList.find_all('tr')
    for i in range(1, len(trs)):
      tds = trs[i].find_all('td')
      row = {
          "name": tds[0].get_text().replace('Enter »', '').strip(),
          "writers": tds[1].get_text().strip().replace('\n', ',').replace('\r', ',').replace(",,", ",").strip(),
          "start": moscow_to_utc(datetime.strptime(tds[2].get_text().strip(), timeFmt)),
          "length": tds[3].get_text().strip(),
          # "beforestart": tds[4].get_text().strip(),
          "reg": "",
          # data-contestId -> lowercase
          "cid": trs[i].attrs['data-contestid']
      }
      # if row["beforestart"].startswith("Before start"):
      #   row["beforestart"] = row["beforestart"][len("Before start"):].strip()

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
      cur.append(row)

  his = []
  trs: List[BeautifulSoup] = hisContests.find_all('tr')
  for i in range(1, len(trs)):
    tds = trs[i].find_all('td')
    # remove a tag
    alla = tds[0].find_all('a')
    for a in alla:
      a.decompose()
    # print(tds[0].children)
    row = {
        "name": tds[0].get_text().strip(),
        "writers": tds[1].get_text().strip().replace('\n', ',').replace('\r', ',').replace(",,", ",").strip(),
        "start": moscow_to_utc(datetime.strptime(
            tds[2].find('span', class_="format-time-only").get_text().strip(),
            timeFmt)),
        "length": tds[3].get_text().strip(),
        "registered": tds[5].get_text().strip(),
        # data-contestId -> lowercase
        "cid": trs[i].attrs['data-contestid']
    }
    his.append(row)

  return cur, his


def printData(html):
  # print(html)
  cur, his = html2json(html)
  console = Console()

  table = Table(title="Current or upcoming contests")
  table.add_column("Name",  style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Length")
  table.add_column("Before Start")
  table.add_column("Reg")
  table.add_column("Id", style="magenta")

  for item in cur:
    td = item['start'] - datetime.now()
    table.add_row(
        item["name"],  # tds[0].get_text().strip(),
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        utc_to_local(item["start"]).strftime(timeFmt),
        item["length"],  # tds[3].get_text().strip(),
        str(timedelta(days=td.days, seconds=td.seconds)) if td.days >= 0 else 'Started',
        item["reg"],  # tds[5].get_text().strip(),
        item["cid"],  # tds[5].get_text().strip(),
        style=Style(bgcolor=None if item["reg"].startswith("Before") else (
            "dark_green" if item["reg"].startswith("Registered") else "grey30"))
    )

  console.print(table)

  # history
  table = Table(title="History contests (Recent 5)")
  table.add_column("Name",  style="cyan", no_wrap=False)
  # table.add_column("Writers", style="magenta")
  table.add_column("Start")
  table.add_column("Length")
  table.add_column("Registered")
  table.add_column("Id", style="magenta")

  for i in range(min(5, len(his))):
    item = his[i]
    table.add_row(
        item["name"],  # tds[0].get_text().strip(),
        # item["writers"],  # tds[1].get_text().strip(),
        # https://strftime.org/
        # Jan/27/2022 17:35 tds[2].get_text().strip(),
        utc_to_local(item["start"]).strftime(timeFmt),
        item["length"],  # tds[3].get_text().strip(),
        item["registered"],  # tds[5].get_text().strip(),
        item["cid"],  # tds[5].get_text().strip(),
    )

  console.print(table)


def main():
  http_util = MockHttpUtil()
  url = 'https://codeforces.com/contests'
  printData(http_util.get(url).text)


if __name__ == '__main__':
  main()
