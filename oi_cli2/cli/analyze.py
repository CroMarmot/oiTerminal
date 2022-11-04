from typing import List

from oi_cli2.model.Analyze import Analyze
from oi_cli2.utils.analyze import AnalyzeManager

# TODO 动态注册不同平台


def analyze_list(tm: AnalyzeManager):
  analyze_list: List[Analyze] = tm.get_list()
  for i in range(len(analyze_list)):
    if i == 0 or analyze_list[i].platform != analyze_list[i - 1].platform:
      print(analyze_list[i].platform)
    mark = ' '
    if analyze_list[i].default:
      mark = '*'
    print(f'\t {mark} {analyze_list[i].template_alias} {analyze_list[i].submit_lang}')

  if len(analyze_list) == 0:
    print("Analyze list is empty.")


def analyze_new(tm: AnalyzeManager):
  platforms = ['Codeforces', 'AtCoder']
  for i in range(len(platforms)):
    print(f"{i + 1}) {platforms[i]}")
  try:
    index = int(input("> "))
  except Exception:
    print("input error")
    return

  if 0 < index <= len(platforms):
    platform = platforms[index - 1]
  else:
    print("input error")
    return

  submit_lang = input('submit_lang:')
  template_alias = input('template_alias:')
  class_path = input('class_path:')

  tm.add_analyze(platform, submit_lang, template_alias, class_path)


def analyze_modify(tm: AnalyzeManager):
  analyze_list = tm.get_list()

  for i in range(len(analyze_list)):
    if i == 0 or analyze_list[i].platform != analyze_list[i - 1].platform:
      print(analyze_list[i].platform)
    mark = ' '
    item = analyze_list[i]
    if item.default:
      mark = '*'
    print(f'\t {mark} {i}) {item.template_alias}')
    print(f'\t\t submit_lang: {item.submit_lang}')
    print(f'\t\t class_path:  {item.class_path}')

  try:
    acc_index = int(input("> "))
  except Exception:
    print("input error")

  if acc_index < 0 or acc_index >= len(analyze_list):
    print("input error")
    return

  print("1) Change Analyze template")
  print("2) Change Analyze submit language")
  print("3) Change Analyze class path")
  print("4) Set as Default")
  print("5) Delete")

  try:
    index = int(input("> "))
  except (Exception):
    print("input error")

  if index == 1:
    tm.modify_template_alias(acc_index, input("Enter template_alias:"))
  elif index == 2:
    tm.modify_submit_lang(acc_index, input("Enter submit lang:"))
  elif index == 3:
    tm.modify_class_path(acc_index, input("Enter class path:"))
  elif index == 4:
    tm.set_default(acc_index)
  elif index == 5:
    tm.delete_analyze(acc_index)


def analyze(db):
  print("1) Analyze List")
  print("2) New Analyze")
  print("3) Modify Analyze")
  try:
    index = int(input("> "))
  except (Exception):
    print("input error")

  tm = AnalyzeManager(db)

  if index == 1:
    analyze_list(tm)
  elif index == 2:
    analyze_new(tm)
  elif index == 3:
    analyze_modify(tm)
  else:
    print("input error")
