class InvalidMove(Exception):
    pass

def mini_board_coord(line, column):
    return (line // 3, column // 3)
def coord_in_mini_board(line, column):
    return (line % 3, column % 3)

def board_winner(board):
    def valid(char):
        return char not in (None, ' ')
    for l in range(0, 3):
        if valid(board[l][0]) and board[l][0] == board[l][1] == board[l][2]:
            return board[l][0]
    for c in range(0, 3):
        if valid(board[0][c]) and board[0][c] == board[1][c] == board[2][c]:
            return board[0][c]
    if valid(board[1][1]) and (
            board[0][0] == board[1][1] == board[2][2] or
            board[0][2] == board[1][1] == board[2][0]):
        return board[1][1]
    return None


class Game:
    def __init__(self, current_player, users, grid=None, last_move=None):
        self.current_player = current_player
        self.users = users
        self.grid = grid or list(map(lambda x:[' ']*9, range(0, 9)))
        self.last_move = None

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
        assert isinstance(grid, list)
        assert len(grid) == 9
        assert all(map(lambda l:len(l) == 9, grid))
        line_checker = lambda x:isinstance(x, str) and len(x)==1
        assert all(map(lambda l:all(map(line_checker, l)), grid))
        return Game(current_player, users, grid)

    def to_dict(self):
        return {'current_player': self.current_player, 'users': self.users,
                'grid': self.grid, 'last_move': self.last_move}

    def __repr__(self):
        return ('inceptoe.game.Game(current_player=%s, users=%s, '
               'grid=%s, last_move=%s)') % \
                (self.current_player, self.users, self.grid, self.last_move)

    def make_move(self, line, column, apply_=True):
        if self.last_move is not None:
            if self.grid[line][column] != ' ':
                raise InvalidMove('This cell has already been played.')
            (last_char, last_line, last_column) = self.last_move
            expected_mini_board = coord_in_mini_board(last_line, last_column)
            played_mini_board = mini_board_coord(line, column)
            if expected_mini_board != played_mini_board and \
                    self.mini_board_winner(*expected_mini_board) is None:
                raise InvalidMove('Wrong mini board.')
            if self.mini_board_winner(*played_mini_board) is not None:
                raise InvalidMove('This mini board has already be won.')
        if apply_:
            self.grid[line][column] = self.current_player
            self.last_move = (self.current_player, line, column)
            self.current_player = self.select_next_player()

    def select_next_player(self):
        def f(c):
            return c and c != self.current_player and c != ' '
        return list(filter(f, self.users.values()))[0]

    def mini_board_winner(self, line, column):
        g = self.grid
        l = line
        c = column
        return board_winner([
            g[l*3][c*3:c*3+3],
            g[l*3+1][c*3:c*3+3],
            g[l*3+2][c*3:c*3+3],
            ])
    def board_winner(self):
        g = self.grid
        w = board_winner
        return w([[
                    w([g[0][0:3], g[1][0:3], g[2][0:3]]),
                    w([g[0][3:6], g[1][3:6], g[2][3:6]]),
                    w([g[0][6:9], g[1][6:9], g[2][6:9]]),
                ],
                [
                    w([g[3][0:3], g[4][0:3], g[5][0:3]]),
                    w([g[3][3:6], g[4][3:6], g[5][3:6]]),
                    w([g[3][6:9], g[4][6:9], g[5][6:9]]),
                ],
                [
                    w([g[6][0:3], g[7][0:3], g[8][0:3]]),
                    w([g[6][3:6], g[7][3:6], g[8][3:6]]),
                    w([g[6][6:9], g[7][6:9], g[8][6:9]]),
                ],
                ])

