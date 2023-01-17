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


.. note:: About remote language id: https://github.com/CroMarmot/oiTerminal/blob/master/LANG.md
