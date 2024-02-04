
RESET = "\33[0m"

BLACK = "\33[30m"
RED = "\33[31m"
GREEN = "\33[32m"
YELLOW = "\33[33m"
BLUE = "\33[34m"
PURPLE = "\33[35m" 
LIGHTBLUE = "\33[36m"
WHITE = "\33[37m"

BOLD = "\33[1m"    
UNDERLINE = "\33[4m"
INVERTED = "\33[7m"

class bg:
    BLACK_BG = "\33[40m"
    RED_BG = "\33[41m"
    GREEN_BG = "\33[42m"
    YELLOWBG = "\33[43m"
    BLUE_BG = "\33[44m"
    PURPLE_BG = "\33[45m" 
    LIGHTBLUE_BG = "\33[46m"
    WHITE_BG = "\33[47m"

def getColorInt(fg, bg):
    return "\33[38;5;" + str(fg) + "m" + "\33[48;5;" + str(bg) + "m"

def colored(text, fg, bg=BLACK):
    return fg + bg + str(text) + RESET 

