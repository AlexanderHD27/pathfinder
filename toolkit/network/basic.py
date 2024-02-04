import socket
import threading

def recvall(sock, BUFF_SIZE = 2048):
        data = b""
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data   

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (host, port)

    def recvall(self, BUFF_SIZE = 2048):
        data = b""
        while True:
            part = self.sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data        

    def start(self, handler, args):
        self.sock.connect(self.address)
        handler(self.sock, args)

class Server:

    def __init__(self, host, port):
        self.connections = {}
        self.address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.address)

        self.running = True
        self.conmThreads = []
        self.handlerThread = None

    def handel(self, _self_, handler, args):
        self = _self_

        while self.running:
            self.sock.listen()
            conn, addr = self.sock.accept()
            self.connections.update({addr: conn})
            process = threading.Thread(target=handler, args=[conn, addr, args])
            process.start()
            self.conmThreads.append(process)

    def start(self, handler, args):
        self.handlerThread = threading.Thread(target=self.handel, args=[self, handler, args])
        self.handlerThread.start()

    def stop(self):
        self.running = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        s.close()
        self.handlerThread.join()

    def restart(self, handler, args):
        self.stop()
        self.start(handler, args)

    def recvall(self, sock, BUFF_SIZE = 2048):
        data = b""
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data   