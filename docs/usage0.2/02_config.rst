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

    oi config template new AtCoder "C++17-test" "~/mycode/.oiTerminal/atc_temp.cpp" "clang++ -o Main Main.cpp -std=gnu++17 -O2 -g -Wall -Wcomma -Wextra -fsanitize=integer,undefined,null,alignment" "./Main" 4003
    oi config template new AtCoder "C++17-submit" "~/mycode/.oiTerminal/atc_temp.cpp" "clang++ -o Main Main.cpp -std=gnu++17 -O2 -g -Wall -Wcomma -Wextra" "./Main" 4003


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

    C (GCC 9.2.1)                   4001
    C (Clang 10.0.0)                4002
    C++ (GCC 9.2.1)                 4003
    C++ (Clang 10.0.0)              4004
    Java (OpenJDK 11.0.6)           4005
    Python (3.8.2)                  4006
    Bash (5.0.11)                   4007
    bc (1.07.1)                     4008
    Awk (GNU Awk 4.1.4)             4009
    C# (.NET Core 3.1.201)          4010
    C# (Mono-mcs 6.8.0.105)         4011
    C# (Mono-csc 3.5.0)             4012
    Clojure (1.10.1.536)            4013
    Crystal (0.33.0)                4014
    D (DMD 2.091.0)                 4015
    D (GDC 9.2.1)                   4016
    D (LDC 1.20.1)                  4017
    Dart (2.7.2)                    4018
    dc (1.4.1)                      4019
    Erlang (22.3)                   4020
    Elixir (1.10.2)                 4021
    F# (.NET Core 3.1.201)          4022
    F# (Mono 10.2.3)                4023
    Forth (gforth 0.7.3)            4024
    Fortran (GNU Fortran 9.2.1)     4025
    Go (1.14.1)                     4026
    Haskell (GHC 8.8.3)             4027
    Haxe (4.0.3); js                4028
    Haxe (4.0.3); Java              4029
    JavaScript (Node.js 12.16.1)    4030
    Julia (1.4.0)                   4031
    Kotlin (1.3.71)                 4032
    Lua (Lua 5.3.5)                 4033
    Lua (LuaJIT 2.1.0)              4034
    Dash (0.5.8)                    4035
    Nim (1.0.6)                     4036
    Objective-C (Clang 10.0.0)      4037
    Common Lisp (SBCL 2.0.3)        4038
    OCaml (4.10.0)                  4039
    Octave (5.2.0)                  4040
    Pascal (FPC 3.0.4)              4041
    Perl (5.26.1)                   4042
    Raku (Rakudo 2020.02.1)         4043
    PHP (7.4.4)                     4044
    Prolog (SWI-Prolog 8.0.3)       4045
    PyPy2 (7.3.0)                   4046
    PyPy3 (7.3.0)                   4047
    Racket (7.6)                    4048
    Ruby (2.7.1)                    4049
    Rust (1.42.0)                   4050
    Scala (2.13.1)                  4051
    Java (OpenJDK 1.8.0)            4052
    Scheme (Gauche 0.9.9)           4053
    Standard ML (MLton 20130715)    4054
    Swift (5.2.1)                   4055
    Text (cat 8.28)                 4056
    TypeScript (3.8)                4057
    Visual Basic (.NET Core 3.1.101)4058
    Zsh (5.4.2)                     4059
    COBOL - Fixed (OpenCOBOL 1.1.0) 4060
    COBOL - Free (OpenCOBOL 1.1.0)  4061
    Brainfuck (bf 20041219)         4062
    Ada2012 (GNAT 9.2.1)            4063
    Unlambda (2.0.0)                4064
    Cython (0.29.16)                4065
    Sed (4.4)                       4066
    Vim (8.2.0460)                  4067
