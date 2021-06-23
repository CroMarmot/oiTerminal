# Oi Terminal [![Build Status](https://travis-ci.org/CroMarmot/oiTerminal.svg?branch=dev)](https://travis-ci.org/CroMarmot/oiTerminal)

> Coding...

python3.6+ only, https://www.python.org/dev/peps/pep-0526/

## Supported platform:

|Platforms|fetch|test_case|submit|result|code ref|short name|contest/problem example|
|---|---|---|---|---|---|---|---|
|Codeforces|Contest|Yes|Yes|Yes|VirtualJudge|cf|1112|
|AtCoder|Contest|Yes|Yes|Yes|None |ac|abc101|
|CometOJ(planing)|No|No|No|No|None |comet|2|
|bzoj(planing)|No|No|No|No|None |bz||
|aizu|No|No|No|No|VirtualJudge|||
|hdu|No|No|No|No|VirtualJudge|||
|poj|No|No|No|No|VirtualJudge|||
|wust|No|No|No|No|VirtualJudge|||
|zoj|No|No|No|No|VirtualJudge|||

# Usage

- [x] `pip3 install -r requirements.txt`

- [x] `cp _config.json config.json` and modify `config.json` About `up_lang` using `./lang.py --oj cf`

- [x] write your templateCodeFile under `template/`, the filename should be equal to the 'template' field in `lang.json`

- [x] parse contest `./contest.py cf 1112` 1112 is contest id (which is in url instead of the number after `#`)

- [ ] TODO 2.1 parse single problem `./problem.py cf 1112A`

- [x] writing code any way you like，e.g. `vim A.cpp`

- [x] test code e.g. `./test.py A`

- [x] submit code e.g. `./submit.py A`

# register contest

> codeforces

`./reg.py cf <contestId>`

example:`./reg.py cf 1198`

# Functions

Test is in local, regardless of the platform , only language

Local language supported:`./lang.py`, current supported:`C++`,`C++11`,`C++14`,`C++17`,`Java8`,`Python3`,`Python2`,`Rust`,`Go`

Platform language (example: `./lang.py --oj cf`)

# Q&A

> I'm using Windows, how can I using this tool?

Windows has [WSL(Windows Subsystem Linux)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) !

and [Announcing WSL 2](https://devblogs.microsoft.com/commandline/announcing-wsl-2/)

You can enjoy Ubuntu on Windows !

> I'm using `g++/gcc` instead of `clang++` ,or I'm using `pypy` instead of `python3` where is setting?

check the `lang.py` file

> `--ignore-trailing-space` not support

The program is using `diff` to compare the result. However this command has different arguments in different OS, you can change the `diff_cmd` and `show_diff_cmd` in `test.py`

# About

- [ ] Get Contest
    - [ ] basic info
    - [x] problem's in contest
    - [ ] running date
    
- [ ] Fetch problem
    - [x] basic info
    - [ ] memory limit & time limit
    - [x] test case
       
- [ ] programming language support
    - [ ] language list fetch, check and show
    - [x] test code in local with test case
    - [x] submit for different language

- [x] login

- [x] fetching submit result

- [x] Language tool
    - [x] get supported local language
    - [x] get remote oj language key-value pair

# TODO

- [ ] 增加交互性配置过程，减少手动配置操作，合并配置文件 目测不兼容 计划到v2

- [ ] MacOS系统的diff命令参数不同，提取比较命令到配置文件

- [ ] 增加 调用系统命令的test，比如 diff方法调用的

- [ ] websocket 获取codeforces的当前测试节点个数，目前api在测试过程中始终返回0

- [ ] 不是取最后一题，而是根据题目id等信息请求分析出提交id(可能性能会略低)

- [ ] 打一半发现忘记注册了，增加是否注册的检测或者提醒？

- [ ] more arg support in python 先只支持json配置 和简单的语言参数支持,之后再增加配置优先级别。

- [ ] config.json checker

- [ ] BUG: 大于小于号等会转义的html字符的处理

- [ ] pytest mypy, mypy可以检查方法，但是如果是网络请求回来的数据不一定满足，如果用assert感觉太丑，求好的办法

- [ ] tox 用于建立孤立环境，安装依赖，指定py版本，调用其它测试

- [ ] travis CI 在线自动测试 增加测试内容

- [ ] 编写 文档 wiki

- [ ] 增加 config.py 取代手工配置 配合db.py(做成代理式)+sqlite

- [ ] 增加 安静模式 和全输出模式(-v/-debug), 增加更改log设计

- [ ] 网络崩溃处理 例如agc033

- [ ] 处理掉所有JSON文件，改为类

- [ ] 把部分json配置改为sqlite配置

- [ ] 不合理的else清理

- [ ] Codeforces:IDLENESS_LIMIT_EXCEEDED

- [ ] add fetch state for bad network

# envirnoment

default environment is production

develop environment:`OITERMINAL_ENV=dev`

# ref / dependency

[VirtualJudge/spider](https://github.com/VirtualJudge/spider)

[BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[colors](https://misc.flogisoft.com/bash/tip_colors_and_formatting)


