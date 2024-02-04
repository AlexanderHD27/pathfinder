# Imports
from sys import path as sysPath
from os import getcwd
sysPath.append(getcwd())

import time
import threading
import socket
import sys
import src

# Socket Connection class for the Monitor Program
class ServerCon(threading.Thread):

    def __init__(self, _address_, _port_, _name_, _updater_):

        threading.Thread.__init__(self) # Inits Thread
        self.HOST = _address_
        self.PORT = _port_
        self.name = _name_
        self.updater = _updater_
        self.sock = socket.socket(src.connectionFamily, socket.SOCK_STREAM) # Creates socket object
        self.display = None

    def run(self): # The Multithreaded Method

        if not src.enableBluetooth:
            self.Proxy = Proxy(self.display, self.name + "proxy")
            self.Proxy.display = self.display
            self.Proxy.start()

        while self.display.running:
            conn = None

            try: # Setting Up Conncetions
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating Socket Object
                self.display.log("Creating a {} {} socket...".format(self.sock.type.name, self.sock.family.name), src.DEBUG, self.name)
                self.display.log("Binding socket to {} at port {}...".format(self.HOST, self.PORT), src.DEBUG, self.name)
                self.sock.bind((self.HOST, self.PORT)) # Binding it to port and address

                self.display.log("Wating for Connections as {} on port {}...".format(self.HOST, self.PORT), src.DEBUG, self.name)
                self.sock.listen(30) # Wating for Connections
                conn, addr = self.sock.accept() # Accepting on Connection
                self.display.log("", src.DEBUG, self.name)
                self.display.log("Connected to {} on port {}!".format(addr[0], addr[1]), src.NOTIFY, self.name)
                self.display.log("", src.DEBUG, self.name)

                # Messuring Latency
                self.display.log("Messuring latency...", src.DEBUG, self.name)
                latency = time.time()
                conn.sendall(b"ECHO ECHO ECHO")
                conn.recv(2048)
                latency = time.time() - latency
                self.display.log("This Connection has a latency of {}s while sending {} bytes!".format(round(latency, 5), sys.getsizeof(b"ECHO")), src.DEBUG, self.name)

            except Exception as E:
                self.display.log("While connecting a Exception accured:", src.ERROR, self.name)
                self.display.log(E, src.ERROR)
                time.sleep(0.5)
                continue

            timestamp = time.time() 
            self.updater(self, conn, timestamp)
            
            try: # Closing Conncetion
                conn.close() 
                self.display.log("", src.DEBUG)
                self.display.log("Closed Connection to {} on port {} after {}s !".format(addr[0], addr[1], round(time.time()-timestamp, 4)), src.NOTIFY, self.name)
                self.display.log("", src.DEBUG)

            except Exception as E:
                self.display.log("While closing the Connection a Exception accured:", src.ERROR, self.name)
                self.display.log(E, src.ERROR)

class ClientCon(threading.Thread):
    
    def __init__(self, _address_, _port_, _robot_, _updater_):
        threading.Thread.__init__(self)
        self.address = _address_  
        self.port = _port_ 
        self.robot = _robot_
        self.updater = _updater_
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def run(self):
        self.sock.connect((self.address, self.port))
        self.sock.sendall(self.sock.recv(2084))
        self.updater(self)
        self.sock.close()

class Proxy(threading.Thread):

    def __init__(self, _display_, _name_):
        threading.Thread.__init__(self)

        self.display = _display_

    def run(self):
        while self.display.running:
            break