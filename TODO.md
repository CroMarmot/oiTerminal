# v0.2

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
## 方案思考记录

### state.json

提交 测试等使用的题目配置信息。

用户名，密码不在此处，在工具总管理的地方(version 1 一直是)

应该由原来的一部分（总管理工具）改为两部分：（总管理工具，平台自定义）

## 参考

https://github.com/xalanq/cf-tool

# Utils

缩写名字工具

网络请求工具

文件读写工具

命令行交互工具

减少了 传递引用修改，改为使用返回值（1 是更清晰吧，吗？2 是并不是巨大代价来创建）

一个目标 为了之后新写平台支持，少写代码，

向 git 学习，用户的目录，需要 `.oiTerminal` 文件夹，内部是 配置类的, 所以向上找第一个包含 `.oiTerminal` 的文件夹

## webbrowser support aes codeforces
