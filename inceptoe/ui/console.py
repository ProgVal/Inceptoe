
class ConsoleUi:
    def on_join_match_reply(self, reply, match):
        print('Joined match %s. Users: %s' % (match.match_id, match.users))
