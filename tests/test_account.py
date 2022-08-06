from oi_cli2.utils.account import AccountManager
from tests.mock.Cipher import FakeCipher
from tests.mock.DB import FakeDB


def test_account():
  db = FakeDB()
  cipher = FakeCipher()
  am = AccountManager(db, cipher)

  platform = 'Codeforces'
  user = 'user'
  password = 'zxcv1234'

  # default is empty
  assert am.get_list() == []

  am.add_account(platform, user, password)
  # password encrypted
  assert am.get_list()[0].password == cipher.encrypt(password)

  platform1 = 'Codeforces1'
  user1 = 'user1'
  password1 = 'zxcv12341'

  am.add_account(platform1, user1, password1)
  assert len(am.get_list()) == 2

  platform2 = 'Codeforces2'
  user2 = 'user2'
  password2 = 'zxcv12342'

  am.add_account(platform2, user2, password2)
  am.delete_account(1)
  assert len(am.get_list()) == 2
  assert am.get_list()[1].platform == platform2
  assert am.get_list()[1].account == user2
