from sys import argv

import sys


def main():
  if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} <scripts> [arg0[ arg1[ ... ]]]")
    return
  # python3 curry.py oiTerminal.custom.Codeforces.contestList
  if sys.argv[1] == 'oiTerminal.custom.Codeforces.contestList':
    from oiTerminal.custom.Codeforces.contestList import main
    main()
  pass


if __name__ == '__main__':
  main()
