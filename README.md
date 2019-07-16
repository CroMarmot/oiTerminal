# Oi Terminal


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

- [x] write your templatecodefile under `template/`, the filename should be equal to the 'template' field in `lang.json`

- [x] parse contest `./contest.py cf 1112` 1112 is contest id (which is in url instead of the number after `#`)

- [ ] TODO 2.1 parse single problem `./problem.py cf 1112A`

- [x] writing code any way you like，e.g. `vim A.cpp`

- [x] test code e.g. `./test.py A`

- [x] submit code e.g. `./submit.py A`

# Functions

Test is in local, regardless of the platform , only language

Local language:`./lang.py`

Platform language (example: `./lang.py --oj cf`)

|Local language|supported?|
|:---:|:---:|
|C++|Yes|
|C++11|Yes|
|C++14|Yes|
|C++17|Yes|
|Java8|Yes|
|Python3|Yes|
|Python2|Yes|
|Go1.9|no|
|JS|no|
|Rust|no|

# Q&A

> I'm using Windows, how can I using this tool?

Windows has [WSL(Windows Subsystem Linux)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) !

and [Announcing WSL 2](https://devblogs.microsoft.com/commandline/announcing-wsl-2/)

You can enjoy Ubuntu on Windows !

# Plan

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

- [ ] different oj [virtualJudge 支持 除去(分析样例和测试)的功能]

- [x] login

- [x] fetching submit result

- [x] Language tool
    - [x] get supported local language
    - [x] get remote oj language key-value pair

# TODO

- [ ] more arg support in python 先只支持json配置 和简单的语言参数支持,之后再增加配置优先级别。

- [ ] config.json checker

- [ ] atcoder


1. 父类/公用 model逻辑设计

util:

网络访问

文件访问

配置读取

语言

lang:

get_language(account)

core: 直接调用oj的方法

oj:模拟请求，访问，分析页面，返回键值对表 -> Object LangKV

core: 分析结果打印展示

---

parser:

parser_contest(contestId,account):

parser_problem(problemId,account)


core:

读取 题目、比赛，语言，用户名密码， 调用oj.parser_context()，

oj:

根据 题目、比赛，用户,进行网络请求（util），分析页面结果，返回给core，Object_CONTEST 或 Object_PROBLEM

core:

对结果进行 生成文件，拷贝模板，跳转目录

---

test:

core: 分析参数 state.json,直接本地测试，和oj无关

---

submit

submit(problemID,account,filepath)

getresult(problemID,account)

core: 分析参数，调用oj的submit,

oj: 模拟请求，返回 `提交`结果，不包括测试结果, OBJECT_SUBMIT_STAT

core: 分析结果，进行展示，如果成功提交，开始调用oj获取结果

oj: 模拟请求，具体实现，api或其它,返回，返回OBJECT_RESULT

core:展示 成果错误，或者等待状态再请求。


2. 增加测试

3. pytest mypy

mypy可以检查方法，但是如果是网络请求回来的数据不一定满足，如果用assert感觉太丑，求好的办法

用于测试

4. tox

用于建立孤立环境，安装依赖，指定py版本，调用其它测试

5. travis CI

在线自动测试

[![Build Status](https://travis-ci.org/CroMarmot/oiTerminal.svg?branch=dev)](https://travis-ci.org/CroMarmot/oiTerminal)

---

测试样例



公用 错误设计

1. 必须的文件,未找到
2. 


编写 文档

TODO 增加 config.py 取代手工配置

TODO 增加 安静模式 和全输出模式(-v/-debug), 增加更改log设计

TODO 网络崩溃处理 例如agc033

TODO 处理掉所有JSON文件，改为类

TODO 把部分json配置改为sqlite配置

# flow

testflow:

0. read problemId from arg (exp.'A')
1. read state from `state.json` (exp. lang = C++)
2. copy file (exp. A.cpp) to TESTFOLDER/Main.<suffix> (exp cpp)
3. compile
4. exe

# ref / dependency

[VirtualJudge/spider](https://github.com/VirtualJudge/spider)

[Beautiful 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

[colors](https://misc.flogisoft.com/bash/tip_colors_and_formatting)
