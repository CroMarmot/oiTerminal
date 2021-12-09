# v0.2

## plan

- [ ] 分析管理？？

状态/数据 (是否默认(默认管理器？

- [x] 账号:(平台, 账号,密码, 加解密工具)
- [x] 模板:(平台，别名，模板在本地的路径，编译命令，执行命令，清理命令)
- [x] 平台:(名称，地址，提交语言映射表)

操作,结果(主要和操作对应)

- [ ] 平台:(登录，获取分析题目/比赛，查看题目/比赛/登录状态，提交代码，产看映射表)
- [ ] 账号，模板配置 管理

- [x]  加解密工具
- [x]  日志工具
- [x] 路径上模拟.git 的思路，使用最近.oiTerminal 所在的位置为 根目录
- [ ]  本地jsondb/sqlite工具


## more modularization

    cli -> core
    python restful api server -> core

## partition

- [ ] core:
  - [ ] db:
    - [ ] config
  - [ ] log:
    - [ ] error.log
  - [ ] generate folder
  - [x] generate template code
  - [ ] dispatcher:
    - [ ] register contest
    - [ ] fetch problem
      - [ ] download html
      - [ ] analysis test example
    - [ ] call compiler
    - [ ] test code in local environment with analysis example input/output
    - [ ] submit code
    - [ ] dynamic get result
- [ ] utils(flat lib):
  - [ ] db:

  - [ ] log:

  - [ ] network:
    - [ ] websocket:
    - [ ] json api:

## more `unit testable code`

maybe Dependency Injection ?

## Codeforces

- [ ] Support Contests, Gym, Groups and acmsguru.
- [ ] Support all programming languages in Codeforces.
- [ ] Submit codes.
- [ ] Watch submissions' status dynamically.
- [ ] Fetch problems' samples.
- [ ] Compile and test locally.
- [ ] Clone all codes of someone.
- [ ] Generate codes from the specified template (including timestamp, author, etc.)
- [ ] List problems' stats of one contest.
- [ ] Use default web browser to open problems' pages, standings' page, etc.
- [ ] Setup a network proxy. Setup a mirror host.
- [ ] Colorful CLI.

## Design

- [ ] Support Contests, Gym, Groups and acmsguru.
- [x] Support all programming languages in Codeforces.
- [x] Submit codes.
- [ ] Watch submissions' status dynamically. TODO: api -> websocket
- [x] Fetch problems' samples.
- [x] Compile and test locally.
- [ ] List problems' stats of one contest.
- [ ] Use default web browser to open problems' pages, standings' page, etc.
- [ ] Setup a network proxy. Setup a mirror host.

---

- [ ] (Part support, Later) Generate codes from the specified template (including timestamp, author, etc.)
- [ ] (Later) Colorful CLI.
- [ ] (Not in plan) Clone all codes of someone.

- [ ] `pull [ac] [<specifier>...]`
- [ ] `clone [ac] [<handle>]`
- [ ] `sid [<specifier>...]`
- [ ] `upgrade`
- [ ] `open [<specifier>...]`
- [ ] `stand [<specifier>...]`
- [ ] `gen [<alias>]`
- [ ] `watch [all] [<specifier>...]`

cli

- [ ] `config`
  - [ ] account
    - [ ] platform
    - [ ] back
      - [ ] username
      - [ ] password
  - [ ] template (for local test)
    - [ ] alias
    - [ ] path
    - [ ] compile
    - [ ] exec
    - [ ] clean
  - [ ] analyze
    - [ ] platform
      - [ ] default local language
      - [ ] default platform language
            <hinter ?>
- [ ] helper
  - [ ] display language id
  - [ ] firefox
- [ ] `register contest`  

- [ ] `submit`
  - [ ] `[-f <file>]`
- [ ] `list [<specifier>...]`
  - [ ] 查看题目列表和状态
- [ ] `parse [<specifier>...]` 按照单个题目获取
- [ ] `test [<file>]`
- [ ] `race [<specifier>...]` 如果比赛还未开始且进入倒计时，则该命令会倒计时。倒计时完后，会自动打开一些题目页面并拉取样例。
- [ ] 命令使用频次统计
- [ ] 本地多 log

## 方案思考记录

### 题目分析结构

```
1409
├── A.html
├── A.in.0
├── A.out.0
├── B.html
├── B.in.0
├── B.out.0
├── C.html
├── C.in.0
├── C.out.0
├── D.html
├── D.in.0
├── D.out.0
├── E.html
├── F.html
├── F.in.0
├── F.in.1
├── F.in.2
├── F.in.3
├── F.out.0
├── F.out.1
├── F.out.2
└── F.out.3

1409-C++17/
├── A.cpp
├── B.cpp
├── C.cpp
├── D.cpp
├── E.cpp
├── F.cpp
├── log
│   └── oiTerminal.log
├── state.json
├── submit.py -> ../../../submit.py
├── TEST
│   ├── A.out.0
│   ├── B.out.0
│   ├── C.out.0
│   ├── Main
│   └── Main.cpp
└── test.py -> ../../../test.py
```

> 老结构

    /cf/..

特点
分离了题目数据和用户
自动进入比赛文件夹后，`vim [X].cpp`，比较方便，`test.py` 等需要增加题目即可

> 新考虑的结构

    cf/contest/id/[X]/
    cf/gym/id/[X]/

差别
完全以单个题目为单位
在初始化打开时相对麻烦，需要多 cd 几次
对于后续的单题目支持，和 gym 支持，甚至非比赛的其它平台单个题目的支持的最小单位

### 多维度目录结构

对于一个题目的维度

平台，比赛 id，语言，题目 id

语言其实是两个部分，本地调试编译语言，和平台对应的编译器序号。

思考了一下，平台又总的管理工具创建文件夹，而内部的 `f(比赛id,语言,题目id)` 由平台的函数提供文件夹路径， =>

因为希望可以多语言支持，所以（题目和解析结果）和（代码测试）的分开？

### state.json

提交 测试等使用的题目配置信息。

用户名，密码不在此处，在工具总管理的地方(version 1 一直是)

应该由原来的一部分（总管理工具）改为两部分：（总管理工具，平台自定义）

## 参考

https://github.com/xalanq/cf-tool

```json
{
  "template": [
    {
      "alias": "cpp",
      "lang": "54",
      "path": "/tmp/a.cpp",
      "suffix": ["cpp"],
      "before_script": "g++ $%full%$ -o $%file%$.exe -std=c++17",
      "script": "./$%file%$.exe",
      "after_script": "rm $%file%$.exe"
    }
  ],
  "default": 0,
  "host": "https://codeforces.com",
  "folder_name": {
    "acmsguru": "acmsguru",
    "contest": "contest",
    "group": "group",
    "gym": "gym",
    "root": "cf"
  }
}
```

核心依然是 DI，使用应用层面尽量少代码，多配置

# Utils

缩写名字工具

网络请求工具

文件读写工具

命令行交互工具

减少了 传递引用修改，改为使用返回值（1 是更清晰吧，吗？2 是并不是巨大代价来创建）

一个目标 为了之后新写平台支持，少写代码，

向 git 学习，用户的目录，需要 `.oiTerminal` 文件夹，内部是 配置类的, 所以向上找第一个包含 `.oiTerminal` 的文件夹
