
import numpy as np
from collections import deque
import pyqtgraph as pg
from PyQt6 import QtCore
import pandas as pd
import os
import realtime 

print("PID test" , os.getegid())

rate = None

app = pg.mkQApp("RT Scatter")

win = pg.GraphicsLayoutWidget(title="Real-time Scatter")
p = win.addPlot()
p.showGrid(x=True, y=True)

l = deque()
def update():
    l.append(rate)
    print(l)
        
        

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(600)   # ~60 FPS

win.show()
pg.exec()
