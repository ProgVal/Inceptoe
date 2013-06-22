from ..game import Game, InvalidMove

class ConsoleUi:
    def set_handler(self, handler):
        self._handler = handler

    def on_join_match_reply(self, reply, match):
        print('Joined match %s. Users: %s' % (match.match_id, match.users))

    def on_new_game(self, obj, game):
        self._char = obj['your_char']
        self.on_make_move(obj, game)

    def on_make_move(self, obj, game):
        self.print_game(game)
        if game.current_player == self._char:
            while not self.play(game):
                pass
        else:
            print('%s\'s turn.' % game.current_player)

    def print_game(self, game):
        print('   ' + (' '.join(map(str, range(1, 10)))))
        print('  +-----+-----+-----+')
        for (letter, line, level) in zip('ABCDEFGHI', game.grid, [1, 1, 0]*3):
            print(letter + ' |' + ('|'.join(line)) + '|')
            if level == 0:
                print('  +-----+-----+-----+')
            else:
                print('  |-+-+-|-+-+-|-+-+-|')

    def play(self, game):
        move = input('Move? ')
        if len(move) != 2:
            print('Bad input. Should be a letter (line) and a digit(column)')
            return False
        (line, column) = move
        line = ord(line.lower()) - ord('a')
        if not (0 <= line <= 8):
            print('Invalid line.')
            return False
        if not column.isdigit() or not (1 <= int(column) <= 9):
            print('Invalid column.')
            return False
        column = int(column)-1


        try:
            game.make_move(line, column, apply_=False)
        except InvalidMove as e:
            print('Invalid move: %s' % e.args[0])
            return False
        else:
            self._handler.make_move(line, column)
            return True
