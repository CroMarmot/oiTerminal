#!/usr/bin/env python3
from sys import argv

import sys


def main():
  if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} <scripts> [arg0[ arg1[ ... ]]]")
    return
  if sys.argv[1] == 'oiTerminal.custom.Codeforces.contestList':
    # python3 curry.py oiTerminal.custom.Codeforces.contestList
    from oiTerminal.custom.Codeforces.contestList import main
    main()
  elif sys.argv[1] == 'oiTerminal.custom.Codeforces.problemList':
    # python3 curry.py oiTerminal.custom.Codeforces.problemList 1628
    from oiTerminal.custom.Codeforces.problemList import main
    main(sys.argv[2:])
  elif sys.argv[1] == 'oiTerminal.custom.Codeforces.standing':
    # python3 curry.py oiTerminal.custom.Codeforces.standing 1628
    from oiTerminal.custom.Codeforces.standing import main
    main(sys.argv[2:])
  pass


if __name__ == '__main__':
  main()
