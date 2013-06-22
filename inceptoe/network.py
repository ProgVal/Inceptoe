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
    """Return an unique ID (obtained with thread-safe incrementation)."""
    global _last_uid, _uid_lock
    with _uid_lock:
        _last_uid += 1
        return str(_last_uid)

class Handler(asyncore.dispatcher):
    """Abstract class for managing a connection an events."""
    def __init__(self, sock=None, ui=None):
        super(Handler, self).__init__(sock)
        self._unpacker = msgpack.Unpacker(use_list=True, encoding='utf8')
        self._ui = ui
        if ui is not None:
            ui.set_handler(self)

    def readable(self):
        time.sleep(0.1)
        return True

    def writeable(self):
        return True

    def handle_read(self):
        data = self.recv(4096)
        self._unpacker.feed(data)
        while self._read_object():
            pass

    def _read_object(self):
        """Read an object and dispatch it according to the `command` entry."""
        try:
            obj = self._unpacker.unpack()
        except msgpack.exceptions.OutOfData:
            return False
        if obj is None:
            return False
        assert isinstance(obj, dict), obj
        assert 'command' in obj, obj
        method_name = 'on_' + obj['command']
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            parsed = method(obj)
            if self._ui is not None and hasattr(self._ui, method_name):
                getattr(self._ui, method_name)(obj, parsed)
        else:
            print('Unknown command received: %s' % obj['command'])
        return True

    def handle_error(self):
        traceback.print_exc()


def run():
    """Run the network drivers."""
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print('Received Ctrl-C. Exiting.')
        return
