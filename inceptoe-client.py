#!/usr/bin/env python3

import sys
import inceptoe

def main(host, port, nick, match_id=None):
    print('Running client version %i' % inceptoe.network.PROTOCOL_VERSION)
    ui = inceptoe.ui.ConsoleUi()
    client = inceptoe.client.ClientDriver(ui)
    server = client.connect_to_server(host, port, nick)
    server.join_match(match_id)
    inceptoe.network.run()

USAGE = 'Usage: client.py <host> <port> <nickname> [<match id>]'

if __name__ == '__main__':
    if len(sys.argv) == 4:
        (name, host, port, nick) = sys.argv
        match_id = None
    elif len(sys.argv) == 5:
        (name, host, port, nick, match_id) = sys.argv
    else:
        print(USAGE)
        exit()
    if not port.isdigit():
        print(USAGE)
        exit()
    port = int(port)
    main(host, port, nick, match_id)
