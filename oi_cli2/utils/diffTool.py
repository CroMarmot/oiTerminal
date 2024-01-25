import os
from typing import Any

from oi_cli2.cli.constant import RED, DEFAULT
# mac os 的命令似乎不支持 --ignore-trailing-space
diff_cmd = "diff --brief -B --ignore-trailing-space"  # 用于比较
show_diff_cmd = "diff -B --ignore-trailing-space -y"  # 用于展示差异


# TODO 非系统命令diff, 改为 自己实现函数/注入式/支持交互
def diff_result_fn(std_in_file: str, std_out_file: str, user_out_file: str) -> None:
  diff = os.system(f"{diff_cmd} {std_out_file} {user_out_file}")
  if diff != 0:
    print(RED)
    print("==============================================================================")
    with open(std_in_file,'r') as f:
      lines = f.readlines()
      for line in lines[:100]:
        print(line,end='')
      if len(lines) > 100:
        print("...more")
    # os.system(f"cat {std_in_file}")
    print("\n-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -")
    os.system(f"{show_diff_cmd} {std_out_file} {user_out_file}")
    print("\n==============================================================================")
    print(DEFAULT)
