import socket
import msgpack
import asyncore

from . import network
from .game import Game
from .match import Match

class ServerHandler(network.Handler):
    def __init__(self, host, port, ui):
        super(ServerHandler, self).__init__(ui=ui)
        self._server_version = None
        self._match = None
        self._games = []
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.send(msgpack.packb({'command': 'handshake',
            'version': network.PROTOCOL_VERSION}))

    def join_match(self, match_id):
        self.send(msgpack.packb({'command': 'join_match',
            'match_id': match_id}))

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

    def on_new_game(self, obj):
        game = Game.from_dict(obj['game'])
        self._games.append(game)
        return game

class ClientDriver(asyncore.dispatcher):
    def __init__(self, ui):
        super(ClientDriver, self).__init__()
        self._handlers = []
        self._games = {}
        self._ui = ui

    def connect_to_server(self, host, port, ui=None):
        server = ServerHandler(host, port, ui or self._ui)
        self._handlers.append(server)

        return server
