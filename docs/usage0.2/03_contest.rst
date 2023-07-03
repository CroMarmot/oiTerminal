Contest
=======

``oi contest --help`` for more details

.. note:: If you enable auto completion, you can just tap less letter by press more ``Tab``

List
------

Example:

.. code-block:: console

    $ oi contest list Codeforces 
    [INFO]: Checking Log in 
    [INFO]: YeXiaoRain is Logged in Codeforces
                                                   Current or upcoming contests                                                
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
    ┃ Name                               ┃ Start             ┃ Length ┃ Before Start    ┃ Reg                          ┃ Id   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
    │ Codeforces Round 882 (Div. 2)      │ Jul/06/2023 22:35 │ 02:00  │ 3 days, 4:39:11 │ Before registration 28:39:17 │ 1847 │
    │ Codeforces Round 883 (Div. 3)      │ Jul/07/2023 22:35 │ 02:15  │ 4 days, 4:39:11 │ Before registration 28:39:15 │ 1846 │
    │ Codeforces Round (Div. 1 + Div. 2) │ Jul/11/2023 22:35 │ 02:00  │ 8 days, 4:39:11 │ Before registration 04:39:15 │ 1844 │
    └────────────────────────────────────┴───────────────────┴────────┴─────────────────┴──────────────────────────────┴──────┘
                                          History contests (Recent 10)                                      
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━┓
    ┃ Name                                                ┃ Start             ┃ Length ┃ Registered ┃ Id   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━┩
    │ Educational Codeforces Round 151 (Rated for Div. 2) │ Jun/29/2023 22:35 │ 02:00  │ 28370      │ 1845 │
    │ CodeTON Round 5 (Div. 1 + Div. 2, Rated, Prizes!)   │ Jun/24/2023 22:05 │ 03:00  │ 26372      │ 1842 │
    │ Codeforces Round 881 (Div. 3)                       │ Jun/20/2023 22:35 │ 02:15  │ 30978      │ 1843 │
    │ Codeforces Round 880 (Div. 1)                       │ Jun/18/2023 22:35 │ 02:00  │ 1245       │ 1835 │
    │ Codeforces Round 880 (Div. 2)                       │ Jun/18/2023 22:35 │ 02:00  │ 21917      │ 1836 │
    │ Codeforces Round 879 (Div. 2)                       │ Jun/18/2023 16:05 │ 02:00  │ 20335      │ 1834 │
    │ Educational Codeforces Round 150 (Rated for Div. 2) │ Jun/12/2023 22:35 │ 02:00  │ 26443      │ 1841 │
    │ Codeforces Round 878 (Div. 3)                       │ Jun/06/2023 22:35 │ 02:15  │ 31544      │ 1840 │
    │ Codeforces Round 877 (Div. 2)                       │ Jun/04/2023 22:45 │ 02:00  │ 31174      │ 1838 │
    │ Codeforces Round 876 (Div. 2)                       │ Jun/03/2023 22:35 │ 02:00  │ 24780      │ 1839 │
    └─────────────────────────────────────────────────────┴───────────────────┴────────┴────────────┴──────┘


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


Detail
------

Example:

.. code-block:: console

    $ oi contest detail Codeforces 1621
    [INFO]: Checking Log in 
    [INFO]: YeXiaoRain is Logged in Codeforces
                                        Contest /contest/1621                                    
    ┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ ID ┃ Name                             ┃ Time ┃ Memory  ┃ Passed ┃ Url                     ┃
    ┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ A  │ Stable Arrangement of Rooks      │ 1.0s │ 256.0mb │ 22916  │ /contest/1621/problem/A │
    │ B  │ Integers Shop                    │ 2.0s │ 256.0mb │ 12263  │ /contest/1621/problem/B │
    │ C  │ Hidden Permutations              │ 1.0s │ 256.0mb │ 6372   │ /contest/1621/problem/C │
    │ D  │ The Winter Hike                  │ 1.0s │ 256.0mb │ 3729   │ /contest/1621/problem/D │
    │ E  │ New School                       │ 2.0s │ 256.0mb │ 1629   │ /contest/1621/problem/E │
    │ F  │ Strange Instructions             │ 2.0s │ 256.0mb │ 490    │ /contest/1621/problem/F │
    │ G  │ Weighted Increasing Subsequences │ 1.0s │ 256.0mb │ 523    │ /contest/1621/problem/G │
    │ H  │ Trains and Airplanes             │ 4.0s │ 512.0mb │ 135    │ /contest/1621/problem/H │
    │ I  │ Two Sequences                    │ 8.0s │ 256.0mb │ 92     │ /contest/1621/problem/I │
    └────┴──────────────────────────────────┴──────┴─────────┴────────┴─────────────────────────┘
