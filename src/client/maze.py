from toolkit.console import ui, color

import traceback
import json
import time

# Networking
sock = None
def recvall(BUFF_SIZE = 2048):
        global sock
        data = b""
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data   

def recv():
    return json.loads(recvall().decode("utf-8"))

def send(data):
    global sock
    sock.sendall(json.dumps(data).encode("utf-8"))
    return json.loads(recvall().decode("utf-8"))

def sendop(op, data={}):
    data_ = {"op": op}
    data_.update(data)
    return send(data_)

def latency():
    start = time.time()
    sendop("echo")
    return time.time()-start

# Dijkstra Nodes
class Node:

    # OOP suff 
    def __init__(self, pos, nodeId, n):
        self.neighbors = n
        self.pos = pos
        self.id = nodeId
        self.compress = True

    def __repr__(self):
        return "Node({:2d}, {:2d} )".format(self.pos[0], self.pos[1])

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.pos)

    def __lt__(self, other):
        return self.pos < other.pos

    def __gt__(self, other):
        return self.pos > other.pos

    # geting Postion of potationl neighboars
    def __getNeighborsPos__(self):
        return [
                (self.pos[0] + 1, self.pos[1]), 
                (self.pos[0] - 1, self.pos[1]), 
                (self.pos[0], self.pos[1] + 1), 
                (self.pos[0], self.pos[1] - 1)
               ]

    # Convert Node network to a list
    def getNodeList(self, nodes_visted=[], first=True):
        nodes_visted = nodes_visted

        if first:
            nodes_visted = []

        if self in nodes_visted:
            return nodes_visted
        
        nodes_visted.append(self)
        for i in self.neighbors:
            nodes_visted = i.getNodeList(nodes_visted=nodes_visted, first=False)
        
        return nodes_visted

# Search for A Node    
def searchNodePos(nodes: Node, pos):
    for i in nodes:
        if i.pos == pos:
            return i
    
def searchNodeId(nodes: Node, id):
    for i in nodes:
        if i.id == id:
            return i

# Converting Array to Nodes
def scanNodes(array):
    node_list = []
    node_count = 0
    
    for x,i in enumerate(array):
        for y,j in enumerate(i):
            if j == 1:
                node_list.append(Node((x, y), node_count, []))
                node_count += 1

    for i in node_list:
        for j in i.__getNeighborsPos__():
            
            res = searchNodePos(node_list, j)
            if res != None:
                if not i in res.neighbors:
                    res.neighbors.append(i)
                if not res in i.neighbors:
                    i.neighbors.append(res)

    return searchNodeId(node_list, 0)

# Pring out array with Nodes marked
def printColorNodes(array, root: Node):
    color_dict = {}
    for i in root.getNodeList():
        color_dict.update({i.pos : color.GREEN})
    print(ui.colorTable(array, 1, color_dict))

# Dijkstra Table
class Table:
    
    # Some more OOP stuff
    def __init__(self, node: Node, dist, prev, index=0):
        self.node = node
        self.dist = dist
        self.prev = prev
        self.index = index
        
        self.next = None

    def __str__(self):
        return "[ {:03d} | {:04d} | {} | {} ]".format(self.index, self.dist, self.node, str(self.prev))

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.dist > other.dist
    
    def __lt__(self, other):
        return self.dist < other.dist

    # Adding new entry to table
    def append(self, node: Node, dist, prev):
        if self.next != None:
            self.next.append(node, dist, prev)
        else:
            self.next = Table(node, dist, prev, index=self.index + 1)

    # Converting Table to List
    def getList(self, all=[], first=True):
        all = all
        if first:
            all = []

        all.append(self)
        if self.next != None:
            self.next.getList(all, first=False)
        return all

    # Search for Entry by proporty
    def getEntryByNode(self, node):
        if self.node == node:
            return self
        elif self.next != None:
            return self.next.getEntryByNode(node)
        else:
            return None

    def getEntryByPos(self, pos):
        if self.node.pos == pos:
            return self
        elif self.next != None:
            return self.next.getEntryByPos(pos)
        else:
            return None

    # printing table to console
    def printTable(self):
        print(self)
        if self.next != None:
            self.next.printTable()

    # Backtracking for Djikstra
    def travers(self, table, visited=[], first=True):
        visited = visited
        if first:
            visited = []

        visited.append(self.node.pos)
        if self.prev == None:
            return visited

        return table.getEntryByNode(self.prev).travers(table, visited=visited, first=False)


# Convert array of pos to dirctions!
def getDirction(pos_list):
    dirct_list = []
    last = pos_list[0]
    for i in pos_list[1:]:
        dif = (i[0] - last[0], i[1] - last[1])
        if dif[0] == 0:
            if dif[1] > 0:
                for _ in range(dif[1]):
                    dirct_list.append("n")
            else:
                for _ in range(dif[1] * -1):
                    dirct_list.append("s")
        else:
            if dif[0] > 0:
                for _ in range(dif[0]):
                    dirct_list.append("e")
            else:
                for _ in range(dif[0] * -1):
                    dirct_list.append("w")
        last = i
        
    return dirct_list

# Creating Table from Nodes
def createTable(root: Node):
    root = root
    table = Table(root, 0, None)
    nodes = root.getNodeList()
    nodes.remove(root)
    for i in nodes:
        table.append(i, 10**10, None)
    return table

# Executing the Dijkstra algorthim
def getDijkstraTable(root: Node):
    table = createTable(root)
    unvisted = sorted(table.getList())
    unvisted.reverse()
    visited = []

    while len(unvisted) > 0:
        unvisted = sorted(unvisted)
        unvisted.reverse()
        current = unvisted.pop()
        for i in current.node.neighbors:
            current_table = table.getEntryByPos(i.pos)
            if current_table.dist > current.dist + 1:
                current_table.dist = current.dist + 1
                current_table.prev = current.node

        visited.append(current)

    return table

# Wrapping complicate Math up!
def findPath(start, stop, root: Node):
    table = getDijkstraTable(searchNodePos(root.getNodeList(), tuple(stop))) # Stop
    start = table.getEntryByPos(tuple(start)) # Start
    
    p = start.travers(table)
    return p


# Maze navigation
class Maze:

    # OOP Stuff again...
    def __init__(self, size, start_pos):
        self.map = [[-1 for j in range(size[1])] for i in range(size[0])]
        self.color_map = [[(0, 0, 0) for j in range(size[1])] for i in range(size[0])]
        self.pos = list(start_pos)
        self.dirction = "n"
        self.write(self.pos, 1)

        self.visited = [tuple(start_pos)]
        self.unvisted = []

    def __str__(self):
        s = ui.table(self.map, 2) + "\n"
        s += str(self.pos) + " "
        if self.dirction == "n":
            s += "/\\"
        elif self.dirction == "s":
            s += "\\/"
        elif self.dirction == "e":
            s += "->"
        elif self.dirction == "w":
            s += "<-"

        return s

    def __repr__(self):
        return self.__str__()


    # Preventing Writes/Reads outside of the map
    def senatize(self, pos):
        return pos[0] >= 0 and pos[0] < len(self.map) and pos[1] >= 0 and pos[1] < len(self.map[0])

    # Save write to map
    def write(self, pos, value):
        if self.senatize(pos):
            self.map[pos[0]][pos[1]] = value
            return True
        return False

    # Save read from map
    def get(self, pos):
        if self.senatize(pos):
            return self.map[pos[0]][pos[1]]
        return None

    # Converting Sensor values to map data
    def pares(self, v):
        res = []
        if v[0] > 70:
            res.append(1)
        else:
            res.append(0)

        if v[1] > 60:
            res.append(1)
        else:
            res.append(0)

        if v[2] > 70:
            res.append(1)
        else:
            res.append(0)

        return res


    # Lets the robot scan his suronding and write it to map
    def scan(self):
        sensor_values = []
        for i in sendop("scan_old")["scan"]:
            sensor_values.append(i)
        sensor_values = self.pares(sensor_values)
        sensor_values.reverse()
        news = []

        if self.dirction == "n": # w n e 
            self.write((self.pos[0], self.pos[1]-1), sensor_values.pop())
            self.write((self.pos[0]-1, self.pos[1]), sensor_values.pop())
            self.write((self.pos[0], self.pos[1]+1), sensor_values.pop())

            news = [
                (self.pos[0], self.pos[1]-1),
                (self.pos[0]-1, self.pos[1]),
                (self.pos[0], self.pos[1]+1)
            ]

        elif self.dirction == "e": # n e s
            self.write((self.pos[0]-1, self.pos[1]), sensor_values.pop())
            self.write((self.pos[0], self.pos[1]+1), sensor_values.pop())
            self.write((self.pos[0]+1, self.pos[1]), sensor_values.pop())

            news = [
                (self.pos[0]-1, self.pos[1]),
                (self.pos[0], self.pos[1]+1),
                (self.pos[0]+1, self.pos[1])
            ]

        elif self.dirction == "s": # e s w
            self.write((self.pos[0], self.pos[1]+1), sensor_values.pop())
            self.write((self.pos[0]+1, self.pos[1]), sensor_values.pop())
            self.write((self.pos[0], self.pos[1]-1), sensor_values.pop())

            news = [
                (self.pos[0], self.pos[1]+1),
                (self.pos[0]+1, self.pos[1]),
                (self.pos[0], self.pos[1]-1)
            ]

        elif self.dirction == "w": # s w n
            self.write((self.pos[0]+1, self.pos[1]), sensor_values.pop())
            self.write((self.pos[0], self.pos[1]-1), sensor_values.pop())
            self.write((self.pos[0]-1, self.pos[1]), sensor_values.pop())

            news = [
                (self.pos[0]+1, self.pos[1]),
                (self.pos[0], self.pos[1]-1),
                (self.pos[0]-1, self.pos[1])
            ]
        print(self.visited)
        for i in news:
            if self.get(i) == 1 and (not tuple(i) in self.visited):
                self.unvisted.append(i)

        if self.senatize(self.pos):
            self.color_map[self.pos[0]][self.pos[1]] = tuple(sendop("color")["color"])

    # turn absolute into on diction
    def turn_old(self, d):
        dirs = ["n", "e", "s", "w"]
        rot = dirs.index(d) - dirs.index(self.dirction)

        if rot != 0:
            sendop("turn_old", {"n":rot*90, "d":"r"})
        else:
            pass
        self.dirction = d

    def turn(self, d):
        if d == self.dirction:
            return

        if d == "n":
            sendop("turn", {"n":0})
        elif d == "s":
            sendop("turn", {"n":180})
        elif d == "e":
            sendop("turn", {"n":90})
        elif d == "w":
            sendop("turn", {"n":270})

        self.dirction = d

    # moving n units
    def move(self, n):
        if self.dirction == "n":
            dirc = (-1*n, 0)
        elif self.dirction == "s":
            dirc = (n, 0)
        elif self.dirction == "e":
            dirc = (0, n)
        elif self.dirction == "w":
            dirc = (0, -1*n)
        else:
            dirc = (0, 0)
            
        if not self.senatize((dirc[0] + self.pos[0], dirc[1] + self.pos[1])):
            return False

        sendop("move", {"n":abs(dirc[0]+dirc[1])})
        self.pos[0] = dirc[0] + self.pos[0]
        self.pos[1] = dirc[1] + self.pos[1]
        time.sleep(7)
        self.turn(self.dirction)
        return True

    # moving absolute into on dirction n units
    def moveD(self, n, d):
        self.turn(d)
        return self.move(n)

    # Pathfind and move to a location (dijkstra stuff)
    def goto(self, goal, activ=True, display=False):

        try:
            root = scanNodes(self.map)
            path = findPath(tuple(self.pos), tuple(goal), root)
            last = list(self.pos).copy()
            ins = []

            if display:
                color_dic = {}
                for i in path:
                    color_dic.update({i:color.GREEN})
                print(ui.colorTable(self.map, 1, color_dic))    

            for i in path:
                d = (last[0] - i[0], last[1] - i[1])
                if d == (1, 0): # north
                    if len(ins) > 0 and ins[-1][0] == "n":
                        ins[-1] = ("n", ins[-1][1]+1)
                    else:
                        ins.append(("n", 1))

                elif d == (-1, 0): # south
                    if len(ins) > 0 and ins[-1][0] == "s":
                        ins[-1] = ("s", ins[-1][1]+1)
                    else:
                        ins.append(("s", 1))

                elif d == (0, -1):
                    if len(ins) > 0 and ins[-1][0] == "e":
                        ins[-1] = ("e", ins[-1][1]+1)
                    else:
                        ins.append(("e", 1))

                elif d == (0, 1):
                    if len(ins) > 0 and ins[-1][0] == "w":
                        ins[-1] = ("w", ins[-1][1]+1)
                    else:
                        ins.append(("w", 1))
                last = i

            for i in ins:
                self.moveD(i[1], i[0])
            self.pos = list(goal)
            self.visited.append(goal)
            return True
        except:
            traceback.print_exc()

    # Ex and importing Map data
    def export_map(self, name):
        with open(name + ".json", "w") as f:
            f.write(json.dumps({"map" : self.map, "color_map" : self.color_map}))

    def import_map(self, name):
        with open(name) as f:
            data = json.loads(f.read())
            self.map = data["map"]
            self.color_map = data["color_map"]

    def isFinished(self):
        suc = False
        for i in self.map:
            for j in i:
                if j == -1:
                    suc = True

        suc = not suc
        return suc or len(self.unvisted) <= 0