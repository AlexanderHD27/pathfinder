import threading
import socket
from toolkit.network import basic # pylint: disable=import-error

class Proxy():

    def __init__(self, serverport, serveraddr, clientport, clientaddr):
        threading.Thread.__init__(self)
        self.running = True

        self.serverAddr = (clientaddr, clientport)
        self.clientAddr = (serveraddr, serverport)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverConn = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def handlerServer(self, args, handler):
        try: 
            while self.running:
                data = basic.recvall(self.serverConn)
                data = handler(data)
                self.client.sendall(data)

                if not self.running or data == b"":
                    self.stop()
                    break
                
        except ConnectionAbortedError:
            pass

    def handlerClient(self, _self_, args, handler):
        self = _self_
        try: 
            while self.running:
                data = basic.recvall(self.client)
                data = handler(data)
                self.serverConn.sendall(data)
                
                if not self.running or data == b"":
                    self.stop()
                    break
                

        except ConnectionAbortedError:
            pass

    def stop(self):
        self.running = False
        self.server.close()
        self.client.close()
        self.serverConn.close()

        try: self.clientThread.join()
        except: pass

    def start(self, clientArgs, serverArgs, server2client, client2server):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind(self.serverAddr)
        self.server.listen()
        conn, _ = self.server.accept()
        self.serverConn = conn

        self.client.connect(self.clientAddr)

        self.clientThread = threading.Thread(target=self.handlerClient, args=[self, clientArgs, client2server])
        self.clientThread.start()

        self.handlerServer(serverArgs, server2client)