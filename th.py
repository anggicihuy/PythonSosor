import threading
import time
import os


def io_task(task_id, file_path):
    """
    Simulasi I/O-bound:
    - Membaca file
    - Delay I/O (disk / waiting)
    """
    start = time.time()

    with open(file_path, "r") as f:
        data = f.read()

    time.sleep(1)  # simulasi blocking I/O

    elapsed = time.time() - start
    print(f"Task {task_id} selesai dalam {elapsed:.2f}s")
    return len(data)


if __name__ == "__main__":
    FILE_PATH = "sample.txt"
    NUM_TASKS = 5

    # Buat file dummy (sekali saja)
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            f.write("Artificial Intelligence\n" * 100000)

    # ======================
    # Sequential execution
    # ======================
    start = time.time()
    for i in range(NUM_TASKS):
        io_task(i, FILE_PATH)
    print(f"Sequential time: {time.time() - start:.2f}s\n")

    # ======================
    # Multithreaded execution
    # ======================
    threads = []
    start = time.time()

    for i in range(NUM_TASKS):
        t = threading.Thread(target=io_task, args=(i, FILE_PATH))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Threaded time: {time.time() - start:.2f}s")
