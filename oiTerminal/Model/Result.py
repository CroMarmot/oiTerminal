from enum import Enum


class Result:
    class Status(Enum):
        PENDING = 'Pending'
        RUNNING = 'Running'
        AC = 'AC'
        CE = 'CE'
        WA = 'WA'
        TLE = 'TLE'
        MLE = 'MLE'

    cur_status: Status
    quick_key: str = ''
    passed: str = '0'
    total: str = '0'

    def __init__(self, cur_status: Status):
        self.cur_status = cur_status
