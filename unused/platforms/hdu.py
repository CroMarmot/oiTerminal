import re

from bs4 import BeautifulSoup
from bs4 import element

from spider import config
from spider.config import Problem, Result
from spider.platforms.base import Base, BaseParser
from spider.utils import HttpUtil, HtmlTag


class HDUParser(BaseParser):
    def __init__(self, *args, **kwargs):
        self._static_prefix = 'http://acm.hdu.edu.cn/'
        self._script = """<script type="text/x-mathjax-config">
     MathJax.Hub.Config({
      showProcessingMessages: false,
      messageStyle: "none",
      extensions: ["tex2jax.js"],
      jax: ["input/TeX", "output/HTML-CSS"],
      tex2jax: {
          inlineMath:  [ ["$", "$"] ],
          displayMath: [ ["$$","$$"] ],
          skipTags: ['script', 'noscript', 'style', 'textarea', 'pre','code','a']
      },
      "HTML-CSS": {
          availableFonts: ["STIX","TeX"],
          showMathMenu: false
      }
     });
    </script>
    <script src="https://cdn.bootcss.com/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>"""

    def problem_parse(self, response, pid, url):
        problem = Problem()

        problem.remote_id = pid
        problem.remote_url = url
        problem.remote_oj = 'HDU'

        if response is None:
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

        match_groups = re.search(r'color:#1A5CC8\'>([\s\S]*?)</h1>', website_data)
        if match_groups:
            problem.title = match_groups.group(1)
        match_groups = re.search(r'(\d* MS)', website_data)
        if match_groups:
            problem.time_limit = match_groups.group(1)
        match_groups = re.search(r'/(\d* K)', website_data)
        if match_groups:
            problem.memory_limit = match_groups.group(1)
        problem.special_judge = re.search(r'color=red>Special Judge</font>', website_data) is not None

        problem.html = ''
        for tag in soup.find('h1').parent.children:
            if type(tag) == element.Tag and tag.get('class') and set(tag['class']).intersection({'panel_title',
                                                                                                 'panel_content',
                                                                                                 'panel_bottom'}):
                if set(tag['class']).intersection({'panel_title', }):
                    tag['class'] += (HtmlTag.TagDesc.TITLE.value,)
                    tag['style'] = HtmlTag.TagStyle.TITLE.value
                else:
                    tag['class'] += (HtmlTag.TagDesc.CONTENT.value,)
                    tag['style'] = HtmlTag.TagStyle.CONTENT.value
                problem.html += str(HtmlTag.update_tag(tag, self._static_prefix))
        problem.html += self._script
        problem.status = Problem.Status.STATUS_SUCCESS
        return problem

    def result_parse(self, response):
        result = Result()

        if response is None or response.status_code != 200:
            result.status = Result.Status.STATUS_RESULT_ERROR
            return result
        website_data = response.text
        soup = BeautifulSoup(website_data, 'lxml')
        line = soup.find('table', attrs={'class': 'table_text'}).find('tr', attrs={'align': 'center'}).find_all('td')
        if line:
            result.unique_key = line[0].string
            result.verdict_info = line[2].get_text()
            result.execute_time = line[4].string
            result.execute_memory = line[5].string
            result.status = Result.Status.STATUS_RESULT_SUCCESS
        else:
            result.status = Result.Status.STATUS_RESULT_ERROR
        return result


class HDU(Base):
    def __init__(self, *args, **kwargs):
        self._code_type = 'gb18030'
        self._req = HttpUtil(headers=config.default_headers, code_type=self._code_type,
                             *args, **kwargs)

    @staticmethod
    def home_page_url():
        url = 'http://acm.hdu.edu.cn/'
        return url

    def get_cookies(self):
        return self._req.cookies.get_dict()

    def set_cookies(self, cookies):
        if isinstance(cookies, dict):
            self._req.cookies.update(cookies)

    def is_login(self):
        url = 'http://acm.hdu.edu.cn/'
        res = self._req.get(url)
        if res and re.search(r'userloginex\.php\?action=logout', res.text) is not None:
            return True
        return False

    def login_website(self, account):
        if account and account.cookies:
            self._req.cookies.update(account.cookies)
        if self.is_login():
            return True
        login_link_url = 'http://acm.hdu.edu.cn/userloginex.php'
        post_data = {'username': account.username,
                     'userpass': account.password,
                     'login': 'Sign In'
                     }
        self._req.post(url=login_link_url, data=post_data,
                       params={'action': 'login'})
        return self.is_login()

    def account_required(self):
        return False

    def get_problem(self, pid, account=None):

        url = 'http://acm.hdu.edu.cn/showproblem.php?pid=' + pid
        res = self._req.get(url)
        return HDUParser().problem_parse(res, pid, url)

    def submit_code(self, account, pid, language, code):
        if not self.login_website(account):
            return Result(Result.Status.STATUS_SUBMIT_ERROR)
        url = 'http://acm.hdu.edu.cn/submit.php'
        post_data = {'check': '0', 'language': language, 'problemid': pid, 'usercode': code}
        res = self._req.post(url=url, data=post_data, params={'action': 'submit'})
        if res and res.status_code == 200:
            return Result(Result.Status.STATUS_SUBMIT_SUCCESS)
        return Result(Result.Status.STATUS_SUBMIT_ERROR)

    def find_language(self, account):
        if self.login_website(account) is False:
            return None
        url = 'http://acm.hdu.edu.cn/submit.php'
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
        url = f'http://acm.hdu.edu.cn/status.php?first=&pid=${pid}&user={account.username}&lang=0&status=0'
        return self.get_result_by_url(url=url)

    def get_result_by_rid_and_pid(self, rid, pid):
        url = f'http://acm.hdu.edu.cn/status.php?first=${rid}&pid=&user=&lang=0&status=0'
        return self.get_result_by_url(url=url)

    def get_result_by_url(self, url):
        res = self._req.get(url)
        return HDUParser().result_parse(res)

    def is_working(self):
        url = 'http://acm.hdu.edu.cn/'
        res = self._req.get(url)
        if res and re.search(r'<H1>Welcome to HDU Online Judge System</H1>', res.text):
            return True
        return False

    @staticmethod
    def is_accepted(verdict):
        return verdict == 'Accepted'

    @staticmethod
    def is_compile_error(verdict):
        return verdict == 'Compilation Error'

    @staticmethod
    def is_running(verdict):
        return verdict in ['Queuing', 'Compiling', 'Running']
