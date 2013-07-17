import unittest

from inceptoe import server, network

class TestClientHandler(server.ClientHandler):
    def __init__(self, addr, server):
        self._objects = []
        super(TestClientHandler, self).__init__(None, addr, server)
    def send(self, obj):
        self._objects.append(obj)

class TestServerDriver(server.ServerDriver):
    def _setup_network(self):
        pass
    def spawn_client(self):
        addr = ('127.0.0.1', int(network.uid()))
        client = TestClientHandler(addr, self)
        self._clients[str(addr)] = client
        return client

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = TestServerDriver()
    def get_replies(self, method, obj):
        method.__self__._objects = []
        method(obj)
        return self.get_objects(method.__self__)
    def get_objects(self, handler):
        (objects, handler._objects) = (handler._objects, [])
        return objects

    def classic_initialization(self):
        # foo is connecting
        u_foo = self.server.spawn_client()
        replies = self.get_replies(u_foo.on_handshake,
            {'version': network.PROTOCOL_VERSION, 'nickname': 'foo'})
        self.assertEqual(replies,
            [{'command': 'handshake_reply', 'accepted': True,
                'version': network.PROTOCOL_VERSION}])
        replies = self.get_replies(u_foo.on_join_match,
            {'match_id': 'my_match'})
        self.assertEqual(len(replies), 1, replies)
        self.assertEqual(replies[0],
            {'command': 'join_match_reply', 'accepted': True,
                'match_id': 'my_match', 'users': ['foo']})

        # bar is connecting
        u_bar = self.server.spawn_client()
        replies = self.get_replies(u_bar.on_handshake,
            {'version': network.PROTOCOL_VERSION, 'nickname': 'bar'})
        self.assertEqual(replies,
            [{'command': 'handshake_reply', 'accepted': True,
                'version': network.PROTOCOL_VERSION}])
        replies = self.get_replies(u_bar.on_join_match,
            {'match_id': 'my_match'})
        self.assertEqual(len(replies), 2, replies)
        self.assertEqual(replies[0],
            {'command': 'join_match_reply', 'accepted': True,
                'match_id': 'my_match', 'users': ['bar', 'foo']})

        replies2 = self.get_objects(u_foo)
        self.assertEqual(len(replies2), 2, replies2)
        self.assertEqual(replies2[0],
            {'command': 'user_joined_match', 'user': 'bar',
                'match_id': 'my_match'})
        self.assertEqual(replies[1]['command'], 'new_game')
        self.assertEqual(replies2[1]['command'], 'new_game')
        self.assertEqual(replies[1]['match_id'], 'my_match')
        self.assertEqual(replies2[1]['match_id'], 'my_match')
        self.assertEqual(replies[1]['game'], replies2[1]['game'])
        self.assertEqual(
                set((replies[1]['your_char'], replies2[1]['your_char'])),
                set(('X', 'O')))

        if replies[1]['your_char'] == 'X':
            (u_X, u_O) = (u_bar, u_foo)
        else:
            (u_X, u_O) = (u_foo, u_bar)
        return (u_X, u_O)

    def testTrivial(self):
        (u_X, u_O) = self.classic_initialization()
        replies = self.get_replies(u_X.on_make_move,
            {'line': 3, 'column': 3, 'match_id': 'my_match'})
        self.assertEqual(replies[0], {'command': 'make_move',
            'match_id': 'my_match', 'line': 3, 'column': 3})

    def testForbiddenPlay(self):
        (u_X, u_O) = self.classic_initialization()
        self.assertEqual(self.get_replies(u_O.on_make_move,
            {'line': 3, 'column': 3, 'match_id': 'my_match'})[0]['command'],
            'error')

    def testSpectator(self):
        (u_X, u_O) = self.classic_initialization()
        u_X.on_make_move({'line': 3, 'column': 3, 'match_id': 'my_match'})

        u_spec = self.server.spawn_client()
        replies = self.get_replies(u_spec.on_handshake,
            {'version': network.PROTOCOL_VERSION, 'nickname': 'baz'})
        self.assertEqual(replies,
            [{'command': 'handshake_reply', 'accepted': True,
                'version': network.PROTOCOL_VERSION}])
        replies = self.get_replies(u_spec.on_join_match,
            {'match_id': 'my_match'})
        self.assertEqual(len(replies), 2, replies)
        self.assertEqual(replies[0],
            {'command': 'join_match_reply', 'accepted': True,
                'match_id': 'my_match', 'users': ['bar', 'baz', 'foo']})
        self.assertEqual(replies[1]['command'], 'new_game')
        self.assertEqual(replies[1]['match_id'], 'my_match')
        self.assertEqual(replies[1]['game']['grid'][3][3], 'X')
        self.assertEqual(replies[1]['your_char'], None)
