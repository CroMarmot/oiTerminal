import pytest
from oiTerminal.Model.Contest import Contest


class TestContest():
    def test_type_error(self):
        try:
            c = Contest()
        except TypeError as e:
            return
        pytest.raises(RuntimeError)
