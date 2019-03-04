import json
import os

from oiTerminal.model import Account, Problem, Contest, TestCase
from oiTerminal.core import Core

dist = "dist"


def language(remote_oj):
    return json.dumps({
        'languages': Core(remote_oj).find_language(account=Account('robot4test', 'robot4test'))
    })


def get_problem(
        oj: str,
        pid: str,
        account: Account):
    _problem = Core(oj).get_problem(pid=pid, account=account)
    return _problem


def get_contest(oj: str, cid: str, account: Account):
    # test support contest TODO
    return Core(oj).get_contest(cid, account=account)


def supports():
    return json.dumps({
        'supports': Core.get_supports()
    })


def create_contest_files(contest: Contest = None):
    if contest is None:
        print("contest is None")
    folder = dist + "/" + contest.oj + "/" + contest.id + "/"
    print(folder)
    os.makedirs(folder, exist_ok=True)  # TODO rm exist ok = true
    for problem_id, problem_detail in contest.problem_set.items():
        pd: Problem = problem_detail
        with open(folder + problem_id + '.html', "w") as problem_html:
            problem_html.write(pd.html)
            problem_html.close()
        for i in range(len(pd.test_case)):
            tc: TestCase = pd.test_case[i]
            with open(folder + problem_id + '.in.' + str(i), "w") as tc_in:
                tc_in.write(tc.sample_in)
                tc_in.close()
            with open(folder + problem_id + '.out.' + str(i), "w") as tc_out:
                tc_out.write(tc.sample_out)
                tc_out.close()


# TEST -----

def test_contest():
    _contest = get_contest(
        oj="Codeforces",  # 和 codeforces.py 的Class name 对应
        cid='1118',
        account=Account('robot4test', 'robot4test'))
    print(vars(_contest))
    create_contest_files(_contest)


def test_problem():
    _problem = get_problem(
        oj="Codeforces",  # 和 codeforces.py 的Class name 对应
        cid='1118',
        account=Account('robot4test', 'robot4test'))
    print(vars(_problem))


if __name__ == '__main__':
    test_contest()
