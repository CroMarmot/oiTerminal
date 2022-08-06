import os
from oi_cli2.utils.db import JsonFileDB
from tests.mock.Logger import FakeLogger


def test_db():
  test_file = 'testdb.json'
  jfdb = JsonFileDB(test_file, logger=FakeLogger())
  assert jfdb.load("NotExist") is None
  jfdb.save("Hey", 1)
  jfdb.save("dict", {'a': {'b': 'c'}})
  jfdb.save("Hey1", 2)
  assert jfdb.load("Hey") == 1
  assert jfdb.load("Hey1") == 2
  assert jfdb.load("dict") == {'a': {'b': 'c'}}
  os.remove(test_file)
