import time
import threading
import multiprocessing as mp
import psutil
import cProfile
import pstats

def cpu_task(n):
       """Task CPU-bound: Hitung faktorial."""
       result = 1
       for i in range(1, n+1):
           result *= i
       return result

def io_task(filename):
       """Task I/O-bound: Baca file."""
       with open(filename, 'r') as f:
           data = f.read()
       return len(data)

def run_threading(num_workers, task_type, *args):
       """Jalankan dengan threading."""
       threads = []
       for _ in range(num_workers):
           if task_type == 'cpu':
               t = threading.Thread(target=cpu_task, args=args)
           else:
               t = threading.Thread(target=io_task, args=args)
           threads.append(t)
           t.start()
       for t in threads: t.join()

def run_multiprocessing(num_workers, task_type, *args):
       """Jalankan dengan multiprocessing."""
       processes = []
       for _ in range(num_workers):
           if task_type == 'cpu':
               p = mp.Process(target=cpu_task, args=args)
           else:
               p = mp.Process(target=io_task, args=args)
           processes.append(p)
           p.start()
       for p in processes: p.join()

def monitor_performance(func, *args):
       """Monitor dengan psutil dan profiler."""
       # Start monitoring
       start_cpu = psutil.cpu_percent(interval=1)
       start_mem = psutil.virtual_memory().percent
       start_time = time.time()

       # Profile eksekusi
       profiler = cProfile.Profile()
       profiler.enable()
       func(*args)
       profiler.disable()

       # End monitoring
       end_time = time.time()
       end_cpu = psutil.cpu_percent(interval=1)
       end_mem = psutil.virtual_memory().percent

       # Print hasil
       print(f"Execution Time: {end_time - start_time:.2f}s")
       print(f"CPU Usage: {end_cpu}%")
       print(f"Memory Usage: {end_mem}%")

       # Simpan profile stats
       stats = pstats.Stats(profiler)
       stats.sort_stats('cumulative').print_stats(10)  # Top 10 functions

if __name__ == "__main__":
       num_workers = 4  # Sesuaikan dengan CPU cores
       # Buat file dummy untuk I/O
       with open('test_file.txt', 'w') as f:
           f.write('x' * 10**6)  # 1MB file

       print("=== Threading CPU ===")
       monitor_performance(run_threading, num_workers, 'cpu', 10000)

       print("\n=== Multiprocessing CPU ===")
       monitor_performance(run_multiprocessing, num_workers, 'cpu', 10000)

       print("\n=== Threading I/O ===")
       monitor_performance(run_threading, num_workers, 'io', 'test_file.txt')

       print("\n=== Multiprocessing I/O ===")
       monitor_performance(run_multiprocessing, num_workers, 'io', 'test_file.txt')
   