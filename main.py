from multiprocessing import Process, Queue
from realtime import run as run_realtime,StockData
from graphs import run as run_graphs

def main():
    q = Queue(maxsize=50000)
    p1 = Process(target=run_realtime, args=(q,))
    p2 = Process(target=run_graphs,  args=(q,))
    p3 = Process(target=z)

    p1.start()
    p2.start()

    try:
        p1.join()
        p2.join()
        p3.join()

    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
        p3.terminate()


def z():
    while True:
        if(StockData is not None):
            print(len(StockData))
        else:
            print("empty")
    


if __name__ == "__main__":
    main()
