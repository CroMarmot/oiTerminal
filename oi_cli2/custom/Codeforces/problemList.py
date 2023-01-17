from typing import List
from bs4 import BeautifulSoup
import bs4
from oi_cli2.model.ProblemMeta import E_STATUS, ProblemMeta


def html2struct(html: str) -> List[ProblemMeta]:
  soup = BeautifulSoup(html, 'lxml')
  currentContestList = soup.find('div', class_='datatable')
  assert isinstance(currentContestList, bs4.Tag)
  # print(currentContestList)
  trs: List[BeautifulSoup] = currentContestList.find_all('tr')
  ret = []
  for i in range(1, len(trs)):
    tds = trs[i].find_all('td')
    namediv = tds[1].div.div
    row = ProblemMeta(
        id=tds[0].get_text().strip(),
        name=namediv.get_text().strip(),
        passed=tds[3].get_text().strip(),
    )

    if 'class' in trs[i].attrs:
      classes: str = trs[i].attrs['class']  # mypy ?, List[str]
      if 'accepted-problem' in classes:
        row.status = E_STATUS.AC
      elif 'rejected-problem' in classes:
        row.status = E_STATUS.ERROR
    limit = tds[1].find('div', class_="notice").get_text().strip()
    if limit.startswith('standard input/output'):
      limit = limit[len('standard input/output'):].strip()
      try:
        t, m = limit.split(',')
        row.time_limit_msec = int(float(t.strip().split(' ')[0]) * 1000)
        row.memory_limit_kb = int(float(m.strip().split(' ')[0]) * 1000)
      except:
        pass

    ret.append(row)
  return ret