import re

from bs4 import BeautifulSoup
from bs4 import element

from spider import config
from spider.config import Problem, Result
from spider.platforms.base import Base, BaseParser
from spider.utils import HtmlTag, HttpUtil


class ZOJParser(BaseParser):
    def __init__(self):
        self._static_prefix = 'http://acm.zju.edu.cn/onlinejudge/'
        self._script = """<style>
* {
    font-family: Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    font-size: 14px;
}
</style>"""

    def problem_parse(self, response, pid, url):
        problem = Problem()

        problem.remote_id = pid
        problem.remote_url = url
        problem.remote_oj = 'ZOJ'
        if not response:
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        website_data = response.text
        status_code = response.status_code

        if status_code != 200:
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        if re.search('No such problem', website_data):
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem

        soup = BeautifulSoup(website_data, 'lxml')
        problem.title = str(soup.find('span', attrs={'class': 'bigProblemTitle'}).get_text())
        match_groups = re.search(r'(\d* Second)', website_data)
        if match_groups:
            problem.time_limit = match_groups.group(1)
        match_groups = re.search(r'(\d* KB)', website_data)
        if match_groups:
            problem.memory_limit = match_groups.group(1)
        problem.special_judge = re.search(r'<font color="blue">Special Judge</font>',
                                          website_data) is not None
        problem.html = ''
        problem.html += self._script
        raw_html = soup.find('div', attrs={'id': 'content_body'})
        for tag in raw_html.children:
            if type(tag) == element.NavigableString:
                problem.html += str(tag)
            if type(tag) == element.Tag and tag.name not in ['center', 'hr']:
                if tag.name == 'a' and tag.get('href') == '/onlinejudge/faq.do#sample':
                    continue
                if tag.name == 'h2':
                    tag['style'] = HtmlTag.TagStyle.TITLE.value
                    if tag.get('class'):
                        tag['class'] += (HtmlTag.TagDesc.TITLE.value,)
                    else:
                        tag['class'] = (HtmlTag.TagDesc.TITLE.value,)
                elif tag.name == 'p' and tag.b and tag.b.string in ['Input', 'Output', 'Sample Input',
                                                                    'Sample Output']:
                    tag.b['style'] = HtmlTag.TagStyle.TITLE.value
                    if tag.get('class'):
                        tag.b['class'] += (HtmlTag.TagDesc.TITLE.value,)
                    else:
                        tag.b['class'] = (HtmlTag.TagDesc.TITLE.value,)
                else:
                    tag['style'] = HtmlTag.TagStyle.CONTENT.value
                    if tag.get('class'):
                        tag['class'] += (HtmlTag.TagDesc.CONTENT.value,)
                    else:
                        tag['class'] = (HtmlTag.TagDesc.CONTENT.value,)
                    HtmlTag.update_tag(tag, self._static_prefix)
                problem.html += str(tag)
        problem.status = Problem.Status.STATUS_SUCCESS
        return problem

    def result_parse(self, response):
        result = Result()

        if response is None or response.status_code != 200:
            result.status = Result.Status.STATUS_RESULT_ERROR
            return result
        website_data = response.text
        soup = BeautifulSoup(website_data, 'lxml')
        line = soup.find('table', attrs={'class': 'list'}).find('tr', attrs={'class': 'rowOdd'}).find_all(
            'td')
        if line:
            result.unique_key = line[0].string
            result.verdict_info = line[2].get_text().strip()
            result.execute_time = line[5].string + "ms"
            result.execute_memory = line[6].string + "KB"
            result.status = Result.Status.STATUS_RESULT_SUCCESS
        else:
            result.status = Result.Status.STATUS_RESULT_ERROR
        return result


class ZOJ(Base):
    def __init__(self, *args, **kwargs):
        self._req = HttpUtil(headers=config.default_headers, *args, **kwargs)

    @staticmethod
    def home_page_url():
        url = 'http://acm.zju.edu.cn/onlinejudge/'
        return url

    def is_login(self):
        url = 'http://acm.zju.edu.cn/onlinejudge/'
        res = self._req.get(url)
        if res and re.search(r'/onlinejudge/logout.do">Logout', res.text) is not None:
            return True
        return False

    def get_cookies(self):
        return self._req.cookies.get_dict()

    def set_cookies(self, cookies):
        if isinstance(cookies, dict):
            self._req.cookies.update(cookies)

    def login_website(self, account):
        if account and account.cookies:
            self._req.cookies.update(account.cookies)
        if self.is_login():
            return True
        login_link_url = 'http://acm.zju.edu.cn/onlinejudge/login.do'
        post_data = {'handle': account.username, 'password': account.password}
        self._req.post(url=login_link_url, data=post_data)
        return self.is_login()

    def account_required(self):
        return False

    def get_problem(self, pid, account=None):
        url = 'http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=' + pid
        res = self._req.get(url)
        return ZOJParser().problem_parse(res, pid, url)

    def submit_code(self, account, pid, language, code):
        if not self.login_website(account):
            return Result(Result.Status.STATUS_SPIDER_ERROR)
        problem_url = 'http://acm.zju.edu.cn/onlinejudge/showProblem.do?problemCode=' + str(pid)
        res = self._req.get(problem_url)
        if res is None:
            return Result(Result.Status.STATUS_SUBMIT_ERROR)

        problem_id = re.search(r'problemId=(\d*)"><font color="blue">Submit</font>', res.text).group(1)
        url = 'http://acm.zju.edu.cn/onlinejudge/submit.do?problemId=' + str(problem_id)
        post_data = {'languageId': str(language), 'problemId': str(pid), 'source': code}
        res = self._req.post(url=url, data=post_data)
        if res and res.status_code == 200:
            return Result(Result.Status.STATUS_SUBMIT_SUCCESS)
        return Result(Result.Status.STATUS_SUBMIT_ERROR)

    def find_language(self, account):
        if self.login_website(account) is False:
            return None
        url = 'http://acm.zju.edu.cn/onlinejudge/submit.do?problemId=1'
        languages = {}
        try:
            res = self._req.get(url)
            soup = BeautifulSoup(res.text, 'lxml')
            options = soup.find('select', attrs={'name': 'languageId'}).find_all('option')
            for option in options:
                languages[option.get('value')] = option.string
        finally:
            return languages

    def get_result(self, account, pid):
        url = 'http://acm.zju.edu.cn/onlinejudge/showRuns.do' \
              '?contestId=1&search=true&firstId=-1&lastId=-1&problemCode=' + \
              str(pid) + '&handle=' + account.username + '&idStart=&idEnd='

        return self.get_result_by_url(url=url)

    def get_result_by_rid_and_pid(self, rid, pid):
        url = 'http://acm.zju.edu.cn/onlinejudge/showRuns.do?contestId=1&search=true&fi' \
              'rstId=-1&lastId=-1&problemCode=&handle=&idStart=' + str(rid) + '&idEnd=' + str(rid)
        return self.get_result_by_url(url=url)

    def get_result_by_url(self, url):
        res = self._req.get(url)
        return ZOJParser().result_parse(res)

    def is_working(self):
        url = 'http://acm.zju.edu.cn/onlinejudge/'
        res = self._req.get(url)
        if res and re.search(r'<div class="welcome_msg">Welcome to ZOJ</div>', res.text):
            return True
        return False

    @staticmethod
    def is_accepted(verdict):
        return verdict == 'Accepted'

    @staticmethod
    def is_running(verdict):
        return verdict in ['Queuing', 'Compiling']

    @staticmethod
    def is_compile_error(verdict):
        return verdict == 'Compilation Error'
