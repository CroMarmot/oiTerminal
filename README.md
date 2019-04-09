# Oi Terminal

Coding...

Workable for Codeforces contest now !

- [x] Codeforces
- [ ] Atcoder(working)

python3 only

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

platform:

|Platforms|fetch|test_case|submit|result|code ref|
|---|---|---|---|---|---|
|Codeforces|Contest|Yes|Yes|Yes|VirtualJudge|
|AtCoder| | | | | |
|aizu| | | | |VirtualJudge|
|hdu| | | | |VirtualJudge|
|poj| | | | |VirtualJudge|
|wust| | | | |VirtualJudge|
|zoj| | | | |VirtualJudge|

# Usage

- [x] `pip3 install -r requirements.txt`

- [x] `cp _config.json config.json` and modify `config.json` About `up_lang` using `./lang.py --oj cf`

- [x] write your templatecodefile under `template/`, the filename should be equal to the 'template' field in `lang.json`

- [x] parse contest `./parser.py cf 1112` 1112 is contest id (which is in url instead of the number after `#`)

- [ ] TODO 2.1 parse 1 problem `./parser.py cf 1112A`

- [x] writing code any way you like，e.g. `vim A.cpp`

- [x] test code e.g. `./test.py A`

- [x] submit code e.g. `./submit.py A`


# TODO

- [ ] more arg support in python 先只支持json配置 和简单的语言参数支持,之后再增加配置优先级别。

- [ ] config.json checker

- [ ] atcoder

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
