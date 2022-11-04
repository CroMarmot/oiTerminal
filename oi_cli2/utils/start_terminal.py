import os


def start_terminal(folder: str):
  os.chdir(folder)
  os.system("$SHELL")
