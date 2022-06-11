# TODO

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

