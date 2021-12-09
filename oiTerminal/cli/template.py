from typing import List

from oiTerminal.model.Template import Template
from oiTerminal.utils.template import TemplateManager


def template_list(tm: TemplateManager):
    temp_list: List[Template] = tm.get_list()
    for i in range(len(temp_list)):
        if i == 0 or temp_list[i].platform != temp_list[i - 1].platform:
            print(temp_list[i].platform)
        mark = ' '
        if temp_list[i].default:
            mark = '*'
        print(f'\t {mark} {temp_list[i].alias}')
    if len(temp_list) == 0:
        print("Template list is empty.")


def template_new(tm: TemplateManager):
    platforms = ['Codeforces', 'AtCoder']
    for i in range(len(platforms)):
        print(f"{i + 1}) {platforms[i]}")
    try:
        index = int(input("> "))
    except Exception:
        print("input error")
        return

    if 0 < index <= len(platforms):
        platform = platforms[index-1]
    else:
        print("input error")
        return

    alias = input('alias:')
    path = input('path:')
    compilation = input('compilation:')
    execute = input('execute:')
    clean = input('clean:')

    tm.add_template(platform, alias, path, compilation, execute, clean)


def template_modify(tm: TemplateManager):
    temp_list = tm.get_list()

    for i in range(len(temp_list)):
        if i == 0 or temp_list[i].platform != temp_list[i-1].platform:
            print(temp_list[i].platform)
        mark = ' '
        item = temp_list[i]
        if item.default:
            mark = '*'
        print(f'\t {mark} {i}) {item.alias}')
        print(f'\t\t path:        {item.path}')
        print(f'\t\t compilation: {item.compilation}')
        print(f'\t\t execute:     {item.execute}')
        print(f'\t\t clean:       {item.clean}')

    try:
        acc_index = int(input("> "))
    except Exception:
        print("input error")

    if acc_index < 0 or acc_index >= len(temp_list):
        print("input error")
        return

    print("1) Change Template Alias")
    print("2) Change Template Path")
    print("3) Change Template Execute command")
    print("4) Change Template Clean command")
    print("5) Set as Default")
    print("6) Delete")

    try:
        index = int(input("> "))
    except(Exception):
        print("input error")

    if index == 1:
        tm.modify_alias(acc_index, input("Enter Alias Name:"))
    elif index == 2:
        tm.modify_path(acc_index, input("Enter template code Path:"))
    elif index == 3:
        tm.modify_execute(acc_index, input("Enter execute command"))
    elif index == 4:
        tm.modify_clean(acc_index, input("Enter clean command"))
    elif index == 5:
        tm.set_default(acc_index)
    elif index == 6:
        tm.delete_template(acc_index)


def template(db):
    print("1) Template List")
    print("2) New Template")
    print("3) Modify Template")
    try:
        index = int(input("> "))
    except(Exception):
        print("input error")

    tm = TemplateManager(db)

    if index == 1:
        template_list(tm)
    elif index == 2:
        template_new(tm)
    elif index == 3:
        template_modify(tm)
    else:
        print("input error")
