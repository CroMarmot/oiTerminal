import json
import os
from oi_cli2.cli.constant import LANG_CONFIG_FILE, TEMPLATEFOLDER


class LanguageUtil(object):
  _lang_cfg = None

  @staticmethod
  def init() -> map:
    if LanguageUtil._lang_cfg is not None:
      return LanguageUtil._lang_cfg
    if not os.path.isfile(LANG_CONFIG_FILE):
      raise Exception(f'LANG_CONFIG_FILE [{LANG_CONFIG_FILE}] NOT EXIST!')
    with open(LANG_CONFIG_FILE) as f:
      LanguageUtil._lang_cfg = json.load(f)
    return LanguageUtil._lang_cfg

  @staticmethod
  def local_lang() -> list:
    """
    Return a list of local support language.

    :return: The local_lang list.
    :rtype: list[str]
    """
    return list(LanguageUtil.init().keys())

  @staticmethod
  def lang2suffix(lang) -> str:
    return LanguageUtil.init().get(lang).get('suffix')

  @staticmethod
  def lang2template(lang) -> str:
    return TEMPLATEFOLDER + LanguageUtil.init().get(lang).get('template')

  @staticmethod
  def lang2compile(lang) -> str:
    return LanguageUtil.init().get(lang).get('compile')

  @staticmethod
  def lang2exe(lang, input_file, output_file):
    return LanguageUtil.init().get(lang).get('exe') + " < " + input_file + " > " + output_file