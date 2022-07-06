# Oi Terminal [![Build Status](https://travis-ci.org/CroMarmot/oiTerminal.svg?branch=dev)](https://travis-ci.org/CroMarmot/oiTerminal)

**Codeforces 在比赛时 新增了aes保护, 本工具暂时不能在比赛时使用, 需要cookies中增加RCPC, next分支已经支持**

AtCoder 目前会出现Ex为题号但是链接是`_h`后缀的, 处理上有些问题,如[ABC255Ex](https://atcoder.jp/contests/abc255/tasks/abc255_h),可以自动获取和测试,需要手动提交

python3.6+

## Supported platform

|Platforms|contest|test_case|submit|result|reg contest|short name|
|---|---|---|---|---|---|---|
|Codeforces|Yes|Yes|Yes|Yes|Yes|cf|
|AtCoder|Yes|Yes|Yes|Yes|No|ac|

## Usage

### Install dependency

```shell
pip3 install -r requirements.txt
```

### Config username and password

- copy `_config.json` to `config.json` and modify it

- Check the [lang.json](./lang.json) for `lang` field

### Config submit language in each platform

- Check the [LANG.md](./LANG.md) for `up_lang` field

### Config your template code

- Put your template code under `template/`, the filename should be equal to the `template` field in `lang.json`

### Parse codeforces contest

- `./contest.py cf 1112` 1112 is contest id (which is in url instead of the number after `#`)

### Parse atcoder contest

- `./contest.py ac abc255` same as codeforces, find it in url

### Write code

any way you like，e.g. `vim A.cpp`

### Test code

e.g. `./test.py A`

### Submit code and wait the result

e.g. `./submit.py A`

### register codeforces contest

```shell
./reg.py cf <contestId>
```

example:

```shell
./reg.py cf 1198
```

## Q&A

### I'm using Windows, how can I using this tool?

Windows has [WSL(Windows Subsystem Linux)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) !

and [Announcing WSL 2](https://devblogs.microsoft.com/commandline/announcing-wsl-2/)

You can enjoy Linux on Windows !

### I'm using `g++/gcc` instead of `clang++` ,or I'm using `pypy` instead of `python3` where is setting?

just modify the `lang.json` file

### `--ignore-trailing-space` not support

This program is using `diff` to compare the result. However this command has different arguments in Linux and Mac OS, you can change the `diff_cmd` and `show_diff_cmd` in `test.py`

### Enable `develop` envirnoment

default environment is `production`

enable `develop` environment:

```shell
export OITERMINAL_ENV=dev
```

## ref / dependency

[VirtualJudge/spider](https://github.com/VirtualJudge/spider)

[BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[colors](https://misc.flogisoft.com/bash/tip_colors_and_formatting)
