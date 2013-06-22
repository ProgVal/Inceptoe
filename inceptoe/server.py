import socket
import msgpack
import asyncore

from . import network
from .game import Game
from .match import Match

class ClientHandler(network.Handler):
    def __init__(self, sock, addr, server):
        super(ClientHandler, self).__init__(sock)
        print('Client connecting from %s.' % (addr,))
        self._addr = addr
        self._server = server

    def on_handshake(self, handshake):
        assert 'version' in handshake, handshake
        version = handshake['version']
        assert isinstance(version, int)
        version_ok = (network.PROTOCOL_VERSION == version)
        self.send(msgpack.packb({'command': 'handshake_reply',
            'accepted': version_ok,
            'version': network.PROTOCOL_VERSION}))
        if not version_ok:
            print('%s has version %i, aborting.' % (addr, version))
            return
        print('%s has version %i.' % (self._addr, version))

    def on_join_match(self, obj):
        match_id = obj['match_id'] if 'match_id' in obj else None
        if match_id is None:
            match_id = network.uid()
            match = Match()
            self._server._matches[match_id] = match
            print('User %s created match %s' % (self._addr, match_id))
        elif match_id in self._server._matches:
            match_id = match_id
            match = self._server._matches[match_id]
            print('User %s joined match %s' % (self._addr, match_id))
        else:
            self.send(msgpack.packb({'command': 'join_match_reply',
                'accepted': False,
                'error_message': 'This match (%r) does not exist.' % match_id
                }))
            return
        match.users[self._addr] = self
        self.send(msgpack.packb({'command': 'join_match_reply',
            'accepted': True,
            'match_id': match_id,
            'users': list(map(str, match.users.keys()))}))

        if len(match.users) == 2:
            assert match.game is None, match
            users = dict(zip(map(str, match.users), ['X', 'O'] +
                    list(map(lambda x:None, range(2, len(match.users))))))
            game = Game('X', users)
            for (addr, handler) in match.users.items():
                handler.send(msgpack.packb({'command': 'new_game',
                    'match_id': match_id,
                    'your_char': users[str(addr)],
                    'game': game.to_dict()}))

        return match

    def handle_close(self):
        if not self.connected: # This method is actually called twice
            return
        print('Client %s closed the connection.' % (self._addr,))
        self._server.disconnect(self._addr)
        self.close()

    
class ServerDriver(asyncore.dispatcher):
    def __init__(self, host, port):
        super(ServerDriver, self).__init__()
        self._clients = {}
        self._matches = {}
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        (sock, addr) = self.accept()
        self._clients[addr] = ClientHandler(sock, addr, self)

    def disconnect(self, client):
        assert client in self._clients
        for (match_id, match) in list(self._matches.items()):
            try:
                del match.users[client]
            except KeyError:
                pass
            else:
                if not match.users:
                    print('Match %s closed because %s was the last player in.'%
                            (match_id, client))
                    match.close()
                    del self._matches[match_id]
        del self._clients[client]
