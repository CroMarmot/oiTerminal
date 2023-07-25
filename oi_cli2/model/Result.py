from dataclasses import dataclass
from enum import Enum
from oi_cli2.cli.constant import GREEN, RED, YELLOW, DEFAULT


@dataclass
class SubmissionResult:

  class Status(Enum):
    PENDING, RUNNING, AC, RE, CE, WA, TLE, MLE, IDLE, UNKNOWN = range(10)

  id: str = '0'
  cur_status: Status = Status.PENDING
  url: str = ''  # print for user
  quick_key: str = ''  # for refetch result
  state_note: str = '0'
  time_note: str = ''
  mem_note: str = ''
  msg_txt: str = ''


def status_string(result: SubmissionResult) -> str:
  return {
      SubmissionResult.Status.PENDING: YELLOW + 'Pending...' + DEFAULT,
      SubmissionResult.Status.RUNNING: GREEN + 'Running...' + DEFAULT,
      SubmissionResult.Status.AC: GREEN + 'AC' + DEFAULT,
      SubmissionResult.Status.CE: RED + 'CE' + DEFAULT,
      SubmissionResult.Status.RE: RED + 'RE' + DEFAULT,
      SubmissionResult.Status.WA: RED + 'WA' + DEFAULT,
      SubmissionResult.Status.TLE: RED + 'TLE' + DEFAULT,
      SubmissionResult.Status.MLE: RED + 'MLE' + DEFAULT,
      SubmissionResult.Status.IDLE: RED + 'IDLENESS_LIMIT_EXCEEDED' + DEFAULT,
      SubmissionResult.Status.UNKNOWN: RED + 'UNKNOWN RESULT' + DEFAULT,
  }[result.cur_status]
