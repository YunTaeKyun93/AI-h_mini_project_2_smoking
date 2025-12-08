import time
import os
import psutil

LOG_FILE = "logs/etl.log"

def log(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    full = f"{timestamp} {message}"
    print(full)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full + "\n")

def memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    return round(mem, 2)
