import src.client.maze as maze 
from toolkit.console import color
from toolkit.console import ui
from PIL import Image

array = [
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1]
]


root = maze.scanNodes(array)
path = maze.findPath((2, 2), (1, 2), root)
print(ui.colorTable(array, 1, dict(zip(path, [color.GREEN]*len(path)))))
print(path)

root = maze.scanNodes(array)
path = maze.findPath((1, 2), (0, 2), root)
print(ui.colorTable(array, 1, dict(zip(path, [color.GREEN]*len(path)))))
print(path)