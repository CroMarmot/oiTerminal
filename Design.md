# oiTerminal

## 准备

### 初始化环境

安装`apt install python3 python3-venv python3-pytest`

`python3 -m venv venv`

### 启用环境

`. venv/bin/activate`

### 安装依赖

`pip3 install -r requirements.txt`

## ot

|功能|命令|
|---|---|
|初始化,创建`.oiTerminal` 文件夹|`./ot.py init`|
| - [ ] 查看用户|`./ot.py config account list` |
| - [ ] 新增用户|`./ot.py config account new <platform> <account> [--default]`|
| - [ ] 更改用户|`./ot.py config account modify <platform> <account> [--pass] [--default]`|
| - [ ] 删除用户|`./ot.py config account delete <platform> <account>`|
| - [ ] 查看模板|`./ot.py config template list`|
| - [ ] 新增模板|`./ot.py config template new <platform> <alias> <path> <compile command> <execute command> <submit lang id>`|
| - [ ] 更新模板|`./ot.py config template modify <platform> <alias> [--path <path>] [--compile <compile command>] [--execute <execute command>] [--submitlangid <submit lang id>]`|
| - [ ] 删除模板|`./ot.py config template delete <platform> <alias>`|
| - [ ] 比赛列表|`./ot.py contest list <platform>`|
| - [ ] 比赛详情|`./ot.py contest detail <platform> <contest id>`|
| - [ ] 比赛排名|`./ot.py contest standing <platform> <contest id>`|
| - [ ] 拉取比赛|`./ot.py contest fetch <platform> <contest id>`|
| - [ ] 题目获取|`./ot.py problem fetch <platform> <problem id>`|
| - [ ] 平台特殊配置? |`./ot.py browser www.codeforces.com [--rcpc rcpc]`|
| - [ ] 测试当前文件夹代码|`./ot.py test`|
| - [ ] 提交当前文件夹代码|`./ot.py submit`|
