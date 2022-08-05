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

