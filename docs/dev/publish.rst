=======
Publish
=======


config `~/.pypirc` follow https://packaging.python.org/en/latest/specifications/pypirc/

.. code-block::

  # update oi_cli2/__init__.py
  pip install .[dev]
  rm -rf dist/
  python -m build
  twine check dist/*
  tar -tvf dist/yxr_oi_cli-*.tar.gz
  # upload to test server
  twine upload --repository testpypi dist/*
  pip install --index-url https://test.pypi.org/simple/ --no-deps yxr-oi-cli==<VERSION>
  ...
  # upload
  twine upload dist/*
  # If you use a mirror of PIP, through designated official pypi to test whether the upload successfully
  pip install --index-url https://pypi.org/simple/ yxr-oi-cli==<VERSION>
