from multiprocessing import Process, cpu_count
import math
import time


def find_primes(n):
    """
    CPU-bound task: menghitung bilangan prima hingga n
    """
    primes = []

    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)

    print(f"Found {len(primes)} primes up to {n}")
    return len(primes)


if __name__ == "__main__":
    n = 1_000_000
    num_processes = cpu_count()
    print(num_processes)

    # ======================
    # Sequential execution
    # ======================
    start = time.time()
    result_seq = find_primes(n)
    # for _ in range(num_processes):
        
    
    print(f"Sequential time: {time.time() - start:.2f}s\n")

    # ======================
    # Multiprocessing execution
    # ======================
    processes = []
    start = time.time()

    # chunk_size = n // num_processes
    chunk_size = 1_000_000

    for _ in range(3):
        p = Process(target=find_primes, args=(chunk_size,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"Multiprocess time: {time.time() - start:.2f}s")
