import multiprocessing
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

def run_multiprocessing(num_processes, n):
    processes = []
    start_time = time.perf_counter()

    for _ in range(num_processes):
        p = multiprocessing.Process(target=cpu_bound_task, args=(n,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.perf_counter()
    return end_time - start_time

if __name__ == "__main__":
    N = 50000
    PROCESSES = [1, 2, 4, 8]

    print("=== MULTIPROCESSING TEST ===")
    print(f"PID: {os.getpid()}")

    for p in PROCESSES:
        exec_time = run_multiprocessing(p, N)
        print(f"Processes: {p}, Execution Time: {exec_time:.4f} seconds")
