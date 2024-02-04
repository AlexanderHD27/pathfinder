import socket

# Connection values
address = socket.gethostbyname(socket.gethostname())
#address = "127.0.0.1"
#address = "169.254.209.59"
cmdPort = 63401
dataPort = 63402
enableBluetooth = True

try:
    connectionFamily = socket.AF_BLUETOOTH
except:
    enableBluetooth = False
    connectionFamily = socket.AF_INET
    #address = "127.0.0.1"


# Logging Values
DEBUG = 0
ERROR = 1
NOTIFY = 2

loggingLevels = {
    DEBUG : (237, 237, 237),
    ERROR : (255, 15, 15),
    NOTIFY: (136, 245, 27)
}

loggingLevelsNames = {
    DEBUG : "DEBUG ",
    ERROR : "ERROR ",
    NOTIFY: "NOTIFY"
}

# Map Values
mapColor = {
    -1 : (123, 171, 167), # unknow
    0 : (136, 245, 27), # Free
    1 : (255, 15, 15), # Solid
    2 : (255, 241, 43) # Robot
}