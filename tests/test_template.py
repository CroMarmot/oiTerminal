from oi_cli2.utils.template import TemplateManager
from tests.mock.DB import FakeDB


def test_template():
  db = FakeDB()
  am = TemplateManager(db)

  platform = 'Codeforces'
  alias = 'Cf-C++'
  path = './custom/Main.cpp'
  compilation = 'g++ -o Main Main.cpp'
  execute = './Main'
  uplang = 54

  # default is empty
  assert am.get_list() == []

  am.add_template(platform=platform, alias=alias, path=path, compilation=compilation, execute=execute, uplang=uplang)

  assert am.get_list()[0].alias == alias
  assert am.get_list()[0].path == path
  assert am.get_list()[0].platform == platform
  assert am.get_list()[0].compilation == compilation
  assert am.get_list()[0].execute == execute
  assert am.get_list()[0].uplang == uplang

  try:
    # cannot add same alias in same platform
    am.add_template(platform, alias, '', '', '', '')
    assert False
  except Exception as e:
    pass

  platform1 = 'Codeforces1'
  alias1 = 'alias1'

  am.add_template(platform1, alias, '', '', '', '')
  am.add_template(platform, alias1, '', '', '', '')
  am.add_template(platform1, alias1, '', '', '', '')

  assert len(am.get_list()) == 4
