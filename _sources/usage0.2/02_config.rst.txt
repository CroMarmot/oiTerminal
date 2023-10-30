Config
======


User
------

Config user for specific platform, supported CRUD, run ``oi config account --help`` for more details

.. code-block:: bash

    oi config account new <platform> <username>


Example:

.. code-block:: bash

    oi config account new Codeforces Cro-Marmot


Code Template
-------------

Supported CURD, run ``oi config template --help`` for more details

Example:

Add Codeforces(GNU G++20 11.2.0 (64 bit, winlibs)) Local(C++20) template

.. code-block:: bash

    oi config template new Codeforces "C++20" "~/mycode/.oiTerminal/custom_template.cpp" "clang++ -o Main Main.cpp -std=gnu++20 -O2 -g -Wall -Wcomma -Wextra -fsanitize=integer,undefined,null,alignment" "./Main" 73


Add AtCoder(C++ (GCC 9.2.1)) Local(C++17) two different mode

.. code-block:: bash

    oi config template new AtCoder "C++17-test" "~/mycode/.oiTerminal/atc_temp.cpp" "clang++ -o Main Main.cpp -std=gnu++17 -O2 -g -Wall -Wcomma -Wextra -fsanitize=integer,undefined,null,alignment" "./Main" 5001
    oi config template new AtCoder "C++17-submit" "~/mycode/.oiTerminal/atc_temp.cpp" "clang++ -o Main Main.cpp -std=gnu++17 -O2 -g -Wall -Wcomma -Wextra" "./Main" 5001


Remote language id
------------------

.. note:: Not updated in time, run ``oi lang Codeforces``/``oi lang AtCoder`` to query the latest

Codeforces:

.. code-block:: Text

    GNU GCC C11 5.1.0                 43
    Clang++20 Diagnostics             80
    Clang++17 Diagnostics             52
    GNU G++14 6.4.0                   50
    GNU G++17 7.3.0                   54
    GNU G++20 11.2.0 (64 bit, winlibs)73
    Microsoft Visual C++ 2017         59
    GNU G++17 9.2.0 (64 bit, msys 2)  61
    C# 8, .NET Core 3.1               65
    C# 10, .NET SDK 6.0               79
    C# Mono 6.8                       9 
    D DMD32 v2.101.2                  28
    Go 1.19.5                         32
    Haskell GHC 8.10.1                12
    Java 11.0.6                       60
    Java 17 64bit                     74
    Java 1.8.0_241                    36
    Kotlin 1.6.10                     77
    Kotlin 1.7.20                     83
    OCaml 4.02.1                      19
    Delphi 7                          3 
    Free Pascal 3.0.2                 4 
    PascalABC.NET 3.8.3               51
    Perl 5.20.1                       13
    PHP 8.1.7                         6 
    Python 2.7.18                     7 
    Python 3.8.10                     31
    PyPy 2.7.13 (7.3.0)               40
    PyPy 3.6.9 (7.3.0)                41
    PyPy 3.9.10 (7.3.9, 64bit)        70
    Ruby 3.0.0                        67
    Rust 1.66.0 (2021)                75
    Scala 2.12.8                      20
    JavaScript V8 4.8.0               34
    Node.js 12.16.3                   55
    ActiveTcl 8.5                     14
    Io-2008-01-07 (Win32)             15
    Pike 7.8                          17
    Befunge                           18
    OpenCobol 1.0                     22
    Factor                            25
    Secret_171                        26
    Roco                              27
    Ada GNAT 4                        33
    Mysterious Language               38
    FALSE                             39
    Picat 0.9                         44
    GNU C++11 5 ZIP                   45
    Java 8 ZIP                        46
    J                                 47
    Microsoft Q#                      56
    Text                              57
    UnknownX                          62
    Secret 2021                       68

AtCoder:

.. code-block:: Text

    C++ 20 (gcc 12.2)                           5001
    Go (go 1.20.6)                              5002
    C# 11.0 (.NET 7.0.7)                        5003
    Kotlin (Kotlin/JVM 1.8.20)                  5004
    Java (OpenJDK 17)                           5005
    Nim (Nim 1.6.14)                            5006
    V (V 0.4)                                   5007
    Zig (Zig 0.10.1)                            5008
    JavaScript (Node.js 18.16.1)                5009
    JavaScript (Deno 1.35.1)                    5010
    R (GNU R 4.2.1)                             5011
    D (DMD 2.104.0)                             5012
    D (LDC 1.32.2)                              5013
    Swift (swift 5.8.1)                         5014
    Dart (Dart 3.0.5)                           5015
    PHP (php 8.2.8)                             5016
    C (gcc 12.2.0)                              5017
    Ruby (ruby 3.2.2)                           5018
    Crystal (Crystal 1.9.1)                     5019
    Brainfuck (bf 20041219)                     5020
    F# 7.0 (.NET 7.0.7)                         5021
    Julia (Julia 1.9.2)                         5022
    Bash (bash 5.2.2)                           5023
    Text (cat 8.32)                             5024
    Haskell (GHC 9.4.5)                         5025
    Fortran (gfortran 12.2)                     5026
    Lua (LuaJIT 2.1.0-beta3)                    5027
    C++ 23 (gcc 12.2)                           5028
    Common Lisp (SBCL 2.3.6)                    5029
    COBOL (Free) (GnuCOBOL 3.1.2)               5030
    C++ 23 (Clang 16.0.6)                       5031
    Zsh (Zsh 5.9)                               5032
    SageMath (SageMath 9.5)                     5033
    Sed (GNU sed 4.8)                           5034
    bc (bc 1.07.1)                              5035
    dc (dc 1.07.1)                              5036
    Perl (perl  5.34)                           5037
    AWK (GNU Awk 5.0.1)                         5038
    なでしこ (cnako3 3.4.20)                    5039
    Assembly x64 (NASM 2.15.05)                 5040
    Pascal (fpc 3.2.2)                          5041
    C# 11.0 AOT (.NET 7.0.7)                    5042
    Lua (Lua 5.4.6)                             5043
    Prolog (SWI-Prolog 9.0.4)                   5044
    PowerShell (PowerShell 7.3.1)               5045
    Scheme (Gauche 0.9.12)                      5046
    Scala 3.3.0 (Scala Native 0.4.14)           5047
    Visual Basic 16.9 (.NET 7.0.7)              5048
    Forth (gforth 0.7.3)                        5049
    Clojure (babashka 1.3.181)                  5050
    Erlang (Erlang 26.0.2)                      5051
    TypeScript 5.1 (Deno 1.35.1)                5052
    C++ 17 (gcc 12.2)                           5053
    Rust (rustc 1.70.0)                         5054
    Python (CPython 3.11.4)                     5055
    Scala (Dotty 3.3.0)                         5056
    Koka (koka 2.4.0)                           5057
    TypeScript 5.1 (Node.js 18.16.1)            5058
    OCaml (ocamlopt 5.0.0)                      5059
    Raku (Rakudo 2023.06)                       5060
    Vim (vim 9.0.0242)                          5061
    Emacs Lisp (Native Compile) (GNU Emacs 28.2)5062
    Python (Mambaforge / CPython 3.10.10)       5063
    Clojure (clojure 1.11.1)                    5064
    プロデル (mono版プロデル 1.9.1182)          5065
    ECLiPSe (ECLiPSe 7.1_13)                    5066
    Nibbles (literate form) (nibbles 1.01)      5067
    Ada (GNAT 12.2)                             5068
    jq (jq 1.6)                                 5069
    Cyber (Cyber v0.2-Latest)                   5070
    Carp (Carp 0.5.5)                           5071
    C++ 17 (Clang 16.0.6)                       5072
    C++ 20 (Clang 16.0.6)                       5073
    LLVM IR (Clang 16.0.6)                      5074
    Emacs Lisp (Byte Compile) (GNU Emacs 28.2)  5075
    Factor (Factor 0.98)                        5076
    D (GDC 12.2)                                5077
    Python (PyPy 3.10-v7.3.12)                  5078
    Whitespace (whitespacers 1.0.0)             5079
    ><> (fishr 0.1.0)                           5080
    ReasonML (reason 3.9.0)                     5081
    Python (Cython 0.29.34)                     5082
    Octave (GNU Octave 8.2.0)                   5083
    Haxe (JVM) (Haxe 4.3.1)                     5084
    Elixir (Elixir 1.15.2)                      5085
    Mercury (Mercury 22.01.6)                   5086
    Seed7 (Seed7 3.2.1)                         5087
    Emacs Lisp (No Compile) (GNU Emacs 28.2)    5088
    Unison (Unison M5b)                         5089
    COBOL (GnuCOBOL(Fixed) 3.1.2)               5090
