import json
import re
import threading
import logging

from bs4 import BeautifulSoup
from bs4 import element

from oiTerminal.platforms.base import Base, BaseParser
from oiTerminal.utils import HtmlTag, HttpUtil, logger

from oiTerminal.Model.LangKV import LangKV
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
            problem.mem_limit = match_groups.contents[-1]

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

    # TODO codeforces's api won't change during a problem is testing, so i can't fetch zhe progress of testing
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
            raise ConnectionError('Cannot connect to Codeforces! ' + json.dumps(ret))
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
            else:
                logger.warn("UNKNOWN STATE with " + _verdict)
                print("UNKNOWN STATE with " + _verdict)
                result.cur_status = Result.Status.PENDING
        except Exception as e:
            raise ConnectionError('Cannot get latest submission, error:' + str(e))
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
        #
        # if account.cookie is not '':
        #     self._req.cookies.update(account.cookie)
        #     if self._is_login():
        #         return 20*60
        #     else:
        #         self._req.cookies.update()
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

    def get_tta(self) -> str:
        """
        This calculates protection value (_tta)
        Reversed from js
        """
        hstr = self._req.cookies.get('39ce7')
        total = 0
        for i, ch in enumerate(hstr):
            total = (total + (i + 1) * (i + 2) * ord(ch)) % 1009
            if i % 3 == 0:
                total += 1
            if i % 2 == 0:
                total *= 2

            if i > 0:
                total -= ord(hstr[i // 2]) // 2 * (total % 5)
            total = total % 1009
        return total

    def reg_contest(self, cid: str) -> bool:
        if re.match('^\d+$', cid) is None:
            raise Exception('contest id [' + cid + '] ERROR')
        response = self._req.get(url='https://codeforces.com/contestRegistration/' + cid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception(f"Reg Contest Error, cid={cid}")
        print("reg contest:" + cid)

        soup = BeautifulSoup(response.text, 'lxml')

        csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
        _tta = self.get_tta();
        post_data = {
            'csrf_token': csrf_token,
            'action': 'formSubmitted',
            'backUrl': '',
            'takePartAs': 'personal',
            '_tta': _tta,
        }
        self._req.post(url='https://codeforces.com/contestRegistration/' + cid, data=post_data)
        # return True except network error
        # TODO get more detail
        return True

    def get_contest(self, cid: str) -> Contest:
        logging.debug('get_contest'+cid)
        if re.match('^\d+$', cid) is None:
            raise Exception(f'contest id "{cid}" ERROR')

        response = self._req.get(url='https://codeforces.com/contest/' + cid)
        ret = Contest(oj=Codeforces.__name__, cid=cid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception(f"Fetch Contest Error,cid={cid}")
        print("get contest:" + cid)
        CodeforcesParser().contest_parse(contest=ret, response=response.text)
        threads = []
        for pid in ret.problems.keys():
            # self.get_problem(pid=cid + pid, problem=ret.problems[pid])
            t = threading.Thread(target=self.get_problem, args=(cid + pid, ret.problems[pid]))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return ret

    def get_problem(self, pid: str, problem: Problem = None) -> Problem:
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            raise Exception('problem id[' + pid + '] ERROR')
        url = 'https://codeforces.com/contest/' + result.group(1) + '/problem/' + result.group(2)
        if problem is None:
            problem = Problem(oj=Codeforces.__name__, pid=pid, url=url)
        else:
            problem.url = url
        response = self._req.get(url=url)
        print("get problem:" + pid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception(f"Fetch Problem Error, pid={pid}")
        CodeforcesParser().problem_parse(problem=problem, response=response.text)
        return problem

    def submit_code(self, pid: str, language: str, code: str) -> bool:
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            raise Exception("submit_code: WRONG pid[" + pid + "]")

        res = self._req.get(f'https://codeforces.com/contest/{result.group(1)}/submit')
        if res is None:
            raise Exception(f"submit_code: cannot open problem,pid={pid},language={language}")
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
            return True
        return False

    def get_result(self, pid: str) -> Result:
        return self._get_result_by_url(
            'https://codeforces.com/api/user.status?handle=' + self._account.username + '&count=1')

    def get_result_by_quick_id(self, quick_id: str) -> Result:
        return self._get_result_by_url(quick_id)

    def _get_result_by_url(self, url: str) -> Result:
        response = self._req.get(url=url)
        if response is None or response.status_code is not 200 or response.text is None:
            raise Exception(f'get result Failed,url={url}')
        ret = CodeforcesParser().result_parse(response=response.text)
        ret.quick_key = url
        return ret

    def get_language(self) -> LangKV:
        res = self._req.get('https://codeforces.com/problemset/submit')
        ret: LangKV = LangKV()
        if res.text:
            soup = BeautifulSoup(res.text, 'lxml')
            tags = soup.find('select', attrs={'name': 'programTypeId'})
            if tags:
                for child in tags.find_all('option'):
                    ret[child.get('value')] = child.string
        return ret

    def _assert_working(self):
        if self._req.get('https://codeforces.com').status_code != 200:
            raise Exception('https://codeforces.com not working')

    @staticmethod
    def account_required() -> bool:
        return False

    @staticmethod
    def support_contest() -> bool:
        return True
