import pytest
from oiTerminal.Model.Account import Account


class TestAccount():
    def test_type_err(self):
        try:
            acc = Account()
        except TypeError as e:
            print(e)
            return
        pytest.raises(RuntimeError)

    def test_data(self):
        acc = Account("aaa", "xxx")
        assert (acc.username == "aaa")
        assert (acc.password == "xxx")
        assert (acc.cookie is None)

    def test_cookie(self):
        acc = Account("zzq", "vcb", "sags")
        assert (acc.cookie == "sags")

    def test_set_cookie(self):
        acc = Account("zzq53", "2tb")
        acc.cookie = "52h5g"
        assert (acc.cookie == "52h5g")

    def test_del_cookie(self):
        acc = Account("34fea", "gfhbn", "zzzz")
        del acc.cookie
        assert (acc.cookie is None)
