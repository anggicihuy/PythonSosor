import threading
import time
import psutil
import os

def cpu_bound_task(n):
    count = 0
    for i in range(2, n):
        prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                prime = False
                break
        if prime:
            count += 1
    return count

def run_threading(num_threads, n):
    threads = []
    start_time = time.perf_counter()

    for _ in range(num_threads):
        t = threading.Thread(target=cpu_bound_task, args=(n,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.perf_counter()
    return end_time - start_time

if __name__ == "__main__":
    N = 50000   # ukuran workload
    THREADS = [1, 2, 4, 8]

    print("=== THREADING TEST ===")
    print(f"PID: {os.getpid()}")

    for t in THREADS:
        exec_time = run_threading(t, N)
        print(f"Threads: {t}, Execution Time: {exec_time:.4f} seconds")


