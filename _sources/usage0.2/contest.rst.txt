Contest
=======

``oi contest --help`` for more details

.. note:: If you enable auto completion, you can just tap less letter by press more ``Tab``

Fetch
------

Example:

.. code-block:: console

    $ oi contest fetch AtCoder abc284
    ┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┓
    ┃ Problem ┃ Fetched ┃ Parse Status ┃
    ┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━┩
    │ A       │ OK      │ OK           │
    │ B       │ OK      │ OK           │
    │ C       │ OK      │ OK           │
    │ D       │ OK      │ OK           │
    │ E       │ OK      │ OK           │
    │ F       │ OK      │ OK           │
    │ G       │ OK      │ OK           │
    │ Ex      │ OK      │ OK           │
    └─────────┴─────────┴──────────────┘
     /home/cromarmot/mycode/dist/AtCoder/abc284

    $ pushd /home/cromarmot/mycode/dist/AtCoder/abc284
    $ ls
    A  B  C  D  E  Ex  F  G
    $ cd A
    $ ls
    in.0  in.1  Main.cpp  out.0  out.1  state.json  TEST

Now you can write code in ``Main.cpp``

Standing
--------

Example:

.. code-block:: console

    $ oi contest standing Codeforces 1721
                      Friends standing https://codeforces.com/contest/1721/standings/friends/true
    ┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┓
    ┃ rank      ┃ who                ┃ score ┃ penalty ┃ hack     ┃ A     ┃ B     ┃ C     ┃ D     ┃ E     ┃ F     ┃
    ┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━┩
    │ 1         │ jiangly            │ 6     │ 99      │          │ +     │ +     │ +     │ +     │ +1    │ +     │
    │           │                    │       │         │          │ 00:01 │ 00:03 │ 00:08 │ 00:12 │ 00:20 │ 00:45 │
    │ 2 (7)     │ SSRS_              │ 6     │ 197     │          │ +     │ +     │ +     │ +2    │ +     │ +1    │
    │           │                    │       │         │          │ 00:02 │ 00:05 │ 00:12 │ 00:35 │ 00:39 │ 01:14 │
    │ 3 (105)   │ Nero               │ 5     │ 182     │          │ +     │ +     │ +     │ +     │ +1    │       │
    │           │                    │       │         │          │ 00:05 │ 00:15 │ 00:27 │ 00:39 │ 01:26 │       │
    │ 4 (247)   │ SSerxhs            │ 5     │ 251     │          │ +     │ +     │ +     │ +2    │ +5    │       │
    │           │                    │       │         │          │ 00:00 │ 00:04 │ 00:33 │ 00:38 │ 01:46 │       │
    │ 5 (269)   │ Cro-Marmot         │ 5     │ 265     │          │ +     │ +1    │ +     │ +     │ +3    │       │
    │           │                    │       │         │          │ 00:21 │ 00:28 │ 00:42 │ 00:54 │ 01:20 │       │
    │ 6 (272)   │ physics0523        │ 5     │ 266     │ +24 : -5 │ +     │ +2    │ +     │ +1    │ +5    │       │
    │           │                    │       │         │          │ 00:03 │ 00:13 │ 00:24 │ 00:44 │ 01:42 │       │
    │ 7 (444)   │ DAWN.              │ 4     │ 107     │          │ +     │ +2    │ +     │ +     │       │       │
    │           │                    │       │         │          │ 00:04 │ 00:11 │ 00:24 │ 00:48 │       │       │
    │ 8 (1404)  │ yiyezhiqiu0305     │ 4     │ 259     │          │ +1    │ +     │ +     │ +8    │       │       │
    │           │                    │       │         │          │ 00:07 │ 00:15 │ 00:37 │ 01:50 │       │       │
    │ 9 (4176)  │ rainboy            │ 3     │ 172     │ -1       │       │       │       │ +2    │ +1    │ +     │
    │           │                    │       │         │          │       │       │       │ 00:59 │ 00:46 │ 00:37 │
    │ 10 (8354) │ themoon            │ 2     │ 100     │          │       │       │       │ +     │ +1    │       │
    │           │                    │       │         │          │       │       │       │ 00:10 │ 01:20 │       │
    │           │ * ftiasch          │ 6     │         │          │ +     │ +     │ +     │ +     │ +     │ +     │
    │           │ * Totoro_          │ 5     │         │          │ +     │ +     │ +     │ +     │ +     │       │
    │           │ * xudian           │ 5     │         │          │ +     │ +     │ +     │ +     │ +5    │       │
    │           │ * dreamoon_love_AA │ 4     │         │          │ +     │ +     │ +     │ +     │       │       │
    │           │ * 0x3F             │ 3     │         │          │ +     │ +     │ +     │       │       │       │
    │           │ * yiyezhiqiu0305   │ 2     │         │          │       │       │       │ +     │ +2    │       │
    │           │ * GStnt            │ 1     │         │          │       │       │       │       │ +     │       │
    │           │ * physics0523      │ 1     │         │          │       │       │       │       │ +     │       │
    │           │ * SSerxhs          │ 1     │         │          │       │       │       │       │       │ +     │
    │           │ * YeXiaoRain       │ 1     │         │          │       │       │       │       │       │ +1    │
    │           │ * Cro-Marmot       │ 1     │         │          │       │       │       │       │ +1    │       │
    │           │ * Nero             │ 1     │         │          │       │       │       │       │       │ +13   │
    └───────────┴────────────────────┴───────┴─────────┴──────────┴───────┴───────┴───────┴───────┴───────┴───────┘
