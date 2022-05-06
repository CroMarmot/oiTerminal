import getpass
from oiTerminal.cli.constant import CIPHER_KEY

from oiTerminal.utils.account import AccountManager
from oiTerminal.utils.enc import AESCipher


def account_list(am: AccountManager):
  acc_list = am.get_list()
  for i in range(len(acc_list)):
    if i == 0 or acc_list[i].platform != acc_list[i-1].platform:
      print(acc_list[i].platform)
    mark = ' '
    if acc_list[i].default:
      mark = '*'
    print(f'\t {mark} {acc_list[i].account}')
  if len(acc_list) == 0:
    print("Account List is empty.")


def account_new(am: AccountManager):
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

  acc = input("Account:")
  password = getpass.getpass("Password:")

  cf_rcpc = None
  if index == 1:
    cf_rcpc = getpass.getpass("Codeforces rcpc:")

  am.add_account(platform, acc, password, cf_rcpc)


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
  print("3) Set Default")
  print("4) Delete")
  print("5) Change Account cf_rcpc")
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
  elif index == 5:
    cf_rcpc = getpass.getpass("Enter User Codeforces RCPC:")
    am.modify_cf_rcpc(acc_index, cf_rcpc)


def account(db):
  print("1) Account List")
  print("2) New Account")
  print("3) Modify Account")
  try:
    index = int(input("> "))
  except(Exception):
    print("input error")

  am = AccountManager(db=db, cipher=AESCipher(CIPHER_KEY))

  if index == 1:
    account_list(am)
  elif index == 2:
    account_new(am)
  elif index == 3:
    account_modify(am)
  else:
    print("input error")
