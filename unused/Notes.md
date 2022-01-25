# docker

`docker run -it debian`

# 或

`docer start -i <container_name>`

```
apt update && apt install python3 python3-venv
```

文件传输

```
docker cp <from> <to>
docker cp /tmp/outFile <container hash>:/path/to/
```

# venv 

python >= 3.4

```
# 使用venv创建env文件夹
python3 -m venv venv
# 启用环境(linux)
source env/bin/activate
```

# install dep

```
pip install -r requirements.txt
```

# setup.py

`pip install -U setuptools`

`setup.py`

```python
from setuptools import setup, find_packages
setup(
    name = "demo",
    version = "0.1",
    packages = find_packages(),
)
```

执行`python3 setup.py bdist_egg`即可打包一个test的包了。`dist`中生成的是egg包

执行`python3 setup.py install --user` 安装包，在`~/.local/lib/python3.8/site-packages`文件夹下

# Others

标准库 https://docs.python.org/zh-cn/3/library/index.html

setup.py: distutils (1998) -> setuptools(2004) ,wheel(PEP427), https://docs.python.org/zh-cn/3/distutils/setupscript.html#

进阶技巧 https://docs.pythontab.com/interpy/

打包上pip https://packaging.python.org/tutorials/packaging-projects/

argparse https://docs.python.org/zh-cn/3/howto/argparse.html#getting-a-little-more-advanced

async/await https://docs.python.org/zh-cn/3/reference/compound_stmts.html#coroutines


