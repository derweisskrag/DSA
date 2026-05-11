from dsa_kuuking.queues.priority_queue.implementation.priority_queue import PriorityQueue as Regina
from dsa_kuuking.burmese_native import PriorityQueue as Sceriffa
import time

# Test Regina (Python)
start = time.time()
r = Regina()
for i in range(10000):
    r.enqueue(f"Task {i}", i)
print(f"Regina (Python) 10k enqueues: {time.time() - start:.4f}s")

# Test Sceriffa (Rust)
start = time.time()
s = Sceriffa()
for i in range(10000):
    s.push(i, f"Task {i}")
print(f"Sceriffa (Rust) 10k enqueues: {time.time() - start:.4f}s")