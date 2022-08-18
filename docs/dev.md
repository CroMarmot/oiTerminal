# Dev

## Create virtual env

```
python3 -m venv venv
```

## Active virtual env

```
. venv/bin/active
```

## Install dependencies

```
pip3 install -r requirements.txt
```

```
pip3 install -e <path to yxr-atcoder-core>
```

## Auto test

```
pytest
```

# Coverage test

```
coverage run -m pytest
```

## Coverage report

```
coverage html
```

## Auto formatting

```
yapf --in-place --recursive oiTerminal tests
```

## Build

```
python -m build
```

## Install at local for debug

```
cd <code folder>
pip3 install -e <当前项目根的路径>
```

## docs

`cd docs && make html`

## 历史代码

orphan from 4376a9dd05fd52ca923c9f79c26c964543409d09

## 开发环境 log

development: `export OITERMINAL_ENV=dev`
