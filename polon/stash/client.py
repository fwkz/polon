import socket

HOST = 'localhost'
PORT = 50505


def repl():
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        input_stream = raw_input(">> ")
        s.sendall(input_stream)
        data = s.recv(1024)
        print '>> ', repr(data)
        s.close()


class StashClient(object):
    def get(self, key):
        return self.__execute("GET", key=key)

    def put(self, key, value, value_type="STR"):
        return self.__execute("PUT", key=key, value=value, value_type=value_type)

    def __execute(self, method, key, value='', value_type=''):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(";".join([method, key, value, value_type]))
        data = self.s.recv(1024)
        self.s.close()
        return data

if __name__ == "__main__":
    repl()