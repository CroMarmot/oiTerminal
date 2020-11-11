from typing import List, Optional

# Template 是紧密依赖 不采用依赖注入？
from oiTerminal.model.Template import Template
# 依赖注入
from oiTerminal.utils.db import JsonFileDB
# 静态配置
from oiTerminal.utils.consts.ids import Ids


class TemplateManager:

    def __init__(self, db: JsonFileDB):
        self.db = db
        self.keys = ['platform', 'alias', 'path', 'compilation', 'execute', 'clean', 'default']

    def _get_template_list(self) -> List[Template]:
        temp_list: List[dict] = self.db.load(Ids.template)
        if temp_list is None:
            return []
        return list(map(lambda d: Template().dict_init(d), temp_list))

    def _set_template_list(self, temp_list: List[Template]):
        temp_list.sort(key=lambda temp0: (temp0.platform, -temp0.default, temp0.alias))
        self.db.save(Ids.template, list(map(lambda d: d.__dict__, temp_list)))

    def get_list(self) -> List[Template]:
        return self._get_template_list()

    def alias_exist(self, temps: List[Template], platform: str, alias: str):
        for item in temps:
            if item.platform == platform and item.alias == alias:
                return True
        return False

    def get_platform_default(self, platform:str) -> Optional[Template]:
        temps: List[Template] = self._get_template_list()
        for i in range(len(temps)):
            if temps[i].platform == platform and temps[i].default:
                return temps[i]
        return None

    def set_default(self, index: int):
        temps: List[Template] = self._get_template_list()
        assert 0 <= index < len(temps)
        for i in range(len(temps)):
            if i == index:
                temps[i].default = True
            elif temps[i].platform == temps[index].platform:
                temps[i].default = False

        self._set_template_list(temps)

    def delete_template(self, index):
        temps: List[Template] = self._get_template_list()
        assert 0 <= index < len(temps)
        if temps[index].default:
            for i in range(len(temps)):
                if i == index:
                    continue
                if temps[i].platform == temps[index].platform:
                    temps[i].default = True
                    break

        del temps[index]
        self._set_template_list(temps)

    # set default if no platform there
    def add_template(self, platform, alias, path, compilation, execute, clean):
        temps: List[Template] = self._get_template_list()
        if self.alias_exist(temps, platform, alias):
            raise Exception('Duplicate alias')

        is_default = True
        for item in temps:
            if item.platform == platform and item.default:
                is_default = False
                break

        temps.append(Template().initial(platform, alias, path, compilation, execute, clean, default=is_default))
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
