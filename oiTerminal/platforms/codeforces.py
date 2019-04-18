import json
import re

from bs4 import BeautifulSoup
from bs4 import element

from oiTerminal.model import Problem, Result, Account, TestCase, Contest
from oiTerminal.platforms.base import Base, BaseParser
from oiTerminal.utils import HtmlTag, HttpUtil, logger


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

    def contest_parse(self, response: str):
        ret = []
        soup = BeautifulSoup(response, 'lxml')
        match_groups = soup.find(name='table', attrs={'class': 'problems'})
        if match_groups:
            problems = match_groups.find_all(name='td', attrs={'class': 'id'})
            for each_problem in problems:
                ret.append(each_problem.get_text().strip(" \r\n"))
        return ret

    def problem_parse(self, response: str, problem: Problem):
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
        problem.status = Problem.Status.STATUS_SUCCESS

        match_groups = soup.find(name='div', attrs={'class': 'sample-test'})
        problem.test_case = []
        if match_groups:
            test_case_inputs = match_groups.find_all(name='div', attrs={'class': 'input'})
            test_case_outputs = match_groups.find_all(name='div', attrs={'class': 'output'})
            assert (len(test_case_inputs) == len(test_case_outputs))
            for i in range(len(test_case_inputs)):
                t_in = test_case_inputs[i].find(name='pre').get_text("\n").strip(" \r\n")
                t_out = test_case_outputs[i].find(name='pre').get_text("\n").strip(" \r\n")
                problem.test_case.append(TestCase(t_in, t_out))
        return problem

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
    def result_parse(self, response):
        if response is None or response.status_code != 200 or response.text is None:
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


class Codeforces(Base):
    def __init__(self, *args, **kwargs):
        self._req = HttpUtil(*args, **kwargs)

    # 主页链接
    @staticmethod
    def home_page_url() -> str:
        return 'https://codeforces.com/'

    def get_cookies(self):
        return self._req.cookies.get_dict()

    def set_cookies(self, cookies):
        if isinstance(cookies, dict):
            self._req.cookies.update(cookies)

    # 登录页面
    def login_website(self, account):
        if self.is_login():
            return True
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
        return self.is_login()

    # 检查登录状态
    def is_login(self):
        res = self._req.get('https://codeforces.com')
        if res and re.search(r'logout">Logout</a>', res.text):
            return True
        return False

    def account_required(self):
        return False

    # 获取比赛
    def get_contest(self, cid: str, account: Account = None):
        result = re.match('^\d+$', cid)
        if result is None:
            return Contest(oj=Codeforces.__name__, cid=cid)

        url = 'https://codeforces.com/contest/' + result.group()
        response = self._req.get(url=url)
        contest = Contest(oj=Codeforces.__name__, cid=cid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception("Fetch Contest Error")
        problems = CodeforcesParser().contest_parse(response.text)
        if problems is not None:
            contest.problem_set = {}
        for problem in problems:
            contest.problem_set[problem] = self.get_problem(cid + problem, account)
        return contest

    # 获取题目
    def get_problem(self, pid: str, account: Account = None):
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            return Problem(oj=Codeforces.__name__, pid=pid, status=Problem.Status.STATUS_ERROR)

        url = 'https://codeforces.com/contest/' + result.group(1) + '/problem/' + result.group(2)
        response = self._req.get(url=url)
        problem = Problem(oj=Codeforces.__name__, pid=pid, url=url)
        if response is None or response.status_code != 200 or response.text is None:
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        return CodeforcesParser().problem_parse(response.text, problem)

    # 提交代码
    def submit_code(self, account, pid, language, code):
        if not self.login_website(account):
            return Result(Result.Status.STATUS_SPIDER_ERROR)
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

    # 获取当然运行结果
    def get_result(self, account: str, pid: str):
        if self.login_website(account) is False:
            return Result(Result.Status.STATUS_RESULT_ERROR)
        return self.get_result_by_url('https://codeforces.com/api/user.status?handle=' + account.username + '&count=1')

    # 根据源OJ的运行id获取结构
    def get_result_by_rid_and_pid(self, account: Account, pid: str, unique_key: str):
        ret = self.get_result_by_url('https://codeforces.com/api/user.status?handle=' + account.username + '&count=1')
        if ret.status == Result.Status.STATUS_RESULT_SUCCESS and ret.unique_key != unique_key:
            return Result(Result.Status.STATUS_RESULT_ERROR)
        return ret

    # 根据源OJ的url获取结果
    def get_result_by_url(self, url: str):
        res = self._req.get(url=url)
        return CodeforcesParser().result_parse(response=res)

    # 获取源OJ支持的语言类型
    def find_language(self, account):
        if self.login_website(account) is False:
            return {}
        res = self._req.get('https://codeforces.com/problemset/submit')
        website_data = res.text
        languages = {}
        if website_data:
            soup = BeautifulSoup(website_data, 'lxml')
            tags = soup.find('select', attrs={'name': 'programTypeId'})
            if tags:
                for child in tags.find_all('option'):
                    languages[child.get('value')] = child.string
        return languages

    # 检查源OJ是否运行正常
    def is_working(self):
        return self._req.get('https://codeforces.com').status_code == 200

    @staticmethod
    def support_contest():
        return True

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
