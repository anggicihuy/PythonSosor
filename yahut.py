import threading
import time
import requests


def fetch_url(url):
    """Simulate I/O-bound work: fetch data from URL"""
    start = time.time()
    response = requests.get(url)
    elapsed = time.time() - start
    print(f"Fetched {url} in {elapsed:.2f}s")
    return len(response.content)


if __name__ == "__main__":
    # Daftar URL (I/O-bound)
    urls = ["https://httpbin.org/delay/1"] * 5

    # ======================
    # Sequential execution
    # ======================
    start = time.time()
    results_seq = [fetch_url(url) for url in urls]
    print(f"Sequential time: {time.time() - start:.2f}s\n")

    # ======================
    # Multithreaded execution
    # ======================
    threads = []
    start = time.time()

    for url in urls:
        t = threading.Thread(target=fetch_url, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Threaded time: {time.time() - start:.2f}s")
