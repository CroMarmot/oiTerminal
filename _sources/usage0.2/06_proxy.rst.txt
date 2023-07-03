Proxy
=====

this tool use `requests <https://requests.readthedocs.io/>`_ for network request, just config `environment variable <https://requests.readthedocs.io/en/latest/user/advanced/#proxies>`_

Example

.. code-block:: console

  $ export HTTP_PROXY="http://10.10.1.10:3128"
  $ export HTTPS_PROXY="http://10.10.1.10:1080"
  $ export ALL_PROXY="socks5://10.10.1.10:3434"