from time import sleep

import numpy as np
import pyqtgraph as pg
from PyQt6 import QtCore
import os
import math
import sys

print("test PID:", os.getpid())

app = pg.mkQApp("RT Scatter")
win = pg.GraphicsLayoutWidget(title="RT Scatter")
p = win.addPlot()
p.showGrid(x=True, y=True)

N = 10
x = np.random.normal(size=N)
y = np.random.normal(size=N)

sc = pg.PlotDataItem(pen=None, symbol='o', symbolSize=5)
text = pg.TextItem(color='g')
p.addItem(sc)
p.addItem(text)

i = 0
j = [0.23, 0.78, 0.11, 0.65, 0.42, 0.90, 0.33, 0.57, 0.12, 0.48]

def cluster(val, j):
    e = math.exp(-j[i] * val)
    text.setText(f"e: {round(e , 6)}")
    text.setPos(1, 1)

def update():
    global i , j
    sc.setData(x[:i+1], y[:i+1])
    cluster(i, j)
    sleep(1)
    i = (i + 1) % N
   

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(16)

win.show()
sys.exit(pg.exec())