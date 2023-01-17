Doc
======

auto generate from code

.. code-block::

    sphinx-apidoc -f -o docs/ . tests setup.py testlogin.py

This will force overwriting the files list below

.. code-block::

    docs/oi_cli2.rst.
    docs/oi_cli2.abstract.rst.
    docs/oi_cli2.cli.rst.
    docs/oi_cli2.cli.adaptor.rst.
    docs/oi_cli2.core.rst.
    docs/oi_cli2.custom.rst.
    docs/oi_cli2.custom.AtCoder.rst.
    docs/oi_cli2.custom.Codeforces.rst.
    docs/oi_cli2.model.rst.
    docs/oi_cli2.utils.rst.
    docs/oi_cli2.utils.consts.rst.
    docs/modules.rst.

Generate static html doc
------------------------

.. code-block::

    cd docs
    make html

The output file is at ``./docs/_build/html/``

Live doc
--------

.. code-block::

    cd docs
    sphinx-autobuild . ./_build/html/
