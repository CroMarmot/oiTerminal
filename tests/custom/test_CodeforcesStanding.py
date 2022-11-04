from oi_cli2.custom.Codeforces.standing import parseStandingHtml
from tests.mock.MockHttpUtil import MockHttpUtil


def test_standing_contest_1721():
  http_util = MockHttpUtil()
  url = f'https://codeforces.com/contest/1721/standings/friends/true'
  rows, head = parseStandingHtml(http_util.get(url).text)
  assert head == ['rank', 'who', 'score', 'penalty', 'hack', 'A', 'B', 'C', 'D', 'E', 'F']
  assert rows[7].rank == '8\xa0(259)'
  assert rows[7].who == 'Cro-Marmot'
  assert rows[7].score == '5'
  assert rows[7].penalty == '265'
  assert len(rows[7].problems) == 6
  assert rows[7].problems[1].id == 'B'
  assert rows[7].problems[1].score == '+1\n00:28'  # TODO split?


def test_standing_contest_1720():
  http_util = MockHttpUtil()
  url = f'https://codeforces.com/contest/1720/standings/friends/true'
  rows, head = parseStandingHtml(http_util.get(url).text)
  assert head == ['rank', 'who', 'score', 'hack', 'A', 'B', 'C', 'D1', 'D2', 'E']
