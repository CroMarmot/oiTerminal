# -*- coding: utf-8 -*-

import pytest
from oiTerminal.Model.LangKV import LangKV


class TestLangKV():
    def test_data(self):
        lkv = LangKV()
        if lkv != {}:
            pytest.raises(RuntimeError)

    def test_set_12(self):
        lkv = LangKV()
        lkv.set("1", "2")
        assert (lkv.data == {"1": "2"})

    def test_set_rand(self):
        lkv = LangKV()
        lkv.set("133", "2")
        lkv.set("xxx", "223")
        lkv.set("6", "asdfa")
        lkv.set("fgsfg", "xxx")
        assert (lkv.data == {
            "133": "2",
            "xxx": "223",
            "6": "asdfa",
            "fgsfg": "xxx"})

    def test_get_12(self):
        lkv = LangKV()
        lkv.set("33", "4")
        assert (lkv.get("33") == "4")

    def test_get_rand(self):
        lkv = LangKV()
        lkv.set("xx", "z")
        lkv.set("3hh", "n")
        lkv.set("qq", "asg")
        assert (lkv.get("3hh") == "n")
