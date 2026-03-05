import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
from queue import Empty
ratex = None
class MainWindow(QMainWindow):
    def __init__(self, mp_q):
        super().__init__()
        self.mp_q = mp_q

        self.setWindowTitle("Live Graph")
        self.resize(1300, 800)

        # ✅ layout that supports rows/cols
        self.win = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.win)

        # ---- Row 0: scatter/line view
        self.p0 = self.win.addPlot(row=0, col=0, title="Price vs Size (Scatter/Line)")
        #self.p0.setBackground('k')
        self.p0.showGrid(x=True, y=True)

        #self.line0 = self.p0.plot(pen=pg.mkPen('c', width=2))
        self.scatter0 = pg.ScatterPlotItem(size=6, brush=pg.mkBrush('y'))
        self.p0.addItem(self.scatter0)
        
        #.....Text Item
        self.text = pg.TextItem("Trades: 0", color='g')
        self.p0.addItem(self.text)
        
      
            # ---- Row 1: bar view
        self.p1 = self.win.addPlot(row=1, col=0, title="Size Bars")
        self.p1.showGrid(x=True, y=True)

        self.bars1 = pg.BarGraphItem(x=[], height=[], width=0.9)
        self.p1.addItem(self.bars1)

        self.x = []
        self.y = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(16)

    def update_plot(self):
        while True:
            try:
                msg_type, msg = self.mp_q.get_nowait()
            except Empty:
                break

            if msg_type == "stock_trade":
                price = msg.get("p")
                size  = msg.get("s")
                if price is not None and size is not None:
                    self.x.append(price)
                    self.y.append(size)

        if self.y:
            xs = self.x[-500:]
            ys = self.y[-500:]

       
            # row 0
            self.line0.setData(ratex)
            #self.scatter0.setData(x=xs, y=ys)
            self.text.setPos(xs[-1], ys[-1] +5)

            # row 1 (bars indexed by sample # so spacing is uniform)
            idx = list(range(len(ys)))
           # self.bars1.setOpts(x=idx, height=ys, width=0.9)

def run(mp_q):
    app = QApplication(sys.argv)
    window = MainWindow(mp_q)
    window.show()
    return app.exec()


last_price = None
last_time = None
last_size = None 

def RateofChange(q):
    global last_price, last_time

    Pnow = q["s"]
    ts = q["t"]
    Tnow = ts.seconds + ts.nanoseconds * 1e-9
    if last_price is not None:
        dt = Tnow - last_time
        if dt > 0:
            rate = (Pnow - last_price) / dt
            ratex = rate
    last_price = Pnow
    last_time = Tnow



if __name__ == "__main__":
    raise SystemExit("Run from main.py")