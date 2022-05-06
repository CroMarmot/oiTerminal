Usage
=====

.. _installation:

Installation
------------

To use oiTerminal, first install dependency

Enable virtual environment

.. code-block:: console

   $ python3 -m venv venv
   $ . venv/bin/activate



Install 3rd packages

.. code-block:: console

   (.venv) $ pip3 install -r requirements.txt

Setup auto-completion

.. code-block:: console

   (.venv) $ ./auto-completion/gen-ot-auto-completion.sh
   (.venv) $ source /tmp/ot-auto-completion.sh

Init and config user info

**About Codeforces RCPC**: https://codeforces.com/blog/entry/80135

.. code-block:: console

   (.venv) $ ./ot.py init
   (.venv) $ ./ot.py config

Fetch a problem

.. code-block:: console

   (.venv) $ ./ot.py problem Codeforces 1671A

Test your code

.. code-block:: console

   (.venv) ..../dist/Codeforces/1671/A $ ./test.py

Submit your code

.. code-block:: console

   (.venv) ..../dist/Codeforces/1671/A $ ./submit.py
