#!/usr/bin/python3
# Imports
import pygame
import json
import os, sys, time

import src
import traceback
import networking.Core


class Display: # Window Class

    def __init__(self, _cmdConn_, _dataConn_):

        pygame.init() # Initing Pygamel
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 30) # Set Window Spawnpoint

        #Setup Pygame
        pygame.display.set_caption("Monitor")
        pygame.display.set_icon(pygame.image.load("src/Python.png"))

        # Connection Object
        self.cmdConn = _cmdConn_
        self.dataConn = _dataConn_

        # Console Variables
        self.consoleView = 36
        self.consoleMaxChar = 75
        self.consoleDataBuffer = []
        self.consoleData = []
        self.consolePause = False

        # Map Variables
        self.mapData = []

        for x in range(58):
            self.mapData.append([])
            for y in range(58):
                self.mapData[x].append(-1)

        # Sensor Variables
        self.colorSensor = (0, 0, 0)
        self.infraSensor = 0
        self.stoped = False
        self.values = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.pos = [29, 29]

        # Window Variables
        self.running = True
        self.mainSurface = pygame.display.set_mode((1500, 740), 0, 32)
        self.consoleFont = pygame.font.SysFont("Consolas", 20)
        self.clock = pygame.time.Clock()
        
    def log(self, msg, level=src.DEBUG, name=-1): # Log to Console Function
        if not self.consolePause:
            if name != -1:
                self.consoleData.append([msg, src.loggingLevels.get(level), name])
            else:
                self.consoleData.append([msg, src.loggingLevels.get(level)])
        else:
            if name != -1:
                self.consoleDataBuffer.append([msg, src.loggingLevels.get(level), name])
            else:
                self.consoleDataBuffer.append([msg, src.loggingLevels.get(level)])
    
    def update(self): # Updates Window
        # Console Updates
        pos = 0
        if len(self.consoleData) <= self.consoleView:
            for i in range(len(self.consoleData)):
        
                if len(self.consoleData[i]) == 2:
                    text = self.consoleFont.render(str(self.consoleData[i][0])[:self.consoleMaxChar], True, self.consoleData[i][1])
                elif len(self.consoleData[i]) == 3:
                    text = self.consoleFont.render("[{}] ".format(str(self.consoleData[i][2])[:5]) + str(self.consoleData[i][0])[:self.consoleMaxChar-8], True, self.consoleData[i][1])
                
                if len(self.consoleData[i]) == 2 or  len(self.consoleData[i]) == 3:
                    self.mainSurface.blit(text, (10, pos*20 + 10))
                pos += 1
        else:
            for i in range(len(self.consoleData)-self.consoleView, len(self.consoleData)):
                                
                if len(self.consoleData[i]) == 2:
                    text = self.consoleFont.render(str(self.consoleData[i][0])[:self.consoleMaxChar], True, self.consoleData[i][1])
                elif len(self.consoleData[i]) == 3:
                    text = self.consoleFont.render("[{}] ".format(str(self.consoleData[i][2])[:5]) + str(self.consoleData[i][0])[:self.consoleMaxChar-8], True, self.consoleData[i][1])
                
                if len(self.consoleData[i]) == 2 or  len(self.consoleData[i]) == 3:
                    self.mainSurface.blit(text, (10, pos*20 + 10))
                
                pos += 1
 
        # Boarders
        pygame.draw.rect(self.mainSurface, (255, 255, 255), (840, 5, 3, 730))
        pygame.draw.rect(self.mainSurface, (255, 255, 255), (840, 85, 655, 3))
        pygame.draw.rect(self.mainSurface, (255, 255, 255), (925, 5, 3, 81))
        pygame.draw.rect(self.mainSurface, (255, 255, 255), (1010, 5, 3, 81))

        # Map 
        for x in range(len(self.mapData)):
            for y in range(len(self.mapData[x])):
                pygame.draw.rect(self.mainSurface, src.mapColor.get(self.mapData[x][y]), (x*11 + 852, y*11 + 95, 10, 10))

        # Sensor Values
        pygame.draw.rect(self.mainSurface, self.colorSensor, (850, 5, 70, 75))
        pygame.draw.rect(self.mainSurface, (255-self.infraSensor, 255-self.infraSensor, 255-self.infraSensor), (934, 5, 70, 75))

    def mainloop(self): # Mainloop function

        if not src.enableBluetooth:
            self.log("No Bluethoot Connector isn't available! Will use USB Connector!", src.ERROR)
        
        self.cmdConn.start() # Start Cmd Connection Thread
        self.dataConn.start() # Start Data Connection Thread
        
        while self.running: # Main Loop
            
            self.mainSurface.fill((0, 0, 0)) # Reset Window

            for event in pygame.event.get(): # Event Handler
                if event.type == pygame.QUIT:
                    self.cmdConn.sock.close()
                    self.dataConn.sock.close()
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAUSE: # Console pause on
                        self.consolePause = True
                        self.consoleDataBuffer = self.consoleData

                    elif event.key == pygame.K_RETURN: # Console pause off
                        self.consoleData = self.consoleDataBuffer
                        self.consolePause = False

                    elif event.key == pygame.K_ESCAPE:
                        self.cmdConn.sock.close()
                        self.dataConn.sock.close()
                        self.running = False
 
            self.update() # Update Window
            pygame.display.flip()
            self.clock.tick(60) # Clock

        self.cmdConn.sock.close() # Killing Cmd Socket
        self.dataConn.sock.close() # Killing Data Socket
        self.cmdConn.join(1) # Joining Cmd Connection Thread
        self.dataConn.join(1) # Joining Data Connection Thread
        pygame.quit() # Quiting Pygame

def cmdUpdater(self, conn, timestamp):
    try: # Reciving Data
        while True:     
            dataList = [] # Creating Variables
            data = b""
    
            while True: # Buffering Data
                incommingData = conn.recv(2048) # Reciving 2048 bytes of Data
                dataList.append(incommingData)

                if sys.getsizeof(incommingData) < 34:
                    break
                
            for i in dataList:
                data = data + i

            if len(data) > 0:
                self.display.log("[{}] Got {} bytes of Data! ASCII : {}".format(round(time.time()-timestamp, 3), sys.getsizeof(data), str(data, "ascii")), src.DEBUG, self.name)

            if "!EXIT!" in str(data, "ascii"):
                break

    except Exception as E:
        self.display.log("While reciving Data a Exception accured:", ERROR, self.name)
        self.display.log(E, ERROR)
    
def dataUpdater(self, conn, timestamp):
    try: # Reciving Data
        datalog = []
        getWall = lambda x: 1 if x > 128 else 0

        while self.display.running:     
            
            # Reciving Color Sensor Values
            incommingData = str(conn.recv(4096), "ascii")

            try:
                incommingData = json.loads(incommingData)
                self.display.colorSensor = incommingData["color"]
                self.display.infraSensor = incommingData["infra"]
                moved = incommingData["moved"]
                facing = incommingData["facing"]

                if moved == 0:
                    self.display.pos[1] += 1
                elif moved == 1:
                    self.display.pos[1] -= 1 
                elif moved == 2:
                    self.display.pos[0] += 1                 
                elif moved == 3:
                    self.display.pos[0] -= 1     

                for x in range(len(self.display.mapData)):
                    for y in range(len(self.display.mapData[x])):
                        if self.display.mapData[x][y] == 2:
                            self.display.mapData[x][y] = 0

                try:
                    if facing == 0:
                        self.display.mapData[self.display.pos[0]][self.display.pos[1] + 1] = getWall(incommingData["infra"])

                    elif facing == 1:
                        self.display.mapData[self.display.pos[0]][self.display.pos[1] - 1] = getWall(incommingData["infra"])

                    elif facing == 2:
                        self.display.mapData[self.display.pos[0] + 1][self.display.pos[1]] = getWall(incommingData["infra"])

                    elif facing == 3:
                        self.display.mapData[self.display.pos[0] - 1][self.display.pos[1]] = getWall(incommingData["infra"])
                except:
                    pass

                if self.display.pos[0] >= 0 and self.display.pos[0] < len(self.display.mapData) and self.display.pos[1] >= 0 and self.display.pos[1] < len(self.display.mapData[0]):
                    self.display.mapData[self.display.pos[0]][self.display.pos[1]] = 2

            except Exception as E:
                traceback.print_exc()

    except Exception as E:
        self.display.log("While reciving Data a Exception accured:", src.ERROR, self.name)
        self.display.log(E, src.ERROR)

if __name__ == "__main__": # Main Fuction

    cmdConnection = networking.Core.ServerCon(src.address, src.cmdPort, "CMD ", cmdUpdater) # Creating Command Connection Thread
    dataConnection = networking.Core.ServerCon(src.address, src.dataPort, "data", dataUpdater) # Creating Data Connection Thread

    display = Display(cmdConnection, dataConnection) # Creating Window Object

    cmdConnection.display = display # Link Cmd Connection Thread with Window Object
    dataConnection.display = display # Link Data Connection Thread with Window Object

    display.mainloop() # Starting Mainloop


