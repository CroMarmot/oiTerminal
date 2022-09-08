import datetime
from oi_cli2.custom.Codeforces.contestList import html2json
from tests.mock.MockHttpUtil import MockHttpUtil


def test_codeforces_parser():
  http_util = MockHttpUtil()
  url = 'https://codeforces.com/contests'
  curResult, hisResult = html2json(http_util.get(url).text)
  assert len(curResult) == 7
  assert len(hisResult) == 100

  assert curResult[0]['name'] == 'Codeforces Round #768 (Div. 1)'
  assert curResult[0]['writers'] == 'BrayanD,dmga44,humbertoyusta'
  assert curResult[0]['start'] == datetime.datetime(2022, 1, 27, 14, 35)
  assert curResult[0]['length'] == '02:00'
  assert 'beforestart' not in curResult[0]
  assert curResult[0]['reg'] is not None
  assert curResult[0]['cid'] == '1630'

  assert hisResult[0]['name'] == 'Codeforces Round #767 (Div. 1)'
  assert hisResult[0]['writers'] == 'SlavicG,magnus.hegdahl'
  assert hisResult[0]['start'] == datetime.datetime(2022, 1, 22, 14, 35)
  assert hisResult[0]['length'] == '02:00'
  assert hisResult[0]['registered'] is not None
  assert hisResult[0]['cid'] == '1628'
