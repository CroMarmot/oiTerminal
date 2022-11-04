from typing import List

# Analyze 是紧密依赖 不采用依赖注入？
from oi_cli2.model.Analyze import Analyze
# 依赖注入
from oi_cli2.utils.db import JsonFileDB
# 静态配置
from oi_cli2.utils.consts.ids import Ids


class AnalyzeManager:

  def __init__(self, db: JsonFileDB):
    self.db = db
    self.keys = ['platform', 'alias', 'path', 'compilation', 'execute', 'clean', 'default']

  def _get_analyze_list(self) -> List[Analyze]:
    analyze_list: List[dict] = self.db.load(Ids.analyze) or []
    return list(map(lambda d: Analyze().dict_init(d), analyze_list))

  def _set_analyze_list(self, analyze_list: List[Analyze]):
    analyze_list.sort(key=lambda temp0: (temp0.platform, -temp0.default, temp0.template_alias))
    self.db.save(Ids.analyze, list(map(lambda d: d.__dict__, analyze_list)))

  def get_list(self) -> List[Analyze]:
    return self._get_analyze_list()

  def set_default(self, index: int):
    analyze_list: List[Analyze] = self._get_analyze_list()
    assert 0 <= index < len(analyze_list)
    for i in range(len(analyze_list)):
      if i == index:
        analyze_list[i].default = True
      elif analyze_list[i].platform == analyze_list[index].platform:
        analyze_list[i].default = False

    self._set_analyze_list(analyze_list)

  def delete_analyze(self, index):
    analyze_list: List[Analyze] = self._get_analyze_list()
    assert 0 <= index < len(analyze_list)
    if analyze_list[index].default:
      for i in range(len(analyze_list)):
        if i == index:
          continue
        if analyze_list[i].platform == analyze_list[index].platform:
          analyze_list[i].default = True
          break

    del analyze_list[index]
    self._set_analyze_list(analyze_list)

  # set default if no platform there
  def add_analyze(self, platform, submit_lang, template_alias, class_path):
    analyze_list: List[Analyze] = self._get_analyze_list()

    is_default = True
    for item in analyze_list:
      if item.platform == platform and item.default:
        is_default = False
        break

    analyze_list.append(Analyze().initial(platform, submit_lang, template_alias, class_path, default=is_default))
    self._set_analyze_list(analyze_list)

  def modify_submit_lang(self, index: int, value: str):
    analyze_list: List[Analyze] = self._get_analyze_list()
    assert 0 <= index < len(analyze_list)
    analyze_list[index].submit_lang = value
    self._set_analyze_list(analyze_list)

  def modify_template_alias(self, index: int, value: str):
    analyze_list: List[Analyze] = self._get_analyze_list()
    assert 0 <= index < len(analyze_list)
    analyze_list[index].template_alias = value
    self._set_analyze_list(analyze_list)

  def modify_class_path(self, index: int, value: str):  # 实例class 文件
    analyze_list: List[Analyze] = self._get_analyze_list()
    assert 0 <= index < len(analyze_list)
    analyze_list[index].class_path = value
    self._set_analyze_list(analyze_list)
