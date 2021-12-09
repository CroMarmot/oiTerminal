import json
import re
import threading
import traceback

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

    def contest_parse(self, contest: Contest, response: str):
        contest.problems.clear()
        soup = BeautifulSoup(response, 'lxml')
        match_groups = soup.find(name='tbody').find_all(name='tr')
        for each_problem in match_groups:
            td = each_problem.find('td')
            pid = td.get_text().strip(" \r\n")
            contest.problems[pid] = Problem(oj=contest.oj, pid=contest.id + pid)

    def problem_parse(self, problem: Problem, response: str):
        soup = BeautifulSoup(response, 'lxml')

        match_groups = soup.find('span', attrs={'class': 'h2'})
        if match_groups:
            problem.title = ' - '.join(match_groups.get_text().split(' - ')[1:])

        match_groups = match_groups.find_next_sibling('p')
        # Time Limit: 2 sec / Memory Limit: 1024 MB
        if match_groups:
            result = re.match('^Time Limit: (.*)\/ Memory Limit: (.*)$', match_groups.get_text().strip(' \n\t'))
            try:
                problem.time_limit = result.group(1)
                problem.mem_limit = result.group(2)
            except:
                print(traceback.print_exc())

        # match_groups = soup.find(name='div', attrs={'id': 'task-statement'})
        match_groups = soup.find(name='span', attrs={'class': 'lang-en'})
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
        problem.status = Problem.Status.NOTVIS

        problem.test_cases = []
        # match_groups = soup.find(name='span', attrs={'class': 'lang-en'})
        lang_en_str = str(match_groups)
        in_test = re.findall('Sample Input \d</h3><pre>(.*?)</pre>', lang_en_str, flags=re.MULTILINE | re.DOTALL)
        out_test = re.findall('Sample Output \d</h3><pre>(.*?)</pre>', lang_en_str, flags=re.MULTILINE | re.DOTALL)
        assert len(in_test) == len(out_test)
        for idx in range(len(in_test)):
            t_in = in_test[idx].strip(" \r\n")
            t_out = out_test[idx].strip(" \r\n")
            problem.test_cases.append(TestCase(t_in, t_out))
        return problem

    # title=\"Compilation Error\"\u003eCE\u003c/span\u003e\u003c/td\u003e","Score":"0"
    def result_parse(self, response: str) -> Result:
        result = Result(Result.Status.PENDING)
        r = re.search('title=\\\\"(.*?)\\\\".*","Score":"(\d+)"', response)
        result.state_note = r.group(2) + ' score'

        _verdict = r.group(1)
        if _verdict in ['Accepted']:
            result.cur_status = Result.Status.AC
        elif _verdict in ['Wrong Answer']:
            result.cur_status = Result.Status.WA
        elif _verdict in ['Compilation Error']:
            result.cur_status = Result.Status.CE
        elif _verdict in ['Waiting for Judging', 'Judging']:
            result.cur_status = Result.Status.RUNNING
        elif _verdict in ['Runtime Error']:
            result.cur_status = Result.Status.RE
        elif _verdict in ['Time Limit Exceeded']:
            result.cur_status = Result.Status.TLE
        else:
            print("UNKNOWN with [" + _verdict + "]")
            print("UNKNOWN with [" + response + "]")
            result.cur_status = Result.Status.PENDING

        r = re.search('([0-9]+ ms)', response)
        if r is not None:
            result.time_note = r.group(1)
        else:
            result.time_note = "? MS"

        r = re.search('([0-9]+ KB)', response)
        if r is not None:
            result.mem_note = r.group(1)
        else:
            result.mem_note = "? KB"
        return result


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

    def get_contest(self, cid: str) -> Contest:
        response = self._req.get(url='https://atcoder.jp/contests/' + cid + "/tasks")
        ret = Contest(oj=AtCoder.__name__, cid=cid)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception(f"Fetch Contest Error,cid={cid}")
        print("get contest:" + cid)
        AtCoderParser().contest_parse(contest=ret, response=response.text)
        threads = []
        for pid in ret.problems.keys():
            # self.get_problem(pid=cid + pid, problem=ret.problems[pid])
            t = threading.Thread(target=self.get_problem, args=(cid + pid, ret.problems[pid]))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return ret

    # https://atcoder.jp/contests/tenka1-2019-beginner/tasks/tenka1_2019_a
    # it's unregular so go contests page first
    # example: tenkal-2019-beginner_A
    def get_problem(self, pid: str, problem: Problem = None) -> Problem:
        result = re.match('^(.+)([A-Z])$', pid)
        if result is None:
            raise Exception(f'problem id[{ pid }] ERROR')

        url = 'https://atcoder.jp/contests/' + result.group(1) + '/tasks'
        response = self._req.get(url=url)
        if response is None or response.status_code != 200 or response.text is None:
            raise Exception('atcoder fetch task ERROR:' + url)

        if problem is None:
            problem = Problem(oj=AtCoder.__name__, pid=pid, url=url)
        else:
            problem.url = url

        print("get problem:" + pid)
        soup = BeautifulSoup(response.text, 'lxml')
        problem_trs = soup.find('tbody').find_all('tr')
        for each_tr in problem_trs:
            tds = each_tr.find_all('td')
            for td in tds:
                if td.get_text() == result.group(2):
                    problem_url = 'https://atcoder.jp' + td.a.get('href')
                    print('problem url:' + problem_url)

                    res = self._req.get(url=problem_url)
                    if res is None or res.status_code != 200 or res.text is None:
                        raise Exception('problem fetch error:' + problem_url)
                    return AtCoderParser().problem_parse(problem, res.text)

        raise Exception('Not Find Problem:' + pid)

    # data.TaskScreenName: abc101_a
    # data.LanguageId: 3005
    # sourceCode: '# include <bits/stdc++.h>....'
    # csrf_token: '....'
    # <option value="abc101_a">A
    def submit_code(self, pid: str, language: str, code: str) -> bool:
        result = re.match('^(.+)([A-Z])$', pid)
        if result is None:
            raise Exception('problem id[' + pid + '] ERROR')

        res = self._req.get('https://atcoder.jp/contests/' + result.group(1) + '/submit')
        if res is None:
            raise Exception(f"submit_code: cannot open problem,pid={pid},language={language}")
        soup = BeautifulSoup(res.text, 'lxml')
        csrf_token = soup.find('input', attrs={'name': 'csrf_token'})['value']
        r = re.search('<option value="([^"]*?)">' + result.group(2), str(soup), re.DOTALL)
        post_data = {
            'csrf_token': csrf_token,
            'data.TaskScreenName': r.group(1),
            'data.LanguageId': language,
            'sourceCode': open(code, 'rb').read(),
        }
        url = 'https://atcoder.jp/contests/' + result.group(1) + '/submit'
        res = self._req.post(url, data=post_data)
        if res and res.status_code == 200:
            return True
        return False

    # https://atcoder.jp/contests/abc101/submissions/me?f.Task=abc101_a
    # <a href='/contests/abc101/submissions/5371227'>Detail</a>
    # https://atcoder.jp/contests/abc101/submissions/me/status/json?sids[]=5371077
    def get_result(self, pid) -> Result:
        result = re.match('^(.+)([A-Z])$', pid)
        if result is None:
            raise Exception('problem id[' + pid + '] ERROR')

        res = self._req.get('https://atcoder.jp/contests/' + result.group(1) + '/submit')
        if res is None:
            raise Exception(f"submit_code: cannot open problem,pid={pid}")
        soup = BeautifulSoup(res.text, 'lxml')
        r = re.search('<option value="([^"]*?)">' + result.group(2), str(soup), re.DOTALL)
        request_url = 'https://atcoder.jp/contests/' + result.group(1) + '/submissions/me?f.Task=' + r.group(1)
        res = self._req.get(request_url)
        if res is None:
            raise Exception(f"submit_code: cannot open problem,pid={pid}")
        soup = BeautifulSoup(res.text, 'lxml')
        # <a href='/contests/abc101/submissions/5371227'>Detail</a>
        r = re.search('<td class="text-center">.*?"/contests/(.*?)/submissions/(\d*?)\">Detail</a>', str(soup),
                      re.DOTALL | re.MULTILINE)
        url = 'https://atcoder.jp/contests/' + r.group(1) + '/submissions/me/status/json?sids[]=' + r.group(2)
        print(url)
        return self._get_result_by_url(url)

    def get_result_by_quick_id(self, quick_id: str) -> Result:
        return self._get_result_by_url(quick_id)

    def _get_result_by_url(self, url: str) -> Result:
        response = self._req.get(url=url)
        if response is None or response.status_code is not 200 or response.text is None:
            raise Exception(f'get result Failed,url={url}')
        ret = AtCoderParser().result_parse(response=response.text)
        ret.quick_key = url
        return ret

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
        return True  # 历史题目直接可看,比赛中题目报名后可看,需要 账号+报名
