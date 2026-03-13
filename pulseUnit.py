import os
import time
from queue import Empty, Full
from collections import deque
from threading import Thread, Lock
from cuml.cluster import  HDBSCAN, KMeans
import cuml.accel 

from queue import Full
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler
from polars import self_dtype 
import numpy as np

from collections import deque
from queue import Full
import numpy as np
from sklearn.preprocessing import StandardScaler

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
    def __init__(self, pU_rate):
        self.enabled = True

        self.maxlenght = 5000
        self.buffer = deque(maxlen=self.maxlenght)

        # fixed training window
        self.cluster_maxlen = 2000
        self.cluster_buffer = deque(maxlen=self.cluster_maxlen)

        self.pU_rate = pU_rate

        # last variables for derivatives
        self.last_price = None
        self.last_time = None
        self.last_size = None

        # smoothed flow
        self.M = 0.0
        self.tau = 1.0

        # clustering state
        self.scaler = None
        self.clusterer = None
        self.is_fitted = False

        # hdbscan params
        self.min_cluster_size = 25
        self.min_samples = 5

    def push(self, msg_type, msg):
        if msg is None:
            return

        self.buffer.append((msg_type, msg))

        if msg_type != "stock_trade":
            return

        new_size = msg.get("s")
        new_time = msg.get("t")
        new_price = msg.get("p")

        if new_size is None or new_time is None or new_price is None:
            return

        Tnow = new_time.seconds + new_time.nanoseconds * 1e-9

        if self.last_size is not None:
            dt = Tnow - self.last_time
            if dt > 0:
                # incoming volume
                dv = new_size

                # raw flow rate
                r = dv / dt

                # exponential decay
                decay = np.exp(-dt / self.tau)

                # momentum update
                self.M = self.M * decay + r * (1 - decay)

                try:
                    self.pU_rate.put_nowait((Tnow, self.M))
                except Full:
                    pass

                # features for clustering
                # use dt, not raw timestamp, so labels are more meaningful
                self.cluster_buffer.append([self.M, new_price, dt])

                print("M (smoothed rate):", self.M, new_price, Tnow)

        self.last_size = new_size
        self.last_time = Tnow
        self.last_price = new_price

    def fit_clusters(self):
        if len(self.cluster_buffer) < self.min_cluster_size:
            return None

        X = np.asarray(self.cluster_buffer, dtype=np.float32)

        self.scaler = StandardScaler()
        Xs = self.scaler.fit_transform(X)

        self.clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            prediction_data=True
        )

        self.clusterer.fit(Xs)
        self.is_fitted = True

        return {
            "labels": self.clusterer.labels_,
            "probabilities": self.clusterer.probabilities_,
            "outlier_scores": self.clusterer.outlier_scores_,
            "n_clusters": len(set(self.clusterer.labels_)) - (1 if -1 in self.clusterer.labels_ else 0),
            "n_noise": int(np.sum(self.clusterer.labels_ == -1)),
        }

    def predict_latest(self):
        if not self.is_fitted or self.clusterer is None or self.scaler is None:
            return None

        if len(self.cluster_buffer) == 0:
            return None

        x_new = np.asarray([self.cluster_buffer[-1]], dtype=np.float32)
        x_new_scaled = self.scaler.transform(x_new)

        labels, strengths = hdbscan.approximate_predict(self.clusterer, x_new_scaled)

        return {
            "point": self.cluster_buffer[-1],
            "label": int(labels[0]),
            "strength": float(strengths[0]),
        }

    def step(self):
        if not self.enabled:
            return None

        # fit once so labels stay consistent
        if not self.is_fitted:
            return self.fit_clusters()

        # after fitting, only predict new points
        return self.predict_latest()
        

class MathWorker:
    def __init__(self):
        self.enabled = True
        self.buffer = deque(maxlen=5000)

    def push(self, msg_type, msg):
        self.buffer.append((msg_type, msg))
        #print(self.buffer)
      
     

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
    def __init__(self,pU_rate):
        self.cluster_worker = ClusterWorker(pU_rate)
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
    def __init__(self, mp_q, pU_rate):
        self.mp_q = mp_q
        self.pU_rate = pU_rate

        self.graphs_render = GraphsRender()
        self.scatter3d = Scatter3D()
        self.engine = QuantEngine(self.pU_rate)

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
        print("PulseUnit PID:", os.getpid())
        self.engine.start_threads()

        try:
            while True:
                try:
                    msg_type, msg = self.mp_q.get(timeout=0.5)
                    self.dispatch(msg_type, msg)
                  
                except Empty:
                    
                    pass

        except KeyboardInterrupt:
            self.engine.stop_threads()


def run(mp_q,pU_rate):
    qc = QuantCore(mp_q,pU_rate)
    qc.run_forever()
