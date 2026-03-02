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
