from oi_cli2.custom.Codeforces.CodeforcesParser import CodeforcesParser
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.utils.MockHttpUtil import MockHttpUtil
from oi_cli2.utils.HtmlTag import HtmlTag
from oi_cli2.utils.Logger import getLogger


def test_codeforces_parser():
  http_util = MockHttpUtil()
  test_doc: str = http_util.get('https://codeforces.com/contest/1628/problem/A').text

  parser = CodeforcesParser(html_tag=HtmlTag(
      MockHttpUtil()), logger=getLogger('/tmp/oiTerminal/test.log'))
  parse_problem_result = parser.problem_parse(test_doc)
  assert parse_problem_result.status == ParseProblemResult.Status.NOTVIS
  assert parse_problem_result.title == 'A+B (Trial Problem)'
  assert parse_problem_result.test_cases[0].in_data == '4\n1 5\n314 15\n-99 99\n123 987'
  assert parse_problem_result.test_cases[0].out_data == '6\n329\n0\n1110'
  assert parse_problem_result.time_limit == '2.0 s'
  assert parse_problem_result.mem_limit == '512 MB'
