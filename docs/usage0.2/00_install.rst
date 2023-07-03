Install
=======

.. _installation:

Install From Pypi
-----------------

.. code-block:: console

    $ pip3 install yxr-oi-cli

Install From Github
-------------------

.. code-block:: console

    $ git clone https://github.com/CroMarmot/oiTerminal -b He
    $ cd oiTerminal
    $ pip3 install -e .

Enable tab auto completion
--------------------------

.. code-block:: bash

    _oi_completions()
    {
      keys=$(/usr/bin/env oi completion ${COMP_WORDS[@]:0:$COMP_CWORD})
      COMPREPLY=($(compgen -W "$keys" "${COMP_WORDS[$COMP_CWORD]}"))
    }
    complete -F _oi_completions oi

You can add this in ``~/.bashrc`` for better experience
