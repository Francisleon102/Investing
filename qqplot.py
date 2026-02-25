import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg

app = QApplication(sys.argv)

window = QMainWindow()
central = QWidget()
layout = QVBoxLayout()
central.setLayout(layout)
window.setCentralWidget(central)

# PyQtGraph plot
plot = pg.PlotWidget()
curve = plot.plot()

# Qt button
button = QPushButton("Update Data")

layout.addWidget(plot)
layout.addWidget(button)

def update():
    x = np.arange(100)
    y = np.random.randn(100).cumsum()
    curve.setData(x, y)

button.clicked.connect(update)

window.show()
sys.exit(app.exec())