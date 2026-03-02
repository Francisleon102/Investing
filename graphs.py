import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Live Graph")
        self.resize(800, 500)

        # Plot widget
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)

        # Styling
        self.plot_widget.setBackground('k')
        self.plot_widget.showGrid(x=True, y=True)

        # Data
        self.x = np.arange(100)
        self.y = np.random.randn(100)

        self.curve = self.plot_widget.plot(
            self.x,
            self.y,
            pen=pg.mkPen(color='c', width=2)
        )

def run():
    app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())
