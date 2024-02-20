# v0.2

- [ ] more `unit testable code`
- [ ] Watch submissions' status dynamically.
- [ ] Clone all codes of someone.
- [ ] List problems' stats of one contest.
- [ ] 题目获取 `oi problem Codeforces 1234A`
- [ ] 提交语言信息`oi lang Codeforces`
- [ ] 平台特殊配置? |`oi browser www.codeforces.com [--rcpc rcpc]`|
- [ ] 缩写名字工具?
- [ ] webbrowser support aes codeforces
- [ ] Test with debug / product
- [ ] 增加事件 通知(插件支持)
- [ ] 需要捕获 并重新输出 编译 和 运行时的stderr
- [ ] stack-size:
  - todo fix atcoder abc334 stack-overflow 过多递归core dump,需要ulimit,调用docker?  ./Main < in.testcase28.txt: Segmentation fault (core dumped)
  - Windows: g++ -Wl,--stack=268435456 file.cpp works in
  - Linux:
    - ulimit -s  262144     (256mb, 我电脑目前默认是8mb)
    - ulimit -s unlimited   (这个非root会报错ulimit: stack size: cannot modify limit: Operation not permitted)
  - MacOS:
    - stack_size


