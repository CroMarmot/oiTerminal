from enum import Enum
from const import *


class Result:
    class Status(Enum):
        PENDING, RUNNING, AC, RE, CE, WA, TLE, MLE = range(8)

    @property
    def status_string(self) -> str:
        return {
            Result.Status.PENDING: YELLOW + 'Pending...' + DEFAULT,
            Result.Status.RUNNING: GREEN + 'Running...' + DEFAULT,
            Result.Status.AC: GREEN + 'AC' + DEFAULT,
            Result.Status.CE: RED + 'CE' + DEFAULT,
            Result.Status.RE: RED + 'RE' + DEFAULT,
            Result.Status.WA: RED + 'WA' + DEFAULT,
            Result.Status.TLE: RED + 'TLE' + DEFAULT,
            Result.Status.MLE: RED + 'MLE' + DEFAULT,
        }[self.cur_status]

    cur_status: Status
    quick_key: str = ''

    state_note: str = '0'
    time_note: str = '0/0'
    mem_note: str = '0/0'

    _id: int = 0

    def __init__(self, cur_status: Status):
        self.cur_status = cur_status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
