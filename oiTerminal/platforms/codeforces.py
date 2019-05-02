import json
import re
from typing import List

from bs4 import BeautifulSoup
from bs4 import element

from oiTerminal.Model.LangKV import LangKV
from oiTerminal.platforms.base import Base, BaseParser
from oiTerminal.utils import HtmlTag, HttpUtil, logger

from oiTerminal.Model.Account import Account
from oiTerminal.Model.Problem import Problem
from oiTerminal.Model.TestCase import TestCase
from oiTerminal.Model.Contest import Contest
from oiTerminal.Model.Result import Result


class CodeforcesParser(BaseParser):
    def __init__(self):
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
                contest.problems[pid] = Problem(oj=contest.oj, pid=contest.id + pid)

    def problem_parse(self, problem: Problem, response: str):
        soup = BeautifulSoup(response, 'lxml')

        match_groups = soup.find('div', attrs={'class': 'title'})
        if match_groups:
            problem.title = match_groups.string
            problem.title = str(problem.title)[2:]

        match_groups = soup.find(name='div', attrs={'class': 'time-limit'})
        if match_groups:
            problem.time_limit = match_groups.contents[-1]

        match_groups = soup.find(name='div', attrs={'class': 'memory-limit'})
        if match_groups:
            problem.memory_limit = match_groups.contents[-1]

        match_groups = soup.find(name='div', attrs={'class': 'problem-statement'})
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
                                tag['class'] += (HtmlTag.TagDesc.TITLE.value,)
                                tag['style'] = HtmlTag.TagStyle.TITLE.value
                            else:
                                tag['class'] += (HtmlTag.TagDesc.CONTENT.value,)
                                tag['style'] = HtmlTag.TagStyle.CONTENT.value
                    problem.html += str(HtmlTag.update_tag(child, self._static_prefix))
                else:
                    problem.html += str(HtmlTag.update_tag(child, self._static_prefix))
        problem.html = '<html>' + problem.html + self._script + '</html>'
        problem.status = Problem.Status.NOTVIS  # TODO for show progress

        match_groups = soup.find(name='div', attrs={'class': 'sample-test'})
        problem.test_cases.clear()
        if match_groups:
            test_case_inputs = match_groups.find_all(name='div', attrs={'class': 'input'})
            test_case_outputs = match_groups.find_all(name='div', attrs={'class': 'output'})
            assert (len(test_case_inputs) == len(test_case_outputs))
            for i in range(len(test_case_inputs)):
                t_in = test_case_inputs[i].find(name='pre').get_text("\n").strip(" \r\n")
                t_out = test_case_outputs[i].find(name='pre').get_text("\n").strip(" \r\n")
                problem.test_cases.append(TestCase(t_in, t_out))

    # JSON Example:
    # {"status": "OK", "result": [
    #    {"id": 51191707,
    #     "contestId": 1136,
    #     "creationTimeSeconds": 1552327705,
    #     "relativeTimeSeconds": 5605,
    #     "problem": {"contestId": 1136,
    #                 "index": "D",
    #                 "name": "Nastya Is Buying Lunch",
    #                 "type": "PROGRAMMING",
    #                 "points": 2000.0,
    #                 "rating": 1800,
    #                 "tags": ["greedy"]},
    #     "author": {"contestId": 1136,
    #                "members": [{"handle": "Cro-Marmot"}],
    #                "participantType": "CONTESTANT",
    #                "ghost": false,
    #                "room": 56,
    #                "startTimeSeconds": 1552322100},
    #     "programmingLanguage": "GNU C++17",
    #     "verdict": "OK",
    #     "testset": "TESTS",
    #     "passedTestCount": 70,
    #     "timeConsumedMillis": 390,
    #     "memoryConsumedBytes": 15052800}]}
    def result_parse(self, result: Result, response: str):
        if response is None:
            return Result(Result.Status.STATUS_RESULT_ERROR)
        ret = response.json()
        result = Result()
        if 'status' not in ret or ret['status'] != 'OK':
            raise ConnectionError('Cannot connect to Codeforces! ' + json.dumps(ret))
        try:
            _result = ret['result'][0]
            result.unique_key = _result['id']
            result.verdict_info = _result.get('verdict')
            result.execute_time = str(_result['timeConsumedMillis']) + " MS"
            result.execute_memory = str(_result['memoryConsumedBytes']) + " B"
            result.status = Result.Status.STATUS_RESULT_SUCCESS
        except Exception:
            raise ConnectionError('Cannot get latest submission, error')
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


class Codeforces(Base):
    _cookies: dict
    _account: Account

    def __init__(self, *args, **kwargs):
        self._req = HttpUtil(*args, **kwargs)

    def login_website(self, account: Account) -> int:
        # TODO add method cookie login and save cookies in db/json
        # enable cookies login with db/json saved cookies
        #
        # return self._req.cookies.get_dict()
        # if isinstance(cookies, dict):
        #     self._req.cookies.update(cookies)
        try:
            res = self._req.get('https://codeforces.com/enter?back=%2F')

            soup = BeautifulSoup(res.text, 'lxml')
            csrf_token = soup.find(attrs={'name': 'X-Csrf-Token'}).get('content')
            post_data = {
                'csrf_token': csrf_token,
                'action': 'enter',
                'ftaa': '',
                'bfaa': '',
                'handleOrEmail': account.username,
                'password': account.password,
                'remember': []
            }
            self._req.post(url='https://codeforces.com/enter', data=post_data)
        except Exception as e:
            logger.exception(e)
        if self._is_login():
            account.cookie = self._req.cookies.get_dict()  # outer can get and save cookie from user
            self._account = account
            return 60 * 20
        else:
            return -60

    def _is_login(self) -> bool:
        res = self._req.get('https://codeforces.com')
        if res and re.search(r'logout">Logout</a>', res.text):
            return True
        return False

    @staticmethod
    def account_required() -> bool:
        return False

    def get_contest(self, cid: str) -> Contest:
        if re.match('^\d+$', cid) is None:
            raise Exception('contest id [' + cid + '] ERROR')

        response = self._req.get(url='https://codeforces.com/contest/' + cid)
        ret = Contest(oj=Codeforces.__name__, cid=cid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception("Fetch Contest Error")
        print("get contest:" + cid)
        CodeforcesParser().contest_parse(contest=ret, response=response.text)
        # TODO thread fetch ?
        for pid in ret.problems.keys():
            # TODO which is better
            # ret.problems[pid] = self.get_problem(pid=cid + pid)
            self.get_problem(pid=cid + pid, problem=ret.problems[pid])
        return ret

    def get_problem(self, pid: str, problem: Problem = None) -> Problem:
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            raise Exception('problem id[' + pid + '] ERROR')
        url = 'https://codeforces.com/contest/' + result.group(1) + '/problem/' + result.group(2)
        if problem is None:
            print('from none')
            problem = Problem(oj=Codeforces.__name__, pid=pid, url=url)
        else:
            print('from arg')
            problem = Problem(oj=Codeforces.__name__, pid=pid, url=url)
            problem.url = url
        response = self._req.get(url=url)
        print("get problem:" + pid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception("Fetch Problem Error")
        CodeforcesParser().problem_parse(problem=problem, response=response.text)
        return problem

    def submit_code(self, pid, language, code) -> bool:
        print(account.username + " Login")
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            return Result(Result.Status.STATUS_RESULT_ERROR)

        res = self._req.get('https://codeforces.com/contest/' + result.group(1) + '/submit')
        if res is None:
            return Result(Result.Status.STATUS_SPIDER_ERROR)
        soup = BeautifulSoup(res.text, 'lxml')
        csrf_token = soup.find(attrs={'name': 'X-Csrf-Token'}).get('content')
        post_data = {
            'csrf_token': csrf_token,
            'ftaa': '',
            'bfaa': '',
            'action': 'submitSolutionFormSubmitted',
            'contestId': result.group(1),
            'submittedProblemIndex': result.group(2),
            'programTypeId': language,
            'source': open(code, 'rb').read(),
            'tabSize': 0,
            'sourceFile': '',
        }
        url = 'https://codeforces.com/contest/' + result.group(1) + '/submit?csrf_token=' + csrf_token
        res = self._req.post(url, data=post_data)
        if res and res.status_code == 200:
            return Result(Result.Status.STATUS_SUBMIT_SUCCESS)
        return Result(Result.Status.STATUS_SUBMIT_ERROR)

    # TODO 可能换成 题目页面右侧 获取?
    def get_result(self, pid: str) -> Result:
        return self._get_result_by_url(
            'https://codeforces.com/api/user.status?handle=' + self._account.username + '&count=1')

    def get_result_by_quick_id(self, quick_id: str) -> Result:
        ret = self._get_result_by_url(
            'https://codeforces.com/api/user.status?handle=' + self._account.username + '&count=1')
        if ret.status == Result.Status.STATUS_RESULT_SUCCESS and ret.unique_key != unique_key:
            return Result(Result.Status.STATUS_RESULT_ERROR)
        return ret

    def _get_result_by_url(self, url: str) -> Result:
        res = self._req.get(url=url)
        return CodeforcesParser().result_parse(response=res)

    def get_language(self) -> LangKV:
        res = self._req.get('https://codeforces.com/problemset/submit')
        website_data: str = res.text
        ret: LangKV = LangKV()
        if website_data:
            soup = BeautifulSoup(website_data, 'lxml')
            tags = soup.find('select', attrs={'name': 'programTypeId'})
            if tags:
                for child in tags.find_all('option'):
                    ret.set(child.get('value'), child.string)
        return ret

    def _assert_working(self):
        if self._req.get('https://codeforces.com').status_code != 200:
            raise Exception('https://codeforces.com not working')

    @staticmethod
    def support_contest():
        return True
