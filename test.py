# scatter_highlight_example.py

import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

# Sample data
x = np.arange(20)
y = np.random.randint(5, 100, 20)
threshold = 60

# Create brushes per point
brushes = [
    pg.mkBrush(255, 50, 50) if val > threshold else pg.mkBrush(50, 120, 255)
    for val in y
]

# Optional: change size too
sizes = [
    14 if val > threshold else 8
    for val in y
]

app = QtWidgets.QApplication(sys.argv)

win = pg.GraphicsLayoutWidget(show=True, title="Scatter Highlight Example")
p = win.addPlot(title="Highlight Large Values")
p.showGrid(x=True, y=True)

scatter = pg.ScatterPlotItem(
    x=x,
    y=y,
    size=sizes,
    brush=brushes,     # 👈 per-point coloring
    pen=pg.mkPen(None)
)

p.addItem(scatter)

QtWidgets.QApplication.instance().exec()