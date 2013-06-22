class Game:
    def __init__(self, current_player, grid=None):
        self.turn = first
        self.grid = grid or map(lambda x:[' ']*9, xrange(0, 9))

    @classmethod
    def from_dict(self, dict_):
        assert isinstance(dict_, dict)
        their_char = dict_['opponent_char']
        my_char = dict_['your_char']
        current_player = dict_['current_player']
        grid = dict_['grid']
        assert isinstance(char, str)
        assert len(char) == 1
        assert isinstance(current_player, str)
        assert len(current_player) == 1
        assert isinstance(grid, tuple)
        assert len(grid) == 9
        assert all(map(lambda l:len(l) == 9, grid))
        line_checker = lambda x:isinstance(x, str) and len(x)==1
        assert all(map(lambda l:all(map(line_checker, l)), grid))
        return Game((my_char, their_char), current_player, grid)
