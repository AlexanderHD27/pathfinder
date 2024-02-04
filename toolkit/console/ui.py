from toolkit.console import color
import sys

def rotStringRect(string: str):
    a = string.split("\n")
    b = []

    for j in range(len(a[0])):
        b.append("")
        for i in a:
            b[j] += i[j]     
    b.reverse()
    c = ""
    for i in b:
        c = c + i + "\n"
    c = c[:-1]
    return c


def table(array: list, cellsize: int, style=1, direction=-1):

    if type(array) != list:
        raise ValueError("array has to be a list!")
    if type(cellsize) != int:
        raise ValueError("cellsize has to be a int!")

    if len(array) <= 0:
        if style == 1:
            return "┌┐\n└┘\n"
        elif style == 2:
            return "┌┐\n└┘\n"
        elif style == 0:
            return "┌┐\n└┘\n"
        else:
            return ""
    
    if type(array[0]) != list:
        if direction <= 0:
            array = [array]
        else:
            array = [[i] for i in array]


    if style == 1:
        table = "┌" + "─"*len(array[0])*cellsize + (len(array[0])-1)*"─" + "┐\n"
    elif style == 2:
        table = "┌" + ("─"*cellsize + "┬")*len(array[0])
        table = table[:-1] + "┐\n"
    elif style == 0:
        table = "┌" + "─"*len(array[0])*cellsize + "┐\n"
    else:
        table = ""
 

    for x in range(len(array)):
        if style >= 0:
            table = table + "│"
        
        for y in range(len(array[x])):
            table = table + str(array[x][y]).ljust(cellsize)[:cellsize]
            if style == 1:
                table = table + " "
            elif style == 2:
                table = table + "│"

        if style == 1:
            table = table[:-1] + "│\n"
        elif style >= 0 and style != 2:
            table = table + "│\n"
        else:
            table = table + "\n"
            
        if style == 2 and x+1 != len(array):
            table = table + "├" + (len(array[0]))*("─"*cellsize + "┼")
            table = table[:-1] + "┤\n"

    if style == 1:
        table = table + "└" + "─"*len(array[0])*cellsize + (len(array[0])-1)*"─" + "┘"
    elif style == 2:
        table = table + "└" + ("─"*cellsize + "┴")*len(array[0])
        table = table[:-1] + "┘\n"
    elif style == 0:
        table = table + "└" + "─"*len(array[0])*cellsize + "┘"
    
    return table

def colorTable(array: list, cellsize: int, selected: dict, style=1, direction=-1):
    pass

    if type(array) != list:
        raise ValueError("array has to be a list!")
    if type(cellsize) != int:
        raise ValueError("cellsize has to be a int!")
    if type(selected) != dict:
        raise ValueError("selected has to be a dict!")

    if len(array) <= 0:
        if style == 1:
            return "┌┐\n└┘\n"
        elif style == 2:
            return "┌┐\n└┘\n"
        elif style == 0:
            return "┌┐\n└┘\n"
        else:
            return ""
    
    if type(array[0]) != list:
        if direction <= 0:
            array = [array]
        else:
            array = [[i] for i in array]


    if style == 1:
        table = "┌" + "─"*len(array[0])*cellsize + (len(array[0])-1)*"─" + "┐\n"
    elif style == 2:
        table = "┌" + ("─"*cellsize + "┬")*len(array[0])
        table = table[:-1] + "┐\n"
    elif style == 0:
        table = "┌" + "─"*len(array[0])*cellsize + "┐\n"
    else:
        table = ""


    for x in range(len(array)):
        if style >= 0:
            table = table + "│"
        
        for y in range(len(array[x])):
            if (x, y) in selected.keys():
                table = table + selected.get((x, y))
            table = table + str(array[x][y]).ljust(cellsize)[:cellsize] + color.RESET
            if style == 1:
                table = table + " "
            elif style == 2:
                table = table + "│"

        if style == 1:
            table = table[:-1] + "│\n"
        elif style >= 0 and style != 2:
            table = table + "│\n"
        else:
            table = table + "\n"
            
        if style == 2 and x+1 != len(array):
            table = table + "├" + (len(array[0]))*("─"*cellsize + "┼")
            table = table[:-1] + "┤\n"

    if style == 1:
        table = table + "└" + "─"*len(array[0])*cellsize + (len(array[0])-1)*"─" + "┘"
    elif style == 2:
        table = table + "└" + ("─"*cellsize + "┴")*len(array[0])
        table = table[:-1] + "┘\n"
    elif style == 0:
        table = table + "└" + "─"*len(array[0])*cellsize + "┘"
    
    return table


def progressbar(summ, iteration, suffix="", prefix="", leaght=50):
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / summ))
    filledLength = int(leaght * iteration // summ)
    bar = "█" * filledLength + '-' * (leaght - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s' % (suffix, bar, percent, prefix))
    sys.stdout.flush()

def statebar(summ, stat, suffix="", prefix="", leaght=50):
    filledLength = int(leaght * stat // summ)
    if filledLength == 0:
        bar = "|" + '-' * (leaght - filledLength)
    elif filledLength > leaght:
        bar = "-"*leaght
    else:
        bar = "="*(filledLength-1) + "|" + '-' * (leaght - filledLength)

    sys.stdout.write('\r%s |%s| %s' % (suffix, bar, prefix))
    sys.stdout.flush()

def percent(summ, iteration, suffix="", prefix=""):
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / summ))
    sys.stdout.write('\r%s %s%% %s' % (suffix, percent, prefix))
    sys.stdout.flush()


def update(text):
    for i in range(len(text)): # pylint: disable=unused-variable
        sys.stdout.write("\033[A\033[K")
    printUpdate(text)
    #for i in range(len(text)): # pylint: disable=unused-variable
     #   sys.stdout.write("\033[B")
    #sys.stdout.write(text)
    sys.stdout.flush()

def printUpdate(text):
    for i in text.split("\n"):
        sys.stdout.write(i + "\n")
    sys.stdout.flush()


def chartLines(array: list, hight: int, start: int, step: int, numberCap=-1):
    values = array.copy()
    valueMap = []
    chart = ""

    n = start
    for i in range(hight+1):  
        valueMap.append(n)
        n += step 

    for i in range(len(values)):            
        if values[i] <= valueMap[0]:
            values[i] = -1
        elif values[i] > valueMap[-1]:
            values[i] = len(valueMap)
        else:
            for j in range(len(valueMap)):
                if j != 0 and valueMap[j-1] < values[i] and valueMap[j] >= values[i]:
                    values[i] = j
                    break
                
                elif j == 0 and valueMap[j] == values[i]:
                    values[i] = j
                    break

    for i in range(len(values)): 
            if i != 0:

                # Overflow + last obverflow
                if (values[i] < 0 and values[i-1] < 0) or (values[i] > len(valueMap) and values[i-1] > len(valueMap)):
                    chart += " "*hight + "\n"

                # Same
                elif values[i] == values[i-1]:
                    chart += " "*(values[i]-1) + "─" + " "*(hight-values[i]) + "\n"

                # Overflow
                elif values[i] < 0:
                    chart += "│"*(values[i-1]-1) + "╮" + " "*(hight-values[i-1]) + "\n"

                elif values[i] > len(valueMap)-1:
                    chart += " "*(values[i-1]-1) + "╯" + "│"*(hight-values[i-1]) + "\n"

                # Last overflow
                elif values[i-1] < 0:
                    chart += "│"*(values[i]-1) + "╭" + " "*(hight-values[i]) + "\n"

                elif values[i-1] > len(valueMap)-1:
                    chart += " "*(values[i]-1) + "╰" + "│"*(hight-values[i]) + "\n"

                elif values[i-1] > 0 and values[i] == 0:
                    chart += " "*(values[i]-1) + "─" + " "*(hight-values[i]) + "\n"

                # Normal
                elif values[i] > values[i-1]:
                    chart += " "*(values[i-1]-1) + "╯" + "│"*(values[i]-values[i-1]-1) + "╭" + " "*(hight-values[i]) + "\n"

                elif values[i] < values[i-1]:
                    chart += " "*(values[i]-1) + "╰" + "│"*(values[i-1]-values[i]-1) + "╮" + " "*(hight-values[i-1]) + "\n"

            else:
                if values[i] <= 0 or values[i] > len(valueMap)-1:
                    chart += " "*hight + "\n"
                else: 
                    chart += " "*(values[i]-1) + "─" + " "*(hight-values[i]) + "\n"
    

    chart = rotStringRect(chart[:-1])
    chart = chart.split("\n")

    leaght = 0
    for i in valueMap:
        if len("{: f}".format(i)) > leaght:
            leaght = len("{: f}".format(i)) - numberCap
    
    valueMap.reverse()

    for i in range(len(chart)):
        if numberCap > 0:
            chart[i] = "{: f}".format(valueMap[i])[:-numberCap] .rjust(leaght)+ " ┤" + chart[i] + "│"
        else:
            chart[i] = "{: f}".format(valueMap[i]).rjust(leaght) + " ┤" + chart[i] + "│"

    charttext = ""
    for i in chart:
        charttext += i + "\n"
    chart = charttext

    chart += " "*leaght + " └" + "─"*len(values) + "┘"
    chart =  " "*leaght + " ┌" + "─"*len(values) + "┐\n" + chart
    return chart


def XYview(cursor: tuple, points: list, leath: int, wight: int):
    text = "┌" + "──"*wight + "┐\n"

    for y in range(leath):
        text += "│" 
        for x in range(wight):
            if cursor == (x, y):
                text += "O "
            elif cursor[0] == x:
                text += "| "
            elif cursor[1] == y:
                text += "--"
            elif (x, y) in points:
                text += "X "
            else:
                text += "  "

        text += "│\n" 
    return text + "└" + "──"*wight + "┘\n"

