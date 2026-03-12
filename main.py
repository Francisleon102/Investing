from multiprocessing import Process, Queue, Value
from collections import deque
import subprocess
from realtime import run as run_realtime
from graphs import run as run_graphs
from pulseUnit import run as run_quantcore


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


_sleep_proc = None

def prevent_sleep():
    global _sleep_proc
    _sleep_proc = subprocess.Popen([
        "systemd-inhibit",
        "--what=sleep",
        "--why=live market streaming",
        "sleep:idle",
        "infinity"
    ])


def main():
    prevent_sleep()

    q_in        = Queue(maxsize=50000)
    q_graph     = Queue(maxsize=50000)
    q_quantcore = Queue(maxsize=50000)
    q_log       = Queue(maxsize=50000)
    pU_rate     = Value('d', 0.0)

    p1 = Process(target=run_realtime, args=(q_in,))
    pH = Process(target=hub, args=(q_in, [q_graph, q_quantcore, q_log]))
    p2 = Process(target=run_graphs, args=(q_graph,pU_rate))
    p3 = Process(target=run_quantcore, args=(q_quantcore,pU_rate))

    p1.start(); pH.start(); p2.start(); p3.start()

    try:
        p1.join(); pH.join(); p2.join(); p3.join()
    except KeyboardInterrupt:
        for p in (p1, pH, p2, p3):
            p.terminate()


if __name__ == "__main__":
    main()