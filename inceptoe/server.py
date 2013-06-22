import socket
import msgpack
import asyncore

from . import network

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
        (accepted, error_message, match_id) = self._server.join_match(
                self._addr, self,
                obj['match_id'] if 'match_id' in obj else None)
        self.send(msgpack.packb({'command': 'join_match_reply',
            'accepted': accepted,
            'error_message': error_message,
            'match_id': match_id,
            'users': list(map(str, match.users.keys()))}))

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

    def join_match(self, addr, client, match_id=None):
        if match_id is None:
            match_id = network.uid()
            match = Match()
            self._matches[match_id] = match
            print('User %s created match %i' % (client, match_id))
        elif match_id in self._matches:
            match_id = match_id
            match = self._matches[match_id]
            print('User %s joined match %i' % (client, match_id))
        else:
            return (False, 'This match does not exist.', match_id)
        match.users[addr] = client
        return (True, 'ok', match_id)

    def disconnect(self, client):
        assert client in self._clients
        for (match_id, match) in self._matches.items():
            try:
                match.users.remove(client)
            except KeyError:
                pass
            else:
                if not match.users:
                    print('Match %i closed because %s was the last player in.'%
                            (match_id, client))
                    match.close()
                    del self._matches[match_id]
        del self._clients[client]
