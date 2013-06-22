import time
import socket
import msgpack
import asyncore
import threading
import traceback

from .game import Game
from .match import Match

PROTOCOL_VERSION = 1

class CannotConnect(Exception):
    pass
class ConnectionRefused(Exception):
    pass
class CannotJoinGame(Exception):
    pass
class IncompatibleVersion(Exception):
    pass
class NoDataReceived(Exception):
    pass

_last_uid = 0
_uid_lock = threading.Lock()
def uid():
    global _last_uid, _uid_lock
    with _uid_lock:
        _last_uid += 1
        return _last_uid

class Handler(asyncore.dispatcher):
    def __init__(self, sock=None, ui=None):
        super(Handler, self).__init__(sock)
        self._unpacker = msgpack.Unpacker(use_list=False, encoding='utf8')
        self._ui = ui

    def handle_read(self):
        data = self.recv(4096)
        self._unpacker.feed(data)
        obj = self._unpacker.unpack()
        if obj is None:
            return
        assert isinstance(obj, dict), obj
        assert 'command' in obj, obj
        method = 'on_' + obj['command']
        if hasattr(self, method):
            method = getattr(self, method)
            parsed = method(obj)
            if self._ui is not None:
                getattr(self._ui, method)(obj, parsed)
        else:
            print('Unknown command received: %s' % obj['command'])

    def handle_error(self):
        traceback.print_exc()


def run():
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print('Received Ctrl-C. Exiting.')
        return
