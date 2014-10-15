import socket
from contextlib import contextmanager

from polon.conf import settings


def repl():
    while 1:
        with socket_connection(settings.STASH_ADDRESS) as s:
            input_stream = raw_input(">> ")
            s.sendall(input_stream)
            print '>> ', repr(s.recv(1024))


class StashClient(object):
    def get(self, key):
        return self.__execute("GET", key=key)

    def put(self, key, value, value_type="STR"):
        return self.__execute("PUT", key=key, value=value, value_type=value_type)

    def __execute(self, method, key, value='', value_type=''):
        with socket_connection(settings.STASH_ADDRESS) as s:
            s.sendall(";".join([method, key, value, value_type]))
            return s.recv(1024)


@contextmanager
def socket_connection(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    yield s
    s.close()


if __name__ == "__main__":
    repl()