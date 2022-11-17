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

### Enable tab auto completion

```bash
./auto-completion/gen-ot-auto-completion.sh
source /tmp/ot-auto-completion.sh
```

## 手动配置CF RCPC

手动添加`.oiTerminal/CF_RCPC`, 内容为浏览器中`cookie`的`RCPC`字段

```text
xxxxxxxxxxxxxxxxxxxxxxxx
```

## oi Cheeat Sheat

|Feature|Command|
|---|---|
|initial create `.oiTerminal`folder|`oi init`|
| 新增用户|`oi config account new <platform> <account> [--default]`|
| 查看用户|`oi config account list` |
| 更改用户|`oi config account modify <platform> <account> [--pass] [--default]`|
| 删除用户|`oi config account delete <platform> <account>`|
| 新增模板|`oi config template new <platform> <name>  <path> <compile command> <execute command> <submit lang id> [--default]`|
| 查看模板|`oi config template list`|
| 更新模板|`oi config template modify <platform> <name> [--path <path>] [--compile <compile command>] [--execute <execute command>] [--submitlangid <submit lang id>] [--default]`|
| 删除模板|`oi config template delete <platform> <alias>`|
| 比赛列表|`oi contest list <platform>`|
| 比赛详情|`oi contest detail <platform> <contest id>`|
| 比赛排名|`oi contest standing <platform> <contest id>`|
| 拉取比赛|`oi contest fetch <platform> <contest id>`|
| 测试当前文件夹代码|`oi test`|
| 提交当前文件夹代码|`oi submit`|


