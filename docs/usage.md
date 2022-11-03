# 使用示例

## 初始化

```bash
oi init
```

## 新增用户示例

```bash
oi config account new Codeforces Cro-Marmot
```

## 新增模版示例

新增Codeforces C++20 模版

```bash
oi config template new Codeforces C++20 <模板代码文件路径> "clang++ -o Main Main.cpp -std=gnu++17 -O2 -g -Wall -Wcomma -Wextra -fsanitize=integer,undefined,null,alignment" "./Main" 73
```

**注意** 模板拷贝时会忽略原文件名, 改为 `Main.原后缀`, 因此`编译命令`需要注意

远端`语言id`: https://github.com/CroMarmot/oiTerminal/blob/master/LANG.md

