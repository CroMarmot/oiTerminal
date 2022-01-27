from oiTerminal.utils.analyze import AnalyzeManager
from tests.mock.DB import FakeDB


def test_analyze():
  db = FakeDB()
  am = AnalyzeManager(db)

  platform = 'Codeforces'
  submit_lang = '54'
  template_alias = 'g++'
  class_path = './Codeforces.py'

  # default is empty
  assert am.get_list() == []

  am.add_analyze(platform, submit_lang, template_alias, class_path)

  assert am.get_list()[0].platform == platform
  assert am.get_list()[0].submit_lang == submit_lang
  assert am.get_list()[0].template_alias == template_alias
  assert am.get_list()[0].class_path == class_path

  am.add_analyze(platform, submit_lang, template_alias, class_path)

  platform1 = 'Codeforces1'
  submit_lang1 = '541'
  template_alias1 = 'g++1'
  class_path1 = './Codeforces.py1'

  am.add_analyze(platform1, submit_lang1, template_alias1, class_path1)

  assert len(am.get_list()) == 3
