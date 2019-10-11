import pytest
from oiTerminal.Model.Problem import Problem


class TestProblem():
    def test_type_error(self):
        try:
            p = Problem()
        except TypeError as e:
            return
        pytest.raises(RuntimeError)

    def test_pid_oj(self):
        p = Problem("123A", "cf")
        assert (p.id == "123A")
        assert (p.oj == "cf")

    def test_rw_description(self):
        p = Problem("vas", "asd")
        assert (p.description == '')
        p.description = "html data"
        assert (p.description == "html data")

    def test_rw_test_cases(self):
        pass

    def test_rw_time_limit(self):
        p = Problem("zz", "qwed")
        assert (p.time_limit == '')
        p.time_limit = "1111s"
        assert (p.time_limit == "1111s")

    def test_rw_mem_limit(self):
        p = Problem("zqwez", "hed")
        assert (p.mem_limit == '')
        p.mem_limit = "1234MB"
        assert (p.mem_limit == "1234MB")
