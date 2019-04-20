import pytest
from oiTerminal.Model.TestCases import TestCase, TestCases


class TestTestCase():
    def test_test_case(self):
        try:
            ttc = TestCase()
        except TypeError as e:
            return
        pytest.raises(RuntimeError)

    def test_in_out(self):
        ttc = TestCase("1 \n 2 3", "6")
        assert (ttc.in_data == "1 \n 2 3")
        assert (ttc.out_data == "6")


class TestTestCase():
