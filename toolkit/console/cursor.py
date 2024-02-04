import os
import sys

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


def moveCursor(x, y):
    sys.stdout.write("\33[{};{}H".format(y, x))
    sys.stdout.flush()

def moveCursorUp(n=1):
    sys.stdout.write("\33[{}A".format(n))
    sys.stdout.flush()

def moveCursorDown(n=1):
    sys.stdout.write("\33[{}B".format(n))
    sys.stdout.flush()  

def moveCursorFor(n=1):
    sys.stdout.write("\33[{}C".format(n))
    sys.stdout.flush()  

def moveCursorBack(n=1):
    sys.stdout.write("\33[{}D".format(n))
    sys.stdout.flush()  

def cleanAll():
    sys.stdout.write("\33[2J")
    sys.stdout.flush()  

def cleanLine():
    sys.stdout.write("\033[K")
    sys.stdout.flush()  

def cleanLines(n=1): 
    for i in range(n): # pylint: disable=unused-variable
        sys.stdout.write("\033[K")
        sys.stdout.write("\33[{}A".format(1))
    sys.stdout.flush()
    moveCursorDown(n)

def printLocation(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

def hideCursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def showCursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

