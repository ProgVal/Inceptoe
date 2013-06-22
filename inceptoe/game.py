class Game:
    def __init__(self, current_player, users, grid=None):
        self.current_player = current_player
        self.users = users
        self.grid = grid or list(map(lambda x:[' ']*9, range(0, 9)))

    @classmethod
    def from_dict(self, dict_):
        assert isinstance(dict_, dict)
        current_player = dict_['current_player']
        users = dict_['users']
        grid = dict_['grid']
        assert isinstance(current_player, str)
        assert len(current_player) == 1
        assert isinstance(users, dict)
        assert len(users) >= 2
        def entry_checker(x):
            return isinstance(x[0], str) and \
                    ((isinstance(x[1], str) and len(x[1]) == 1) or
                     x[1] is None)
        assert all(map(entry_checker, users.items()))
        assert isinstance(grid, tuple)
        assert len(grid) == 9
        assert all(map(lambda l:len(l) == 9, grid))
        line_checker = lambda x:isinstance(x, str) and len(x)==1
        assert all(map(lambda l:all(map(line_checker, l)), grid))
        return Game(current_player, users, grid)

    def to_dict(self):
        return {'current_player': self.current_player, 'users': self.users,
                'grid': self.grid}

    def __repr__(self):
        return ('inceptoe.game.Game(current_player=%s, users=%s, '
               'grid=%s)') % (self.current_player, self.users, self.grid)
