import os
import time
from queue import Empty
from collections import deque
from threading import Thread, Lock


class GraphsRender:
    def __init__(self):
        self.enabled = True

    def update(self, msg_type, msg):
        # template for shared render-related prep
        pass


class Scatter3D:
    def __init__(self):
        self.enabled = True

    def update(self, msg_type, msg):
        # template for 3D scatter logic
        pass


class ClusterWorker:
    def __init__(self):
        self.enabled = True
        self.buffer = deque(maxlen=5000)

    def push(self, msg_type, msg):
        self.buffer.append((msg_type, msg))

    def step(self):
        # template for clustering work
        # example: DBSCAN / HDBSCAN / custom density logic
        pass


class MathWorker:
    def __init__(self):
        self.enabled = True
        self.buffer = deque(maxlen=5000)

    def push(self, msg_type, msg):
        self.buffer.append((msg_type, msg))

    def step(self):
        # template for math features
        # example: rate of change, rolling stats, spread, velocity
        pass


class SignalWorker:
    def __init__(self):
        self.enabled = True
        self.buffer = deque(maxlen=5000)

    def push(self, msg_type, msg):
        self.buffer.append((msg_type, msg))

    def step(self):
        # template for prediction / signal generation
        pass


class QuantEngine:
    def __init__(self):
        self.cluster_worker = ClusterWorker()
        self.math_worker = MathWorker()
        self.signal_worker = SignalWorker()

        self.running = True
        self.lock = Lock()
        self.threads = []

    def submit(self, msg_type, msg):
        self.cluster_worker.push(msg_type, msg)
        self.math_worker.push(msg_type, msg)
        self.signal_worker.push(msg_type, msg)

    def _cluster_loop(self):
        while self.running:
            self.cluster_worker.step()
            time.sleep(0.001)

    def _math_loop(self):
        while self.running:
            self.math_worker.step()
            time.sleep(0.001)

    def _signal_loop(self):
        while self.running:
            self.signal_worker.step()
            time.sleep(0.001)

    def start_threads(self):
        t1 = Thread(target=self._cluster_loop, daemon=True)
        t2 = Thread(target=self._math_loop, daemon=True)
        t3 = Thread(target=self._signal_loop, daemon=True)

        self.threads.extend([t1, t2, t3])

        for t in self.threads:
            t.start()

    def stop_threads(self):
        self.running = False


class QuantCore:
    def __init__(self, mp_q):
        self.mp_q = mp_q

        self.graphs_render = GraphsRender()
        self.scatter3d = Scatter3D()
        self.engine = QuantEngine()

        self.trade_count = 0
        self.quote_count = 0
        self.last_msg = None

    def on_stock_trade(self, msg):
        self.trade_count += 1
        self.last_msg = ("stock_trade", msg)

        self.graphs_render.update("stock_trade", msg)
        self.scatter3d.update("stock_trade", msg)
        self.engine.submit("stock_trade", msg)

    def on_stock_quotes(self, msg):
        self.quote_count += 1
        self.last_msg = ("stock_quotes", msg)

        self.graphs_render.update("stock_quotes", msg)
        self.scatter3d.update("stock_quotes", msg)
        self.engine.submit("stock_quotes", msg)

    def dispatch(self, msg_type, msg):
        if msg_type == "stock_trade":
            self.on_stock_trade(msg)

        elif msg_type == "stock_quotes":
            self.on_stock_quotes(msg)

        # elif msg_type == "option_trade":
        #     ...
        # elif msg_type == "option_quote":
        #     ...

    def run_forever(self):
        print("QuantCore PID:", os.getpid())
        self.engine.start_threads()

        try:
            while True:
                try:
                    msg_type, msg = self.mp_q.get(timeout=1.0)
                    self.dispatch(msg_type, msg)
                except Empty:
                    pass

        except KeyboardInterrupt:
            self.engine.stop_threads()


def run(mp_q):
    qc = QuantCore(mp_q)
    qc.run_forever()