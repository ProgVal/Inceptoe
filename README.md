Introduction
============

Implementation of the game known as 'Ultimate tic-tac-toe'.
Rules :
* English: http://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/
* French: https://progval.net/games/morpion-ultime.html

This implementation features a slightly different version of the game,
disabling won little boards even if they are not full.

Protocol and reference
======================

cd to the `docs/` folder, run `make html` and open `_build/html/index.html`.

How to play
===========

First, install dependencies. Here is the command for Debian:

```
sudo aptitude install python3.2 git
sudo pip-3.2 install msgpack-python
```

The, download the source code on both computers:

```
https://github.com/ProgVal/Inceptoe.git
cd Inceptoe
```

Finally, the first player starts a game:

```
./inceptoe-client.py progval.net 8520
```

And it will display the command the other player should run to join
your game.
