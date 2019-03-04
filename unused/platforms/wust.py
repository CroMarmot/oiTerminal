import re

from bs4 import BeautifulSoup
from bs4 import element

from spider import config
from spider.platforms.base import Base, BaseParser
from spider.config import Problem, Result
from spider.utils import HttpUtil, HtmlTag


class WUSTParser(BaseParser):
    def __init__(self, *args, **kwargs):
        self._static_prefix = 'http://acm.wust.edu.cn/'

    def problem_parse(self, response, pid, url):
        problem = Problem()
        problem.remote_id = pid
        problem.remote_url = url
        problem.remote_oj = 'WUST'
        if response is None:
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        website_data = response.text
        status_code = response.status_code
        if status_code != 200:
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        if re.search('Problem is not Available', website_data):
            problem.status = Problem.Status.STATUS_RETRYABLE
            return problem
        match_groups = re.search(r'[\d]{4,}: ([\s\S]*?)</h2>', website_data)
        if match_groups:
            problem.title = match_groups.group(1)
        match_groups = re.search(r'(\d* Sec)', website_data)
        if match_groups:
            problem.time_limit = match_groups.group(1)
        match_groups = re.search(r'(\d* MB)', website_data)
        if match_groups:
            problem.memory_limit = match_groups.group(1)
        problem.special_judge = re.search(r'class=red>Special Judge</span>', website_data) is not None

        soup = BeautifulSoup(website_data, 'lxml')

        problem.html = ''
        for tag in soup.find('div', attrs={'class': 'rich_text'}).children:
            if type(tag) == element.Tag:
                if tag.name in ['h2', 'div']:
                    if not tag.get('class'):
                        tag['class'] = ()
                    if tag.name == 'h2':
                        if tag.div:
                            tag.div.decompose()
                        if tag.img:
                            tag.img.decompose()
                        tag['style'] = HtmlTag.TagStyle.TITLE.value
                        tag['class'] += (HtmlTag.TagDesc.TITLE.value,)
                        problem.html += str(
                            HtmlTag.update_tag(tag, self._static_prefix, update_style=HtmlTag.TagStyle.TITLE.value))

                    else:
                        tag['style'] = HtmlTag.TagStyle.CONTENT.value
                        tag['class'] += (HtmlTag.TagDesc.CONTENT.value,)
                        problem.html += str(
                            HtmlTag.update_tag(tag, self._static_prefix,
                                               update_style=HtmlTag.TagStyle.CONTENT.value))
        problem.html = '<body>' + problem.html + '</body>'
        problem.status = Problem.Status.STATUS_SUCCESS
        return problem

    def result_parse(self, response):
        result = Result()
        if response is None or response.status_code != 200:
            result.status = Result.Status.STATUS_RESULT_ERROR
            return result

        website_data = response.text
        soup = BeautifulSoup(website_data, 'lxml')
        if soup.find('table', attrs={'id': 'result-tab'}).find('tr', attrs={'class': 'evenrow'}) is None:
            result.status = Result.Status.STATUS_SUBMIT_FAILED
            return result
        line = soup.find('table', attrs={'id': 'result-tab'}).find('tr', attrs={'class': 'evenrow'}).find_all('td')
        if line:
            result.unique_key = line[0].string
            result.verdict_info = line[4].string
            result.execute_time = line[6].string
            result.execute_memory = line[5].string
            result.status = Result.Status.STATUS_RESULT_SUCCESS
        else:
            result.status = Result.Status.STATUS_RESULT_ERROR
        return result


class WUST(Base):
    def __init__(self, *args, **kwargs):
        self._headers = config.default_headers
        self._req = HttpUtil(self._headers, 'utf-8', *args, **kwargs)

    @staticmethod
    def home_page_url():
        url = 'http://acm.wust.edu.cn/'
        return url

    def get_cookies(self):
        return self._req.cookies.get_dict()

    def set_cookies(self, cookies):
        if isinstance(cookies, dict):
            self._req.cookies.update(cookies)

    def is_login(self):
        url = 'http://acm.wust.edu.cn/'
        res = self._req.get(url)
        if res is None:
            return False
        if re.search(r'<a href="logout.php">Logout</a>', res.text) is not None:
            return True

    def login_website(self, account):
        if account and account.cookies:
            self._req.cookies.update(account.cookies)
        if self.is_login():
            return True
        login_page_url = 'http://acm.wust.edu.cn/loginpage.php'
        login_link_url = 'http://acm.wust.edu.cn/login.php'

        post_data = {'user_id': account.username,
                     'password': account.password,
                     'submit': 'Submit'}
        self._req.get(login_page_url)
        self._req.post(login_link_url, post_data)
        if self.is_login():
            return True
        return False

    def account_required(self):
        return False

    def get_problem(self, pid, account=None):
        url = f'http://acm.wust.edu.cn/problem.php?id={pid}&soj=0'
        res = self._req.get(url)
        return WUSTParser().problem_parse(res, pid, url)

    def submit_code(self, account, pid, language, code):
        if not self.login_website(account):
            return Result(Result.Status.STATUS_SPIDER_ERROR)
        link_page_url = 'http://acm.wust.edu.cn/submitpage.php?id=' + str(pid) + '&soj=0'
        link_post_url = 'http://acm.wust.edu.cn/submit.php'
        res = self._req.get(link_page_url)
        if res is None or res.status_code != 200:
            return Result(Result.Status.STATUS_SUBMIT_ERROR)
        soup = BeautifulSoup(res.text, 'lxml')
        submitkey = soup.find('input', attrs={'name': 'submitkey'})['value']
        post_data = {'id': str(pid), 'soj': '0', 'language': language, 'source': code, 'submitkey': str(submitkey)}
        self._headers['Referer'] = link_page_url
        res = self._req.post(url=link_post_url, data=post_data, headers=self._headers)
        if res is None or res.status_code != 200:
            return Result(Result.Status.STATUS_SUBMIT_ERROR)
        return Result(Result.Status.STATUS_SUBMIT_SUCCESS)

    def find_language(self, account):
        if self.login_website(account) is False:
            return None
        url = 'http://acm.wust.edu.cn/submitpage.php?id=1000&soj=0'
        languages = {}
        res = self._req.get(url)
        if res is None:
            return languages
        soup = BeautifulSoup(res.text, 'lxml')
        options = soup.find('select', attrs={'name': 'language'}).find_all('option')
        for option in options:
            languages[option.get('value')] = option.string
        return languages

    def get_result(self, account, pid):
        url = f'http://acm.wust.edu.cn/status.php?soj=-1&' \
            f'problem_id={pid}&user_id={account.username}&language=-1&jresult=-1'

        return self.get_result_by_url(url=url)

    def get_result_by_rid_and_pid(self, rid, pid):
        url = 'http://acm.wust.edu.cn/status.php?top=' + rid
        return self.get_result_by_url(url=url)

    def get_result_by_url(self, url):
        res = self._req.get(url)

        return WUSTParser().result_parse(res)

    def is_working(self):
        url = 'http://acm.wust.edu.cn/'
        res = self._req.get(url)
        if res and re.search(r'<a href="index.php">WUST Online Judge</a>', res.text):
            return True
        return False

    @staticmethod
    def is_accepted(verdict):
        return verdict == 'Accepted'

    @staticmethod
    def is_running(verdict):
        return verdict in ['Pending', 'Pending Rejudge', 'Compiling', 'Running & Judging']

    @staticmethod
    def is_compile_error(verdict):
        return verdict == 'Compile Error'
