#!/usr/bin/env python3
import click

from oi_cli2.cli.config import config
from oi_cli2.cli.contest import contest
from oi_cli2.cli.init import init
from oi_cli2.cli.submit import submit_command
from oi_cli2.cli.test import tst_command


@click.group()
@click.pass_context
def main(ctx={}):
  ctx.obj = {}
  #     description='oi-cli for AtCoder & Codeforces')
  # TODO problem contest test submit
  # TODO move to auto test

  # exit(1)
  # if ops[0] == 'problem':
  #   from oiTerminal.cli import problem
  #   problem.main(argv=args.args, logger=logger, folder=folder)
  # else:
  #   parser.print_help()


main.add_command(init)
main.add_command(config)
main.add_command(contest)
main.add_command(tst_command)
main.add_command(submit_command)