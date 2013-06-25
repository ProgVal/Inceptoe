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

First, install dependencies. Here is the command for Debian and Ubuntu:

```
sudo aptitude install git python3 python3-pip
sudo pip-3.2 install msgpack-python
```

(If the second command does not work, replace `pip-3.2` with `pip-3.3`.)

The, download the source code on both computers:

```
git clone https://github.com/ProgVal/Inceptoe.git
cd Inceptoe
```

Finally, the first player starts a game (replace `NICKNAME` with a nickname
you want to use in game):

```
./inceptoe-client.py progval.net 8520 NICKNAME
```

And it will display the command the other player should run to join
your game.
