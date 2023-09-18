from typing import Any, Dict, cast
import click
from .reg_list import reg_list

# TODO inject account

platformNames = list(reg_list.keys())


def platformKey() -> Dict[str, Any]:
  res: Dict[str, Any] = {}
  for k in platformNames:
    res[k] = {}
  return res


platformKeys = platformKey()

# TODO auto generate by click
cliAccept = {
    "init": {},
    "config": {
        "account": {
            "list": {},
            "new": platformKey(),
            "modify": platformKey(),
            "delete": platformKey(),
            "test": platformKey(),  # TODO test login
        },
        "template": {
            "list": {},
            "new": platformKey(),
            "modify": platformKey(),
            "delete": platformKey(),
        }
    },
    # "problem": {
    #     "fetch": platformKey()
    # },
    "contest": {
        "list": platformKey(),
        "detail": platformKey(),
        "standing": platformKey(),
        "fetch": platformKey(),
        "open": platformKey(),
        "reg": platformKey(),
    },
    "lang": platformKey(),
    "test": {},
    "submit": {},
    "result": {},
}


@click.command(name="completion")
@click.argument('cmds', nargs=-1)  # unlimited args
def completion_command(cmds):  # (oi, xxx, xxx)
  # Debug
  # with open('/tmp/out','a+') as f:
  #   f.write(str(cmds))
  ptr = cliAccept
  for i in range(1, len(cmds)):
    key = cmds[i]
    if key in ptr:
      ptr = cast(Dict[str, Any], ptr[key])
    else:
      print()
      return
  for k in ptr:
    print(k, end=' ')
  print()
