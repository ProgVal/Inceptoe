
class Match:
    def __init__(self, match_id=None, users=None, game=None):
        self.match_id = match_id
        self.users = {} if users is None else users
        self.game = game

    def close(self):
        pass

    def __repr__(self):
        return 'inceptoe.match.Match(match_id=%s, users=%s, game=%s)' % \
                (self.match_id, self.users, self.game)
