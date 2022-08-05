# oiTerminal

## Install Dependency

```bash
git clone https://github.com/CroMarmot/yxr-atcoder-core.git
cd yxr-atcoder-core
pip3 install -e .
```

## Install

```bash
git clone https://github.com/CroMarmot/oiTerminal -b He
cd oiTerminal
pip3 install -e .
```

```bash
# Enable tab auto completion
./auto-completion/gen-ot-auto-completion.sh
source /tmp/ot-auto-completion.sh
```

## oi Cheeat Sheat

|Feature|Command|
|---|---|
|initial create `.oiTerminal`folder|`oi init`|
| - [x] 新增用户|`oi config account new <platform> <account> [--default]`|
| - [x] 查看用户|`oi config account list` |
| - [x] 更改用户|`oi config account modify <platform> <account> [--pass] [--default]`|
| - [x] 删除用户|`oi config account delete <platform> <account>`|
| - [x] 新增模板|`oi config template new <platform> <name>  <path> <compile command> <execute command> <submit lang id> [--default]`|
| - [x] 查看模板|`oi config template list`|
| - [x] 更新模板|`oi config template modify <platform> <name> [--path <path>] [--compile <compile command>] [--execute <execute command>] [--submitlangid <submit lang id>] [--default]`|
| - [x] 删除模板|`oi config template delete <platform> <alias>`|
| - [x] 比赛列表|`oi contest list <platform>`|
| - [x] 比赛详情|`oi contest detail <platform> <contest id>`|
| - [x] 比赛排名|`oi contest standing <platform> <contest id>`|
| - [x] 拉取比赛|`oi contest fetch <platform> <contest id>`|
| - [ ] 题目获取|`oi problem fetch <platform> <problem id>`|
| - [ ] 提交语言信息|`oi lang <platform>`|
| - [ ] 平台特殊配置? |`oi browser www.codeforces.com [--rcpc rcpc]`|
| - [x] 测试当前文件夹代码|`oi test`|
| - [x] 提交当前文件夹代码|`oi submit`|

## TODO

手动添加`.oiTerminal/CF_RCPC`, 内容为浏览器中`cookie`的`RCPC`字段

```text
xxxxxxxxxxxxxxxxxxxxxxxx
```
