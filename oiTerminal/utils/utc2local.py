from datetime import datetime, timedelta
import time


def moscow_to_utc(dt: datetime) -> datetime:
  return dt - timedelta(hours=3)


def utc_to_local(utc_datetime: datetime) -> datetime:
  now_timestamp = time.time()
  offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
  return utc_datetime + offset
