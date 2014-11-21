"""NoSQL database written in Python.

Super simple key-value store written by Jeff Knupp. For more info visit:
http://jeffknupp.com/blog/2014/09/01/what-is-a-nosql-database-learn-by-writing-one-in-python/
"""
import socket
import pickle

from command_handlers import *
from polon.conf import settings


COMMAND_HANDLERS = {
    'PUT': handle_put,
    'GET': handle_get,
    'INCREMENT': handle_increment,
    'APPEND': handle_append,
    'DELETE': handle_delete,
    'STATS': handle_stats,
}


def main():
    """Main entry point for script."""
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SOCKET.bind(settings.STASH_ADDRESS)
    SOCKET.listen(1)

    while 1:
        connection, address = SOCKET.accept()
        command, key, value = pickle.loads(connection.recv(4096).decode())

        if command == 'STATS':
            response = handle_stats()
        elif command in ('GET', 'INCREMENT', 'DELETE'):
            response = COMMAND_HANDLERS[command](key)
        elif command in ('PUT', 'APPEND'):
            response = COMMAND_HANDLERS[command](key, value)
        else:
            response = (False, 'Unknown command type [{}]'.format(command))

        update_stats(command, response[0])
        connection.sendall(pickle.dumps(response))
        connection.close()

    SOCKET.shutdown(socket.SHUT_RDWR)
    SOCKET.close()

if __name__ == '__main__':
    main()