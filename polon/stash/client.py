import socket
import pickle
from contextlib import contextmanager

from polon.conf import settings


class StashClient(object):
    def get(self, key):
        return self.__execute("GET", key=key)

    def put(self, key, value):
        return self.__execute("PUT", key=key, value=value)

    def __execute(self, method, key, value=None):
        with socket_connection(settings.STASH_ADDRESS) as s:
            s.sendall(pickle.dumps((method, key, value)))
            return pickle.loads(s.recv(1024))


@contextmanager
def socket_connection(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    yield s
    s.close()


if __name__ == "__main__":
    stash = StashClient()
    print stash.put('kapucyn', ["lista", "kapucynow"])
    print stash.get("kapucyn")[1]