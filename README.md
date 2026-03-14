jupyter nbconvert --to python *.ipynb

Big szie ask and bids that are close together 

Highing bar math : brushes = [pg.mkBrush(200, 50, 50) if val > threshold else pg.mkBrush(50, 120, 200)
           for val in y]

           Mi​=Mi−1​e−Δt/τ+ri​(1−e−Δt/τ)


```python
import math

class FlowMomentum:
    def __init__(self, tau=1.0, k=0.0005, eps_dt=1e-3):
        self.tau = tau      # seconds of memory
        self.k = k          # scale for countdown
        self.eps_dt = eps_dt

        self.t_prev = None
        self.M = 0.0        # momentum state (smoothed rate)
        self.E = 0.0        # countdown / hold state

    def update(self, t, dv):
        """
        t: timestamp (seconds, float)
        dv: incoming volume (shares) since last update (often trade size)
        returns: (rate, M, E)
        """
        if self.t_prev is None:
            self.t_prev = t
            return 0.0, self.M, self.E

        dt = max(t - self.t_prev, self.eps_dt)
        r = dv / dt  # shares/sec

        decay = math.exp(-dt / self.tau)
        # leaky integrator / EMA with irregular dt
        self.M = self.M * decay + r * (1 - decay)

        # countdown hold
        self.E = max(self.E - dt, self.k * self.M)

        self.t_prev = t
        return r, self.M, self.E








last_price = None
last_time = None
last_size = None 

def update(q):
    global last_price, last_time

    Pnow = q["s"]
    ts = q["t"]
    Tnow = ts.seconds + ts.nanoseconds * 1e-9

    if last_price is not None:
        dt = Tnow - last_time
        if dt > 0:
            rate = (Pnow - last_price) / dt
            
           # test.rate = rate
            
    last_price = Pnow
    last_time = Tnow



from multiprocessing import Process, Queue
from collections import deque

from realtime import run as run_realtime
from graphs import run as run_graphs

def hub(q_in, outs, maxlen=50000):
    history = deque(maxlen=maxlen)  # local to hub (not shared)
    while True:
        msg = q_in.get()            # blocks
        history.append(msg)

        # broadcast: each subscriber gets its own copy
        for q_out in outs:
            try:
                q_out.put_nowait(msg)
            except Exception:
                pass

def main():
    q_in = Queue(maxsize=50000)

    q_graph = Queue(maxsize=50000)
    q_log   = Queue(maxsize=50000)   # example second copy

    p1 = Process(target=run_realtime, args=(q_in,))
    pH = Process(target=hub, args=(q_in, [q_graph, q_log]))
    p2 = Process(target=run_graphs, args=(q_graph,))

    p1.start(); pH.start(); p2.start()

    try:
        p1.join(); pH.join(); p2.join()
    except KeyboardInterrupt:
        for p in (p1, pH, p2):
            p.terminate()

if __name__ == "__main__":
    main()





    | Attribute              | Purpose                                 |
| ---------------------- | --------------------------------------- |
| `labels_`              | cluster id per point                    |
| `probabilities_`       | cluster confidence                      |
| `cluster_persistence_` | cluster stability                       |
        cluster 0 → 0.92   (very dense)
        cluster 1 → 0.41   (weak density)
        cluster 2 → 0.73
| `outlier_scores_`      | anomaly score                           |
| `n_clusters_`          | number of clusters                      |
| `prediction_data_`     | allows predicting clusters for new data |



| parameter          | what it controls      |
| ------------------ | --------------------- |
| `min_samples`      | density strictness    |
| `min_cluster_size` | smallest cluster size |
| `metric`           | distance calculation  |















