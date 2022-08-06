from bs4 import BeautifulSoup
from bs4 import element
import json

from oi_cli2.abstract.HtmlTagAbstract import HtmlTagAbstract
from oi_cli2.model.ParseProblemResult import ParseProblemResult
from oi_cli2.model.Problem import Problem
from oi_cli2.model.TestCase import TestCase
from oi_cli2.model.Contest import Contest
from oi_cli2.model.Result import Result


class CodeforcesParser:
  def __init__(self, html_tag: HtmlTagAbstract, logger=None):
    self.html_tag = html_tag
    self._logger = logger
    self._static_prefix = 'https://codeforces.com/'
    self._script = """
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
 showProcessingMessages: true,
 messageStyle: "none",
 extensions: ["tex2jax.js"],
 jax: ["input/TeX", "output/HTML-CSS"],
 tex2jax: {
     inlineMath:  [ ["$$$", "$$$"] ],
     displayMath: [ ["$$$$$$","$$$$$$"] ],
     skipTags: ['script', 'noscript', 'style', 'textarea', 'pre','code','a']
 },
 "HTML-CSS": {
     availableFonts: ["STIX","TeX"],
     showMathMenu: false
 }
});
</script>
<script src="https://cdn.bootcss.com/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML-full" async></script>
"""

  # fill problems field
  def contest_parse(self, contest: Contest, response: str):
    contest.problems.clear()
    soup = BeautifulSoup(response, 'lxml')
    match_groups = soup.find(name='table', attrs={'class': 'problems'})
    if match_groups:
      problems = match_groups.find_all(name='td', attrs={'class': 'id'})
      for each_problem in problems:
        pid = each_problem.get_text().strip(" \r\n")
        contest.problems[pid] = Problem(
            oj=contest.oj, pid=contest.id + pid)

  def problem_parse(self, response: str) -> ParseProblemResult:
    problem = ParseProblemResult()
    soup = BeautifulSoup(response, 'lxml')

    match_groups = soup.find('div', attrs={'class': 'title'})
    if match_groups:
      problem.title = str(match_groups.string)[2:].strip(" \r\n")

    match_groups = soup.find(name='div', attrs={'class': 'time-limit'})
    if match_groups:
      problem.time_limit = match_groups.contents[-1].strip()

    match_groups = soup.find(name='div', attrs={'class': 'memory-limit'})
    if match_groups:
      problem.mem_limit = match_groups.contents[-1].strip()

    match_groups = soup.find(
        name='div', attrs={'class': 'problem-statement'})

    # update url in html
    problem.html = ''
    if match_groups and isinstance(match_groups, element.Tag):
      for child in match_groups.children:
        if isinstance(child, element.Tag) and child.get('class') and set(child['class']).intersection(
                {'header'}):
          pass
        elif isinstance(child, element.Tag):
          for tag in child:
            if isinstance(tag, element.Tag):
              if tag.get('class') is None:
                tag['class'] = ()
              if tag.get('class') and set(tag['class']).intersection({'section-title'}):
                tag['class'] += (self.html_tag.TagDesc.TITLE.value,)
                tag['style'] = self.html_tag.TagStyle.TITLE.value
              else:
                tag['class'] += (self.html_tag.TagDesc.CONTENT.value,)
                tag['style'] = self.html_tag.TagStyle.CONTENT.value
          problem.html += str(self.html_tag.update_tag(child,
                              self._static_prefix))
        else:
          problem.html += str(self.html_tag.update_tag(child,
                              self._static_prefix))
    problem.html = '<html>' + problem.html + self._script + '</html>'
    problem.status = ParseProblemResult.Status.NOTVIS  # TODO for show progress

    match_groups = soup.find(name='div', attrs={'class': 'sample-test'})
    problem.test_cases.clear()
    if match_groups:
      test_case_inputs = match_groups.find_all(
          name='div', attrs={'class': 'input'})
      test_case_outputs = match_groups.find_all(
          name='div', attrs={'class': 'output'})
      assert (len(test_case_inputs) == len(test_case_outputs))
      for i in range(len(test_case_inputs)):
        t_in = test_case_inputs[i].find(
            name='pre').get_text("\n").strip(" \r\n")
        t_out = test_case_outputs[i].find(
            name='pre').get_text("\n").strip(" \r\n")
        problem.test_cases.append(TestCase(t_in, t_out))

    return problem

  # TODO codeforces's api won't change during a problem is testing, so i can't fetch the progress of testing
  # something like wss://pubsub.codeforces.com/ws/s_f496dfbd41a0b1ae37775f3f3bbaf806deb23ff4?_=1556834462081&tag=&time=&eventid=
  # https://github.com/xalanq/cf-tool/blob/d172e3f1c0c7ac6263fc09043071c3ccb5d0b1ff/client/watch.go
  #
  # JSON Example:
  # {
  #   "status": "OK",
  #   "result": [
  #     {
  #       "id": 53644184,
  #       "contestId": 1156,
  #       "creationTimeSeconds": 1556733400,
  #       "relativeTimeSeconds": 2147483647,
  #       "problem": {
  #         "contestId": 1156,
  #         "index": "D",
  #         "name": "0-1-Tree",
  #         "type": "PROGRAMMING",
  #         "tags": [
  #           "dfs and similar",
  #           "divide and conquer",
  #           "dp",
  #           "dsu"
  #         ]
  #       },
  #       "author": {
  #         "contestId": 1156,
  #         "members": [
  #           {
  #             "handle": "Cro-Marmot"
  #           }
  #         ],
  #         "participantType": "PRACTICE",
  #         "ghost": false,
  #         "startTimeSeconds": 1556721300
  #       },
  #       "programmingLanguage": "GNU C++17",
  #       "verdict": "OK",
  #       "testset": "TESTS",
  #       "passedTestCount": 73,
  #       "timeConsumedMillis": 234,
  #       "memoryConsumedBytes": 36864000
  #     }
  #   ]
  # }
  def result_parse(self, response: str) -> Result:
    ret = json.loads(response)
    result = Result(Result.Status.PENDING)
    if 'status' not in ret or ret['status'] != 'OK':
      raise ConnectionError(
          'Cannot connect to Codeforces! ' + json.dumps(ret))
    try:
      _result = ret['result'][0]
      result.id = _result['id']
      result.state_note = str(_result['passedTestCount'])
      result.time_note = str(_result['timeConsumedMillis']) + " MS"
      result.mem_note = str(_result['memoryConsumedBytes']) + " B"
      _verdict = _result.get('verdict')
      if _verdict in ['OK', 'Happy New Year!']:
        result.cur_status = Result.Status.AC
      elif _verdict in ['TESTING', None]:
        result.cur_status = Result.Status.RUNNING
      elif _verdict in ['WRONG_ANSWER']:
        result.cur_status = Result.Status.WA
      elif _verdict in ['RUNTIME_ERROR']:
        result.cur_status = Result.Status.RE
      elif _verdict in ['MEMORY_LIMIT_EXCEEDED']:
        result.cur_status = Result.Status.MLE
      elif _verdict in ['TIME_LIMIT_EXCEEDED']:
        result.cur_status = Result.Status.TLE
      elif _verdict in ['COMPILATION_ERROR']:
        result.cur_status = Result.Status.CE
      elif _verdict in ['IDLENESS_LIMIT_EXCEEDED']:
        result.cur_status = Result.Status.IDLE
      else:
        self._logger.warn("UNKNOWN STATE with " + _verdict)
        print("UNKNOWN STATE with " + _verdict)
        result.cur_status = Result.Status.PENDING
    except Exception as e:
      raise ConnectionError(
          'Cannot get latest submission, error:' + str(e))
    return result

  #  判断结果是否正确
  @staticmethod
  def is_accepted(verdict):
    return verdict in ['Accepted', 'Happy New Year!']

  # 判断是否编译错误
  @staticmethod
  def is_compile_error(verdict):
    return verdict == 'Compilation error'

  # 判断是否运行中
  @staticmethod
  def is_running(verdict):
    return verdict is None or str(verdict).startswith('Running on') or verdict == 'TESTING' or verdict == 'In queue'
