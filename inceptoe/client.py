import socket
import msgpack
import asyncore

from . import network
from .game import Game
from .match import Match

class ServerHandler(network.Handler):
    """Handles connection to a server."""
    def __init__(self, host, port, ui):
        super(ServerHandler, self).__init__(ui=ui)
        self._server_version = None
        self._match = None
        self._games = {}
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.send(msgpack.packb({'command': 'handshake',
            'version': network.PROTOCOL_VERSION}))

    def join_match(self, match_id):
        self.send(msgpack.packb({'command': 'join_match',
            'match_id': match_id}))

    def make_move(self, line, column):
        self.send(msgpack.packb({'command': 'make_move',
            'match_id': self._match.match_id,
            'line': line,
            'column': column}))

    def on_handshake_reply(self, handshake):
        assert isinstance(handshake['accepted'], bool)
        assert self._server_version is None
        self._server_version = handshake['version']
        if not handshake['accepted']:
            raise ConnectionRefused(handshake['error_message'])
        print('Server has version %i: ok.' % handshake['version'])

    def on_join_match_reply(self, reply):
        assert isinstance(reply['accepted'], bool)
        if not reply['accepted']:
            assert isinstance(reply['error_message'], str)
            raise network.CannotJoinGame(reply['error_message'])
        assert self._match is None
        self._match = Match(reply['match_id'], reply['users'])
        return self._match

    def on_user_joined_match(self, obj):
        print('User %s joined match %s' % (obj['user'], obj['match_id']))

    def on_new_game(self, obj):
        game = Game.from_dict(obj['game'])
        self._games[obj['match_id']] = game
        return game

    def on_make_move(self, obj):
        assert isinstance(obj['match_id'], str)
        line = obj['line']
        column = obj['column']
        assert isinstance(line, int)
        assert isinstance(column, int)
        assert 0 <= line <= 8
        assert 0 <= column <= 8
        game = self._games[obj['match_id']]
        game.make_move(obj['line'], obj['column'])
        return game

    def on_message(self, obj):
        assert isinstance(obj['match_id'], str)
        assert isinstance(obj['from'], str)
        assert isinstance(obj['message'], str)
        return (obj['match_id'], obj['from'], obj['message'])

    def send_message(self, message):
        self.send(msgpack.packb({'command': 'message',
            'match_id': self._match.match_id,
            'message': message}))

    def handle_close(self):
        super(ServerHandler, self).handle_close()
        if self._ui and hasattr(self._ui, 'handle_connection_closed'):
            self._ui.handle_connection_closed()

class ClientDriver(asyncore.dispatcher_with_send):
    def __init__(self, ui):
        super(ClientDriver, self).__init__()
        self._handlers = []
        self._games = {}
        self._ui = ui

    def connect_to_server(self, host, port, ui=None):
        server = ServerHandler(host, port, ui or self._ui)
        self._handlers.append(server)

        return server
