import logging
from typing import List

import click
from oi_cli2.core.DI import DI_DB, DI_LOGGER, DI_TEMPMAN

from oi_cli2.model.Template import Template
from oi_cli2.utils.template import TemplateManager


@click.group()
@click.pass_context
def template(ctx):
  """Manage templates"""
  db = ctx.obj[DI_DB]
  ctx.obj[DI_TEMPMAN] = TemplateManager(db)


@template.command(name='list')
@click.option('-d', '--detail', is_flag=True, help="display config detail")
@click.pass_context
def list_command(ctx, detail: bool):
  """List all templates"""
  tm: TemplateManager = ctx.obj[DI_TEMPMAN]
  temp_list: List[Template] = tm.get_list()
  for i in range(len(temp_list)):
    if i == 0 or temp_list[i].platform != temp_list[i - 1].platform:
      print(temp_list[i].platform)
    mark = ' '
    if temp_list[i].default:
      mark = '*'
    print(f'  {mark} {temp_list[i].alias}')
    if detail:
      print(f'  \tCompile command    : {temp_list[i].compilation}')
      print(f'  \tExecute command    : {temp_list[i].execute}')
      print(f'  \tTemplate file Path : {temp_list[i].path}')
      print(f'  \tUpload language id : {temp_list[i].uplang}')
  if len(temp_list) == 0:
    print("Template list is empty.")


@template.command()
@click.pass_context
@click.argument('platform')
@click.argument('name')
@click.argument('path')
@click.argument('compile')
@click.argument('execute')
@click.argument('langid')
def new(ctx, platform, name, path, compile, execute, langid) -> None:
  """Create new template

  PLATFORM    Platform Name, (AtCoder,Codeforces)

  NAME        Custom template name

  PATH        Your template file path

  COMPILE     Compile command

  EXECUTE     Execute command

  LANGID      Upload language id(`oi lang <platform>`)"""
  tm: TemplateManager = ctx.obj[DI_TEMPMAN]
  logger: logging.Logger = ctx.obj[DI_LOGGER]
  logger.debug(f"{platform}, {name}, {path}, {compile}, {execute}, {langid}")
  tm.add_template(platform=platform, alias=name, path=path, compilation=compile, execute=execute, uplang=langid)


@template.command()
@click.pass_context
@click.argument('platform')
@click.argument('name')
def delete(ctx, platform, name) -> None:
  """Delete a specific template"""
  tm: TemplateManager = ctx.obj[DI_TEMPMAN]
  tm.delete_template(platform, name)


@template.command()
@click.pass_context
@click.argument('platform')
@click.argument('name')
@click.option('-n', '--name', 'newname', help='Change template name')
@click.option('-p', '--path', help='Change template path')
@click.option('-c', '--compile', help='Change compile command')
@click.option('-e', '--execute', help='Change execute command')
@click.option('-l', '--langid', help='Change upload language id')
@click.option('-d', '--default', is_flag=True, help='Set as default template')
def modify(ctx, platform, name, newname, path, compile, execute, langid, default) -> None:
  """Update current template

  PLATFORM    Platform Name, (AtCoder,Codeforces)

  NAME        Custom template name
  """
  tm: TemplateManager = ctx.obj[DI_TEMPMAN]
  logger: logging.Logger = ctx.obj[DI_LOGGER]
  logger.debug(f"{platform}, {name}, {path}, {compile}, {execute}, {langid},{default}")
  tm.update_template(platform=platform,
                     alias=name,
                     newalias=newname,
                     path=path,
                     compilation=compile,
                     execute=execute,
                     uplang=langid,
                     default=default)
