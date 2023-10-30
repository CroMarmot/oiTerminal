FAQ
===

No successful submit
--------------------

[TODO add auto checker]

What happens: 

``oi submit`` command shows ``submitted`` but not really submitted

.. code-block::
  
    [YYYY-MM-DD HH:mm:SS,894 oiTerminal ERROR submit.py async_watch_result 57]: 
    Traceback (most recent call last):
      File ".../oi_cli2/cli/submit.py", line 53, in async_watch_result
        async for result in oj.async_get_result_yield(problem_url, time_gap=FETCH_RESULT_INTERVAL):
      File ".../oi_cli2/cli/adaptor/AtCoderAdaptor.py", line 144, in async_get_result_yield
        res = transform_Result(fetch_result(self.http_util, problem_url))
      File ".../yxr-atcoder-core/ac_core/result.py", line 165, in fetch_result
        json_url = _parse_json_url(resp.text)
      File ".../yxr-atcoder-core/ac_core/result.py", line 135, in _parse_json_url
        assert r is not None  # no submission
    AssertionError


Possible solution:

the platform's ``language id`` might change

.. code-block:: bash
    
    # check with command 
    oi lang AtCoder
    oi lang Codeforces
    oi config template list --detail
    # modify with
    oi config template modify AtCoder <your template name> --langid <new language id>
    # example
    oi config template modify AtCoder C++17-test --langid 5001
    # check `up_lang` in your `state.json in` code folder like `/dist/AtCoder/abc309/Ex/state.json`
    # [TODO remove `up_lang` field from `state.json`]
    sed -i 's/4003/5001/g' state.json