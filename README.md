# Oi Terminal

Coding

# Plan

- [ ] 获取比赛
    - [ ] 获取比赛基本信息
    - [ ] 获取比赛的题目
    - [ ] 获取比赛进行时间
    
- [ ] 获取题目
    - [ ] 获取题目基本信息
    - [ ] 获取内存限制 运行时间限制
    - [ ] 获取测试样例
    
- [ ] 分析并下载测试

- [ ] 多语言支持
    - [ ] 语言检测
    - [ ] 测试
    - [ ] 不同语言提交

- [ ] 不同的oj支持 [virtualJudge 支持 除去(分析样例和测试)的功能]

- [ ] 登录/提交

- [ ] 获取测试结果

# Funcitions

测试是本地的，所有通用不分平台，只分语言

|Local language|supported?|
|:---:|:---:|
|C++17|no|
|C++14|no|
|C++11|no|
|Java8|no|
|Python3|no|
|Python2|no|
|Go1.9|no|

和平台相关

|Platforms|fetch|test_case|submit|result|code ref|
|---|---|---|---|---|---|
|Codeforces| Contest/Problem|Yes| | |VirtualJudge|
|aizu| | | | |VirtualJudge|
|hdu| | | | |VirtualJudge|
|poj| | | | |VirtualJudge|
|wust| | | | |VirtualJudge|
|zoj| | | | |VirtualJudge|

# 关于语言

 - [ ] 语言(和本地编写测试对应)

 - [ ] 提交语言(和oj的设置对应)
   - [ ] virtualJudge 提供了远端语言列表获取
   - [ ] 之后根据这个改一个 显示值列表的
   

# 思考

职责划分

Core: 载入oj ，和用户直接交流， 调用oj

utils: 网络工具 登录 cookie

具体Oj 例如CF

parser/submit/test 调用core

# Usage

依然是`config.json` 不加入 版本 ，只留一个模板`_config.json`

- [x] 首先`cp _config.json config.json` 并编辑`config.json` TODO 增加config相关说明?

- [x] 分析比赛举例 ./parser.py cf 1112` 1112为比赛id(url 上的不是 带井号的)

- [x] 编写代码，例如`cd dist/Codeforces/1112-C++17/`

- [x] 测试代码 例如`./test.py A`

- [x] 提交测试代码 例如`./submit.py A`


# Coding

先只支持json配置,之后再增加配置优先级别。

# 面向使用的思考

- [ ] 方案1. 启动后等待接受命令行方式

- [x] 方案2. parser test submit 分开 (+soft link)


# 参考/依赖

[VirtualJudge/spider](https://github.com/VirtualJudge/spider)

[Beautiful 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
