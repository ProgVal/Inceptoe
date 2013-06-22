#!/usr/bin/env python3

import sys
import inceptoe

def main(host, port):
    print('Running server version %i' % inceptoe.network.PROTOCOL_VERSION)
    server = inceptoe.server.ServerDriver(host, port)
    inceptoe.network.run()

USAGE = 'Usage: server.py <host> <port>'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(USAGE)
        exit()
    (name, host, port) = sys.argv
    if not port.isdigit():
        print(USAGE)
        exit()
    port = int(port)
    main(host, port)
