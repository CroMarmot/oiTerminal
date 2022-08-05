#!/usr/bin/env python3
from sys import argv

platformNames = ["Codeforces", "AtCoder"]
isDebug = False


def debug(s: str):
  if not isDebug:
    return
  with open('/tmp/ot-auto-completion-debug.log', 'a') as f:
    f.write(s)


def platformKey():
  res = {}
  for k in platformNames:
    res[k] = {}
  return res


# TODO auto generate by click
cliAccept = {
    "init": {},
    "config": {
        "account": {
            "list": {},
            "new": {},
            "modify": {},
            "delete": {},
            "test": {},  # TODO test login
        },
        "template": {
            "list": {},
            "new": {},
            "modify": {},
            "delete": {},
        }
    },
    "problem": {
        "fetch": platformKey()
    },
    "contest": {
        "list": platformKey(),
        "detail": platformKey(),
        "standing": platformKey(),
        "fetch": platformKey(),
    },
    "test": {},
    "submit": {}
}


def main():
  # first is python scripts name, second is program name
  debug(str(argv))
  ptr = cliAccept
  for i in range(2, len(argv)):
    key = argv[i]
    if key in ptr:
      ptr = ptr[key]
    else:
      print()
      return
  for k in ptr:
    print(k, end=' ')
  print()


if __name__ == '__main__':
  main()
