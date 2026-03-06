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

        # =========================
        # 1) WINDOW / LAYOUT
        # =========================
        self.win = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.win)

        # =========================
        # 2) PLOTS (rows/cols)
        # =========================
        # Row 0: Trades
        self.p0 = self.win.addPlot(row=0, col=0, title="Trades: Price vs Size")
        self.p0.showGrid(x=True, y=True)

        # Row 0 col 1: Quotes
        self.pQ = self.win.addPlot(row=0, col=1, title="Quotes: Bid vs Ask (example)")
        self.pQ.showGrid(x=True, y=True)

        # Row 1: Bars
        self.p1 = self.win.addPlot(row=1, col=0, colspan=2, title="Size Bars")
        self.p1.showGrid(x=True, y=True)

        # =========================
        # 3) ITEMS (line/scatter/bar/text)
        # =========================
        # Trades items
        self.line0 = self.p0.plot(pen=pg.mkPen('c', width=2))
        self.scatter0 = pg.ScatterPlotItem(size=6, brush=pg.mkBrush('y'))
        self.p0.addItem(self.scatter0)

        self.text0 = pg.TextItem("Trades: 0", color='g')
        self.p0.addItem(self.text0)

        # Quotes items (keep simple: one line for bid, one line for ask)
        self.bid_line = self.pQ.plot(pen=pg.mkPen('g', width=2))
        self.ask_line = self.pQ.plot(pen=pg.mkPen('r', width=2))

        # Bars
        self.bars1 = pg.BarGraphItem(x=[], height=[], width=0.9)
        self.p1.addItem(self.bars1)

        # =========================
        # 4) DATA BUFFERS
        # =========================
        # trades
        self.trade_p = []
        self.trade_s = []

        # quotes
        self.bid_p = []
        self.bid_s = []
        self.ask_p = []
        self.ask_s = []

        # counters
        self.trade_count = 0

        # =========================
        # 5) TIMER
        # =========================
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(16)

    # =========================
    # 6) MESSAGE HANDLERS
    # =========================
    def on_stock_trade(self, msg):
        price = msg.get("p")
        size  = msg.get("s")
        if price is None or size is None:
            return
        self.trade_p.append(price)
        self.trade_s.append(size)
        self.trade_count += 1

    def on_stock_quotes(self, msg):
        # correct keys from your quote example:
        # bp, bs, ap, as
        bp = msg.get("bp")
        bs = msg.get("bs")
        ap = msg.get("ap")
        aS = msg.get("as")
        if bp is not None and bs is not None:
            self.bid_p.append(bp)
            self.bid_s.append(bs)
        if ap is not None and aS is not None:
            self.ask_p.append(ap)
            self.ask_s.append(aS)

    # =========================
    # 7) UPDATE LOOP
    # =========================
    def update_plot(self):
        # ---- drain queue
        while True:
            try:
                msg_type, msg = self.mp_q.get_nowait()
            except Empty:
                break

            if msg_type == "stock_trade":
                self.on_stock_trade(msg)
            elif msg_type == "stock_quotes":
                self.on_stock_quotes(msg)
            # elif msg_type == "option_trade": ...
            # elif msg_type == "option_quote": ...

        # ---- render trades
        if self.trade_s:
            xs = self.trade_p[-500:]
            ys = self.trade_s[-500:]

            self.line0.setData(xs, ys)
            self.scatter0.setData(x=xs, y=ys)

            self.text0.setText(f"Trades: {self.trade_count}")
            self.text0.setPos(xs[-1], ys[-1] + 5)

            idx = list(range(len(ys)))
            self.bars1.setOpts(x=idx, height=ys, width=0.9)

        # ---- render quotes (example: plot sizes vs prices)
        if self.bid_s and self.ask_s:
            bpx = self.bid_p[-500:]
            bsy = self.bid_s[-500:]
            apx = self.ask_p[-500:]
            asy = self.ask_s[-500:]

            self.bid_line.setData(bpx, bsy)
            self.ask_line.setData(apx, asy)

def run(mp_q):
    app = QApplication(sys.argv)
    window = MainWindow(mp_q)
    window.show()
    return app.exec()

# =========================
# OPTIONAL: rate-of-change helper (fix: use price "p" not "s")
# =========================
last_price = None
last_time = None

def RateofChange(trade_msg):
    global last_price, last_time, ratex
    Pnow = trade_msg.get("p")
    ts = trade_msg.get("t")
    if Pnow is None or ts is None:
        return

    Tnow = ts.seconds + ts.nanoseconds * 1e-9

    if last_price is not None:
        dt = Tnow - last_time
        if dt > 0:
            ratex = (Pnow - last_price) / dt

    last_price = Pnow
    last_time = Tnow

if __name__ == "__main__":
    raise SystemExit("Run from main.py")