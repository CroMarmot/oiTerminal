import re

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


class AtCoderParser(BaseParser):
    def __init__(self):
        self._static_prefix = 'https://atcoder.jp/'
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

    # TODO
    def contest_parse(self, contest: Contest, response: str):
        ret = {}
        soup = BeautifulSoup(response, 'lxml')
        match_groups = soup.find(name='tbody')
        if match_groups:
            problems = match_groups.find_all(name='tr')
            for each_problem in problems:
                ret.append(each_problem.get_text().strip(" \r\n"))
        return ret

    # TODO
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

    # TODO
    def result_parse(self, response: str) -> Result:
        if response is None or response.status_code != 200 or response.text is None:
            return Result(Result.Status.STATUS_RESULT_ERROR)
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table')
        tag = None
        if table:
            tag = table.find_all('tr')
        if tag:
            children_tag = tag[-1].find_all('td')
            if len(children_tag) > 9:
                result = Result()
                result.unique_key = children_tag[0].string
                result.verdict_info = ''
                for item in children_tag[4].stripped_strings:
                    result.verdict_info += str(item) + ' '
                result.verdict_info = result.verdict_info.strip(' ')
                result.execute_time = children_tag[5].string.strip(" \r\n")
                result.execute_memory = children_tag[6].string.strip(" \r\n")
                result.status = Result.Status.STATUS_RESULT_SUCCESS
                return result
        return Result(Result.Status.STATUS_RESULT_ERROR)


class AtCoder(Base):
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
            res = self._req.get('https://atcoder.jp/login')

            soup = BeautifulSoup(res.text, 'lxml')
            csrf_token = soup.find(attrs={'name': 'csrf_token'}).get('value')
            post_data = {
                'csrf_token': csrf_token,
                'username': account.username,
                'password': account.password,
            }
            self._req.post(url='https://atcoder.jp/login', data=post_data)
        except Exception as e:
            print("login:" + str(e))
            logger.exception(e)
        if self._is_login():
            account.cookie = self._req.cookies.get_dict()  # outer can get and save cookie from user
            self._account = account
            return 60 * 20
        else:
            return -60

    def _is_login(self):
        res = self._req.get('https://atcoder.jp')
        if res and re.search(r'Sign Out</a>', res.text):
            return True
        return False

    # TODO
    def get_contest(self, cid: str) -> Contest:
        url = 'https://atcoder.jp/contests/' + cid + "/tasks"
        response = self._req.get(url=url)
        contest = Contest(oj=AtCoder.__name__, cid=cid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception("Fetch Contest Error")
        problems = AtCoderParser().contest_parse(response.text)
        if problems is not None:
            contest.problem_set = {}
        for problem in problems:
            contest.problem_set[problem] = self.get_problem(cid + problem, account)
        return contest

    # TODO
    def get_problem(self, pid: str, account: Account = None) -> Problem:
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            return Problem(oj=AtCoder.__name__, pid=pid, status=Problem.Status.STATUS_ERROR)

        url = 'https://atcoder.jp/contest/' + result.group(1) + '/problem/' + result.group(2)
        response = self._req.get(url=url)
        problem = Problem(oj=AtCoder.__name__, pid=pid, url=url)
        if response is None or response.status_code != 200 or response.text is None:
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        return AtCoderParser().problem_parse(response.text, problem)

    # TODO
    def submit_code(self, pid: str, language: str, code: str) -> bool:
        if not self.login_website(account):
            return Result(Result.Status.STATUS_SPIDER_ERROR)
        print(account.username + " Login")
        result = re.match('^(\d+)([A-Z]\d?)$', pid)
        if result is None:
            return Result(Result.Status.STATUS_RESULT_ERROR)

        res = self._req.get('https://atcoder.jp/contest/' + result.group(1) + '/submit')
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
        url = 'https://atcoder.jp/contest/' + result.group(1) + '/submit?csrf_token=' + csrf_token
        res = self._req.post(url, data=post_data)
        if res and res.status_code == 200:
            return Result(Result.Status.STATUS_SUBMIT_SUCCESS)
        return Result(Result.Status.STATUS_SUBMIT_ERROR)

    # TODO
    def get_result(self, pid) -> Result:
        if self.login_website(account) is False:
            return Result(Result.Status.STATUS_RESULT_ERROR)
        request_url = 'https://atcoder.jp/problemset/status?friends=on'
        res = self._req.get(request_url)
        website_data = res.text
        if website_data:
            soup = BeautifulSoup(website_data, 'lxml')
            tag = soup.find('table', attrs={'class': 'status-frame-datatable'})
            if tag:
                list_tr = tag.find_all('tr')
                for tr in list_tr:
                    if isinstance(tr, element.Tag) and tr.get('data-submission-id'):
                        return self.get_result_by_url(
                            'https://atcoder.jp/contest/' + pid[:-1] + '/submission/' + tr.get('data-submission-id'))
        return Result(Result.Status.STATUS_RESULT_ERROR)

    # TODO
    def get_result_by_quick_id(self, quick_id: str) -> Result:
        pass

    def get_language(self) -> LangKV:
        res = self._req.get('https://atcoder.jp/contests/practice/submit')
        ret: LangKV = LangKV()
        if res.text:
            soup = BeautifulSoup(res.text, 'lxml')
            tags = soup.find('div', attrs={'id': 'select-lang-practice_1'}).find('select')
            if tags:
                for child in tags.find_all('option'):
                    ret[child.get('value')] = child.string
        return ret

    def _assert_working(self):
        if self._req.get('https://atcoder.jp').status_code != 200:
            raise Exception('https://atcoder.jp not working')

    @staticmethod
    def support_contest() -> bool:
        return True

    @staticmethod
    def account_required() -> bool:
        return False
