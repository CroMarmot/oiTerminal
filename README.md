# oi Termianl

# 初始化环境

`python3 -m venv venv`

# 启用环境

`. venv/bin/activate`

# 安装依赖

`pip3 install -r requirements.txt`

# 测试

`pytest`

# 覆盖测试

`coverage run -m pytest `

测试报告

`coverage html`

# 自动补全

`./auto-completion/gen-ot-auto-completion.sh`

`source /tmp/ot-auto-completion.sh`

# docs

`cd docs && make html`

# 设计

[Design.md](./Design.md)
