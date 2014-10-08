import socket

HOST = 'localhost'
PORT = 50505

while 1:
    input_stream = raw_input(">> ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(input_stream)
    data = s.recv(1024)
    s.close()
    print '>> ', repr(data)