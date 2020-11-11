import getpass

from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.enc import AESCipher

def account_list(am:AccountManager):
    acc_list = am.get_list()
    for i in range(len(acc_list)):
        if i == 0 or acc_list[i].platform != acc_list[i-1].platform:
            print(acc_list[i].platform)
        mark = ' '
        if acc_list[i].default:
            mark = '*'
        print(f'\t {mark} {acc_list[i].account}')


def account_new(am:AccountManager):
    print("1) Codeforces")
    print("2) AtCoder")
    try:
        index = int(input("> "))
    except(Exception):
        print("input error")
        return

    if index == 1:
        platform = "Codeforces"
    elif index == 2:
        platform = "AtCoder"
    else:
        print("input error")
        return

    acc = input("account:")
    password = getpass.getpass("password:")

    am.add_account(platform, acc, password)


def account_modify(am: AccountManager) -> object:
    acc_list = am.get_list()

    for i in range(len(acc_list)):
        if i == 0 or acc_list[i].platform != acc_list[i-1].platform:
            print(acc_list[i].platform)
        mark = ' '
        if acc_list[i].default:
            mark = '*'
        print(f'\t {mark} {i}) {acc_list[i].account}')

    try:
        acc_index = int(input("> "))
    except(Exception):
        print("input error")

    if acc_index < 0 or acc_index >= len(acc_list):
        print("input error")
        return

    print("1) Change Account Name")
    print("2) Change Account Password")
    print("3) SetDefault")
    print("4) Delete")
    try:
        index = int(input("> "))
    except(Exception):
        print("input error")

    if index == 1:
        acc = input("Enter User Name:")
        am.modify_name(acc_index, acc)
    elif index == 2:
        password = getpass.getpass("Enter User Password:")
        am.modify_password(acc_index, password)
    elif index == 3:
        am.set_default(acc_index)
    elif index == 4:
        am.delete_account(acc_index)


def account(db):
    print("1) Account List")
    print("2) New Account")
    print("3) Modify Account")
    try:
        index = int(input("> "))
    except(Exception):
        print("input error")

    am = AccountManager(db, AESCipher('6oiTer9'))

    if index == 1:
        account_list(am)
    elif index == 2:
        account_new(am)
    elif index == 3:
        account_modify(am)
    else:
        print("input error")
