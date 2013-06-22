Introduction
============

Implementation of the game known as 'Ultimate tic-tac-toe'.
Rules :
* English: http://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/
* French: https://progval.net/games/morpion-ultime.html

This implementation features a slightly different version of the game,
disabling won little boards even if they are not full.

Protocol
========

All messages are msgpack-encoding dictionnaries with a 'command' entry.

On connection, client sends a 'handshake' message, and the server replies
with a 'handshake\_reply' message.

Definitions:

* user (or client): someone connected to the server. A user is identified
  with a unique string.
* player: a user who is in a match.
* game: a grid, two players, optional spectators. Moves.
* match: Contains a game. When a game is ended, a new one is created.
  Can be created or joined by a user. Ends when there is no player left.

For the moment, a user may only be in one match per server, but it may
change in a future version of the protocol.

Documentation of each command:

handshake
---------

Should only be sent by the client when connecting.

Keys:
* `version`: The protocol version, as an integer.

handshake\_reply
----------------

Should only be sent by the server, in reply of an `handshake` command.

Keys:
* `accepted`: Whether or not the connection is accepted.
* `error_message`: An error message, if the connection is not accepted.
  Ignored or not given otherwise.
* `version`: Server version.

join\_match
----------

Sent by the client when it wants to join a game.

Keys:
* `match_id`: The ID of the match to join. If not given or None,
  creates a new match.

join\_match\_reply
-----------------

Sent by the server in reply to a `join_match` command.

Keys:
* `accepted`: Whether or not the match request is accepted.
* `error_message`: An error message, if the match request is not accepted.
  Ignored or not given otherwise.
* `match_id`: The ID of the match if it is accepted (Integer).
  Ignored or not given otherwise.
* `users`: List of users in the match (including the recipient), if the
  match request is accepted.

new\_game
---------

Sent by a server when a new game starts.

Keys:
* `match_id`: The ID of the match in which the game takes place.
* `your_char`: Character used by the client receiving this message
  (one-char string if playing, None if spectator).
* `users`: {user: char} mapping.
* `current_player`: Character of the player who is expected to play first.
  (one-char string).
