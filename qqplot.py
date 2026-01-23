import numpy as np
import pyqtgraph as pg
from PyQt6 import QtCore
from config import xdf

app = pg.mkQApp("RT Scatter")

win = pg.GraphicsLayoutWidget(title="Real-time Scatter")
p = win.addPlot()
p.showGrid(x=True, y=True)


x = xdf.iloc[:,2]
y = xdf.iloc[:,6]

p.setXRange(min(x), max(x))
p.setYRange(min(y), max(y))
p.enableAutoRange(x=False, y=False)

sc = pg.ScatterPlotItem(size=9, brush='g')
p.addItem(sc)

idx = 0  # point index to reveal


def update():
  global idx
  if idx >= len(x):
    timer.stop()
    return
  sc.setData(x[:idx + 1], y[:idx + 1])
  idx += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(160)   # ~60 FPS

#update()  # draw first point immediately
win.show()
pg.exec()
