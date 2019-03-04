# Oi Terminal

Coding

# Plan

多语言支持

不同的oj支持

基本功能

> 对于有比赛的 能够分析比赛题目 分析比赛时间？ ...[TODO]

对于单个题目

> 获取题目 获取 内存限制 运行时间限制

> 分析并下载测试

> 多语言测试

> 登录并提交

> 获取测试结果


类的参数接受

用户名

密码

语言(和本地编写测试对应)

提交语言(和oj的设置对应)

题目(不同oj 独自内部处理)


# 思考

职责划分

Core: 载入oj ，和用户直接交流， 调用oj

utils: 网络工具 登录 cookie

具体Oj 例如CF


# 面向使用的思考

 x 方案1. 启动后等待接受命令行方式

- [x] 方案2. parser test submit 分开 (soft link)







# 参考/依赖

[VirtualJudge/spider](https://github.com/VirtualJudge/spider)
