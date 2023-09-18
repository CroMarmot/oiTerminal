from tests.mock.Logger import FakeLogger
from tests.mock.MockAioHttp import MockAioHttp

from oi_cli2.model.ParseProblemResult import ParsedProblemResult
from oi_cli2.model.TestCase import TestCase
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.cli.adaptor.Codeforces.Codeforces import Codeforces
from oi_cli2.model.Account import Account

host = 'https://codeforces.com'


def test_pid2url():
  problem_id = '1843F2'
  oj: BaseOj = Codeforces(http_util=MockAioHttp(host), logger=FakeLogger(), account=Account())
  assert oj.pid2url(problem_id) == 'https://codeforces.com/contest/1843/problem/F2'


def test_problem_by_id():
  problem_id = '1843F2'
  oj: BaseOj = Codeforces(http_util=MockAioHttp(host), logger=FakeLogger(), account=Account())
  result = oj.problem_by_id(problem_id)
  assert result.status == ParsedProblemResult.status.NOTVIS
  assert result.title == 'A+B (Trial Problem)'
  assert result.test_cases == [TestCase(in_data='4\n1 5\n314 15\n-99 99\n123 987', out_data='6\n329\n0\n1110')]
  assert result.id == '1843F2'
  assert result.oj == 'Codeforces'
  assert result.description == ''
  assert result.time_limit == '2.0 s'
  assert result.mem_limit == '512 MB'
  assert result.url == 'https://codeforces.com/contest/1843/problem/F2'
  assert len(result.html) == 47603
  assert result.file_path == '1843/F2'
