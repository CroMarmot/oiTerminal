# Oi Terminal

Coding

# State

Workable for Codeforces contest now !

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

# Functions

Test is in local, regardless of the platform , only language, `oiTerminal/utils.py :: LanguageUtil`

|Local language|supported?|
|:---:|:---:|
|C++|Yes|
|C++11|Yes|
|C++14|Yes|
|C++17|Yes|
|Java8|no|
|Python3|no|
|Python2|no|
|Go1.9|no|

platform:

|Platforms|fetch|test_case|submit|result|code ref|
|---|---|---|---|---|---|
|Codeforces|Contest|Yes|Yes|Yes|VirtualJudge|
|aizu| | | | |VirtualJudge|
|hdu| | | | |VirtualJudge|
|poj| | | | |VirtualJudge|
|wust| | | | |VirtualJudge|
|zoj| | | | |VirtualJudge|

# Usage

- [x] 1. `cp _config.json config.json` and modify `config.json` TODO 增加config相关说明? 比如up_lang

- [x] 2. parse contest `./parser.py cf 1112` 1112 is contest id (which is in url instead of the number after `#`)

- [ ] TODO 2.1 parse 1 problem `./parser.py cf 1112A`

- [x] writing code any way you like，e.g.

- [x] test code e.g. `./test.py A`

- [x] submit code e.g. `./submit.py A`


# TODO

more arg support in python 先只支持json配置,之后再增加配置优先级别。


# ref / dependency

[VirtualJudge/spider](https://github.com/VirtualJudge/spider)

[Beautiful 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
