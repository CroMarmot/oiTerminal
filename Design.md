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

### 初始化

`./ot.py init`

创建`.oiTerminal` 文件夹

### 配置

`./ot.py config`

提供 账号管理，本地模板管理，平台管理

#### 账号管理

1. 账号列表
   - 按平台分组
     - 查看现有账号和默认账号
2. 创建新账号
   - 平台选择
   - 用户名密码(AES加密)
3. 编辑账户
   - 选择一个账号对象
     - 修改名称
     - 修改密码
     - 设置默认（对于其所属平台
     - 删除账号

#### 本地模板管理

1. 模板列表
   - 按平台划分
   - 查看模板别名和默认状态
2. 新建模板
   - 平台选择
   - 模板别名
   - 模板路径
   - 编译命令
   - 运行命令
   - 清理编译命令
3. 编辑模板
   - 按平台
   - 修改别名
   - 修改路径
   - 修改执行命令
   - 修改清理命令
   - 设置默认状态
   - 删除

#### 分析管理

1. 查看分析
   - 按平台
   - 列表和默认标识
2. 新建分析
   - 平台
   - 提交语言标识
   - 别名
   - 分析class路径
3. 编辑
   - 修改模板
   - 修改语言
   - 修改路径
   - 设置默认
   - 删除

### 比赛列表

`./ot.py contest Codeforces`

输出开始和即将开始的比赛

输出注册状态（不可注册，可注册，已注册)，开始时间，比赛时长，距今时间，比赛id

### 比赛详情

`./ot.py contestdetail codeforces <contest id>`

example

`./ot.py contestdetail codeforces 1621`

输出比赛题目和提交状态

输出题目状态（用户当前是否通过，通过人次)

### 比赛排名

`./ot.py standing codeforces <contest id>`

example

`./ot.py standing codeforces 1621`

### 题目获取

`./ot.py problem <platform> <problemid>`

example

`./ot.py problem Codeforces 1628A`

生成 `./dist/<platform>/<problempath>/`

包含

```text
<根据默认本地模板的代码文件>
<根据题目分析出的 in/out 文件>
state.json<记录题目状态包括 平台 problemid 本地模板alias 提交语言id>
submit.py<软链提交脚本>
test.py<软链测试脚本>
```

## 生成目录内

### 测试代码

`./test.py`

根据state.json的本地模板，编译运行并使用所有读入读出，产生对比报告。

### 提交代码

`./submit.py`

根据state.json的提交语言，平台提交代码,配置默认账户，登录并获取提交结果。

## 持续

### 测试

`python3 -m pytest`

### 覆盖测试

`coverage run -m pytest`

测试报告

`coverage html`

# 自动补全

https://devmanual.gentoo.org/tasks-reference/completion/index.html

https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion-Builtins.html

https://www.gnu.org/software/bash/manual/html_node/Programmable-Completion.html

# 历史代码

orphan from 4376a9dd05fd52ca923c9f79c26c964543409d09

## log

development: `export OITERMINAL_ENV=dev`
