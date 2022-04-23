#!/usr/bin/env python3
from sys import argv

platformNames = ["Codeforces","Atcoder"]
basekey = ["init","contest","contestdetail","config"]

def main():
    # first is python scripts name, second is program name
    with open("/tmp/out", "a") as f:
        f.write(str(argv) + "\n")
    if len(argv) == 2:
        for v in basekey:
            print(v, end = ' ')
        print()
    elif len(argv) == 3:
        with open("/tmp/out", "a") as f:
            f.write(" argv == 3 \n")
        if argv[2] == 'contest':
            with open("/tmp/out", "a") as f:
                f.write("out platformNames\n")
            for v in platformNames:
                print(v, end = ' ')
            print()
    else:
        print()

if __name__ == '__main__':
    main()

# Usage
# modify `.py` path in `ot-auto-complete.sh`
# run `source ot-auto-complete.sh`
