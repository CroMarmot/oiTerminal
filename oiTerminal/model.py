from enum import Enum

default_headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

class Contest(object):
    class Status(Enum):
        STATUS_ERROR = 'Error'

    def __init__(self, oj=None, cid=None, status=None):
        self.oj = oj
        self.id = cid
        self.status = status
        self.problem_set = {}  # { "problemid": Problem ,}


class TestCase(object):
    def __init__(self, sample_in=None, sample_out=None):
        self.sample_in = sample_in
        self.sample_out = sample_out


class Problem(object):

    class Status(Enum):
        """
        STATUS_PENDING:加入队列
        STATUS_RUNNING:正在执行中
        STATUS_SUCCESS:成功抓取到题目
        STATUS_RETRYABLE:没有成功抓取到题目，但是可以待会儿重试
        STATUS_ERROR:没有成功抓取到题目
        """
        STATUS_PENDING = 'Pending'
        STATUS_RUNNING = 'Running'
        STATUS_SUCCESS = 'Success'
        STATUS_RETRYABLE = 'Retryable'
        STATUS_ERROR = 'Error'

    def __init__(self, oj=None, pid=None, url=None, status=None):
        self.id = pid
        self.status = status
        self.oj = oj
        self.url = url
        self.title = None
        self.time_limit = None
        self.memory_limit = None
        self.special_judge = None
        self.test_case = None

        # 这个属性是html代码，直接在网页中用iframe展示
        self.html = None

        # 这个属性代表使用的开源OJ类型，比如hustoj,qduoj等。
        self.template = None


class Result(object):
    """
    提交代码到源网站和从原网站抓取结果的返回对象
    """

    def __init__(self, status=None):
        self.unique_key: str = None
        self.verdict_info: str = None
        self.execute_time: str = None
        self.execute_memory: str = None
        self.compile_info: str = None

        self.verdict = None
        self.status = status

    class Status(Enum):
        """
        STATUS_PENDING:放入队列的状态，不可刷新
        STATUS_SPIDER_ERROR:爬虫启动错误，通常指没有可用账号，可以刷新
        STATUS_SUBMIT_ERROR:提交失败，可以刷新
        STATUS_SUBMIT_SUCCESS:成功提交，不可刷新
        STATUS_RESULT_ERROR:获取提交结果失败,但是已经成功提交。不可刷新
        STATUS_RESULT_SUCCESS:获取提交结果成功，不可刷新
        STATUS_SYSTEM_ERROR:系统错误，不可刷新
        """
        STATUS_PENDING = 'Pending'
        STATUS_SPIDER_ERROR = 'Spider Error'
        STATUS_SUBMIT_ERROR = 'Submit Error'
        STATUS_SUBMIT_SUCCESS = 'Submit Success'
        STATUS_RESULT_ERROR = 'Result Error'
        STATUS_RESULT_SUCCESS = 'Result Success'
        STATUS_SYSTEM_ERROR = 'System Error'

    # verdict 表示源平台的运行状态

    class Verdict(Enum):
        """
        verdict:
            RUNNING:源平台正在运行代码或者正在源平台的等待队列之中
            AC: 通过
            CE: 编译错误
            WA: 代码错误，包含超时，结果出错，内存超出, 系统错误等。
            TLE: time limit
            MLE: memory limit
        verdict_info:
            服务器返回的具体内容，不同的平台显示的内容格式不一样
        """
        VERDICT_RUNNING = 'Running'
        VERDICT_AC = 'AC'
        VERDICT_CE = 'CE'
        VERDICT_WA = 'WA'
        VERDICT_TLE = 'TLE'
        VERDICT_MLE = 'MLE'
