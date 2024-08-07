from src.queues.circular_queue.implementation.circular_queue_linked_list import CircularQueue
from src.queues.queue.implementation.queue_list import Queue


def main():
    cq = CircularQueue()
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    cq.display()
    cq.peek()

    cq.dequeue()
    cq.display()
    cq.peek()

if __name__ == "__main__":
    main()
