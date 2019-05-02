from enum import Enum


class Result:
    class Status(Enum):
        VERDICT_PENDING = 'Pending'
        VERDICT_RUNNING = 'Running'
        VERDICT_AC = 'AC'
        VERDICT_CE = 'CE'
        VERDICT_WA = 'WA'
        VERDICT_TLE = 'TLE'
        VERDICT_MLE = 'MLE'

    _cur_status: Status

    def __init__(self):
        pass
