#!/usr/bin/python3
import argparse
import datetime
import json
import os
import shutil

from oiTerminal.utils import LanguageUtil

RED = "\e[31m"
DEFAULT = "\e[39m"
GREEN = "\e[32m"

TEST_FOLDER = "TEST/"

STATE_FILE = "state.json"

IN_SUFFIX = ".in."
OUT_SUFFIX = ".out."

"""
INPUT_NAME="$1.in."
OUTPUT_NAME="$1.out."
MY_NAME="$1.my."
BIN="$TESTFOLDER/$1"
EXECMD="./$BIN"

mkdir -p ${TESTFOLDER}
file="$1".cpp
if [[ ! -f "$file" ]]; then
echo "$file not found."
exit
fi

if ! clang++ -o ${BIN} ${file} -std=gnu++17 -O2 -g -Wall -Wcomma
then
exit
fi

rm -R ${MY_NAME}* &>/dev/null

i=0
while [[ -f "$INPUT_NAME$i" ]] && [[ -f "$OUTPUT_NAME$i" ]]
    do
input="$INPUT_NAME$i"
output="$OUTPUT_NAME$i"
myoutput="$TESTFOLDER/$MY_NAME$i"

if ! `which time` -o time.out -f "( %es )" ${EXECMD} < ${input} > ${myoutput}; then
echo -e ${RED}"Sample test #$i: Runtime Error""$DEFAULT"
echo "Sample Input #$i"
cat ${input}
echo
elif diff --brief -B --ignore-trailing-space ${myoutput} ${output}; then
echo -e ${GREEN}"Sample test #$i: Accepted"${DEFAULT}
else
echo -e ${RED}"Sample test #$i: Wrong Answer"${DEFAULT}
echo "========================================"
echo "Sample Input #$i"
cat ${input}
echo
echo "Sample Output #$i"
cat ${output}
echo
echo "My Output #$i"
cat ${myoutput}
echo
fi
cat time.out
echo "========================================"
i=$[$i+1]
done


"""


def do_test():
    # get problem id
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help="Problem ID example: A")  # TODO all oj list tool # OJUtil
    args = parser.parse_args()
    pid = args.pid

    # get lang config
    if not os.path.isfile(STATE_FILE):
        raise Exception(STATE_FILE + " NOT EXIST!")
    with open(STATE_FILE) as f:
        state_oj = json.load(f)
        lang = state_oj["lang"]

    # makefolder & mv code 2 folder
    os.makedirs(TEST_FOLDER)
    shutil.copy(pid + LanguageUtil.lang2suffix(lang), TEST_FOLDER + "Main" + LanguageUtil.lang2suffix(lang))

    # compile
    os.chdir(TEST_FOLDER)
    if os.system(LanguageUtil.lang2compile(lang, "Main")) is not 0:
        return

    # run  "" not better than 'time' in bash but worse is better :-)
    i = 0
    std_file = "../../" + state_oj["contestId"] + "/" + pid
    while os.path.isfile(std_file + IN_SUFFIX + str(i)):
        std_out_file = std_file + OUT_SUFFIX + str(i)
        user_out_file = pid + OUT_SUFFIX + str(i)
        start_time = datetime.datetime.now()
        os.system(LanguageUtil.lang2exe(lang, "Main", std_file + IN_SUFFIX + str(i), user_out_file))
        end_time = datetime.datetime.now()
        print("time spend: " + str((end_time - start_time).total_seconds()) + "s")

        # cmp
        diff = os.system("diff --brief -B --ignore-trailing-space " + std_out_file + " " + user_out_file)
        if diff is not 0:
            os.system("diff -B --ignore-trailing-space -y " + std_out_file + " " + user_out_file)

        i += 1

    os.chdir("../")
    shutil.rmtree(TEST_FOLDER)


if __name__ == "__main__":
    do_test()
