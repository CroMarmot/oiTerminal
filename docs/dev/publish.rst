=======
Publish
=======


config `~/.pypirc` follow https://packaging.python.org/en/latest/specifications/pypirc/

.. code-block::

  pip install .[dev]
  rm -rf dist/
  python -m build
  twine check dist/*
  # upload to test server
  twine upload --repository testpypi dist/*
  pip install --index-url https://test.pypi.org/simple/ --no-deps yxr-oi-cli==<VERSION>
  ...
  # upload
  twine upload dist/*
  # If you use a mirror of PIP, through designated official pypi to test whether the upload successfully
  pip install --index-url https://pypi.org/simple/ yxr-oi-cli==<VERSION>
