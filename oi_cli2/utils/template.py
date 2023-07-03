from typing import List, Optional
import logging

from oi_cli2.model.Template import Template
from oi_cli2.utils.db import JsonFileDB
from oi_cli2.utils.consts.ids import Ids


class TemplateManager:

  def __init__(self, db: JsonFileDB, platform: str = ''):
    self.db = db
    self.platform = platform
    self.keys = ['platform', 'alias', 'path', 'compilation', 'execute', 'clean', 'default']

  def _get_template_list(self) -> List[Template]:
    temp_list: List[dict] = self.db.load(Ids.template) or []
    return list(map(lambda d: Template().dict_init(d), temp_list))

  def _set_template_list(self, temp_list: List[Template]):
    temp_list.sort(key=lambda temp0: (temp0.platform, -temp0.default, temp0.alias))
    self.db.save(Ids.template, list(map(lambda d: d.__dict__, temp_list)))

  def get_list(self) -> List[Template]:
    return self._get_template_list()

  def alias_exist(self, temps: List[Template], platform: str, alias: str):
    return self.find_alias(temps=temps, platform=platform, alias=alias) != -1

  def find_alias(self, temps: List[Template], platform: str, alias: str) -> int:
    for i in range(len(temps)):
      if temps[i].platform == platform and temps[i].alias == alias:
        return i
    return -1

  def get_platform_default(self, platform: str) -> Optional[Template]:
    temps: List[Template] = self._get_template_list()
    for i in range(len(temps)):
      if temps[i].platform == platform and temps[i].default:
        return temps[i]
    return None

  def get_default(self) -> Optional[Template]:
    if not self.platform:
      logging.error('Please set platform first or using get_platform_default()')
      return None
    temps: List[Template] = self._get_template_list()
    for i in range(len(temps)):
      if temps[i].platform == self.platform and temps[i].default:
        return temps[i]
    return None

  def get_template_by_name(self, platform: str, name: str) -> Optional[Template]:
    temps: List[Template] = self._get_template_list()
    for i in range(len(temps)):
      if temps[i].platform == platform and temps[i].alias == name:
        return temps[i]
    return None

  def get_template_by_alias(self, alias: str) -> Optional[Template]:
    # deperated
    assert False
    pass
    if not self.platform:
      logging.error('Please set platform first or using get_platform_default()')
      return None
    temps: List[Template] = self._get_template_list()
    for i in range(len(temps)):
      if temps[i].platform == self.platform and temps[i].alias == alias:
        return temps[i]
    return None

  def set_temps_default(self, temps: List[Template], index: int):
    assert 0 <= index < len(temps)
    for i in range(len(temps)):
      if i == index:
        temps[i].default = True
      elif temps[i].platform == temps[index].platform:
        temps[i].default = False

  def set_default(self, index: int):
    temps: List[Template] = self._get_template_list()
    assert 0 <= index < len(temps)
    for i in range(len(temps)):
      if i == index:
        temps[i].default = True
      elif temps[i].platform == temps[index].platform:
        temps[i].default = False

    self._set_template_list(temps)

  def delete_template(self, platform: str, name: str) -> bool:
    temps: List[Template] = self._get_template_list()
    idx = -1
    for i in range(len(temps)):
      if temps[i].platform == platform and temps[i].alias == name:
        idx = i
        break
    if idx < 0:
      return False

    if temps[idx].default:
      for i in range(len(temps)):
        if i == idx:
          continue
        if temps[i].platform == temps[idx].platform:
          temps[i].default = True
          break

    del temps[idx]
    self._set_template_list(temps)
    return True

  # set default if no platform there
  def add_template(self, platform, alias, path, compilation, execute, uplang) -> None:
    temps: List[Template] = self._get_template_list()
    if self.find_alias(temps, platform, alias) != -1:
      raise Exception('Duplicate alias')

    is_default = True
    for item in temps:
      if item.platform == platform and item.default:
        is_default = False
        break

    temps.append(Template().initial(platform=platform,
                                    alias=alias,
                                    path=path,
                                    compilation=compilation,
                                    execute=execute,
                                    uplang=uplang,
                                    default=is_default))
    self._set_template_list(temps)

  def modify_alias(self, index: int, value: str):
    temps: List[Template] = self._get_template_list()
    assert 0 <= index < len(temps)
    if self.alias_exist(temps, temps[index].platform, value):
      raise Exception('Duplicate alias')
    temps[index].alias = value
    self._set_template_list(temps)

  def modify_path(self, index: int, value: str):
    temps: List[Template] = self._get_template_list()
    assert 0 <= index < len(temps)
    temps[index].path = value
    self._set_template_list(temps)

  def modify_compilation(self, index: int, value: str):
    temps: List[Template] = self._get_template_list()
    assert 0 <= index < len(temps)
    temps[index].compilation = value
    self._set_template_list(temps)

  def modify_execute(self, index: int, value: str):
    temps: List[Template] = self._get_template_list()
    assert 0 <= index < len(temps)
    temps[index].execute = value
    self._set_template_list(temps)

  def modify_clean(self, index: int, value: str):
    temps: List[Template] = self._get_template_list()
    assert 0 <= index < len(temps)
    temps[index].clean = value
    self._set_template_list(temps)

  # update
  def update_template(self, platform, alias: str, newalias: str, path: str, compilation: str, execute: str, uplang: str,
                      default: bool):
    temps: List[Template] = self._get_template_list()
    idx = self.find_alias(temps, platform, alias)
    if idx == -1:
      raise Exception('Template Not Exist')

    if default:
      self.set_temps_default(temps, idx)

    if newalias:
      temps[idx].alias = newalias

    if path:
      temps[idx].path = path

    if compilation:
      temps[idx].compilation = compilation

    if execute:
      temps[idx].execute = execute

    if uplang:
      temps[idx].uplang = uplang

    self._set_template_list(temps)
