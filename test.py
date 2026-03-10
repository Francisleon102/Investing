import numpy as np
import pyqtgraph as pg
from PyQt6 import QtCore
import os
from cuml.cluster import HDBSCAN
import math
print("test PID:", os.getpid())

app = pg.mkQApp("RT Scatter")
win = pg.GraphicsLayoutWidget(title="Real-time Scatter")
p = win.addPlot()
p.showGrid(x=True, y=True)

N = 500
x = np.random.normal(size=N)
y = np.random.normal(size=N)

sc = pg.PlotCurveItem(size=5)
text = pg.TextItem(color='g')
p.addItem(sc)
p.addItem(text)
i = 0

def update():
    global i
    # show points up to i (growing trail)
    sc.setData(x[:i+1], y[:i+1])
    cluster(i)
   
    

    i = (i + 1) % N

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(16)  # ~60 FPS

def cluster(x): 
    e = 1 / math.exp(x)
    text.setText(f"e :{e}")
    text.setPos(1,10)
    pass 

win.show()
pg.exec()