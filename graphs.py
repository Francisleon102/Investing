import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
from queue import Empty

class MainWindow(QMainWindow):
    def __init__(self, mp_q):
        super().__init__()
        self.mp_q = mp_q

        self.setWindowTitle("Live Graph")
        self.resize(800, 500)

        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        self.plot_widget.setBackground('k')
        self.plot_widget.showGrid(x=True, y=True)

        self.x = []
        self.y = []

        self.curve = self.plot_widget.plot(
            pen=pg.mkPen(color='c', width=2)
        )

        # Timer pulls from multiprocessing queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(16)  # ~60 FPS

    def update_plot(self):
        # Drain queue without blocking UI
        while True:
            try:
                kind, msg = self.mp_q.get_nowait()
            except Empty:
                break

            if kind == "stock_trade":
                price = msg.get("p") 
                if price is not None:
                    self.y.append(price)
                    self.x.append(len(self.y))

        if self.y:
            self.curve.setData(self.x[-500:], self.y[-500:])

def run(mp_q):
    app =  QApplication(sys.argv)
    window = MainWindow(mp_q)
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit("Run from main.py")