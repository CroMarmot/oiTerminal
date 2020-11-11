import os
from oiTerminal.utils.db import JsonFileDB


class FakeLogger:
    def warning(self, *args, **kwargs):
        pass

    def debug(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

    def exception(self, *args, **kwargs):
        pass


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
