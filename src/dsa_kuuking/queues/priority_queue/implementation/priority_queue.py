from dsa_kuuking.interfaces.priority_queue_interface import PriorityQueueInterface
from dsa_kuuking.linked_lists.doubly_linked_list.implementation.doubly_linked_list import DoublyLinkedList
from datetime import datetime
import heapq
from bisect import insort
from typing import Tuple

class PriorityQueue[T]:
    def __init__(self):
        self.queue: DoublyLinkedList[Tuple[int, T]] = DoublyLinkedList()

    def enqueue(self, item: T, priority: int):
        """Add an item to the queue with a given priority."""
        # Insert the item in the correct position based on its priority
        current = self.queue._head
        while current and current.data[0] <= priority:
            current = current.next
        if current:
            self.queue.insert_before(current, (priority, item))
        else:
            self.queue.add_to_end((priority, item)) # will create our first node

    def dequeue(self) -> T:
        """Remove and return the item with the highest priority (lowest priority number)."""
        if self.queue.is_empty():
            raise IndexError("Dequeue from an empty priority queue")
        return self.queue.remove_head().data[1]  # Return the item, not the priority
    
    def peek(self) -> T:
        """Return the item with the highest priority without removing it from the queue."""
        if self.queue.is_empty():
            raise IndexError("Peek from an empty priority queue")
        return self.queue._head.data[1]  # Return the item, not the priority
    
    def is_empty(self) -> bool:
        """Check if the priority queue is empty."""
        return self.queue.is_empty()
    
    def print_queue(self):
        """Print the contents of the queue for debugging purposes."""
        print("Priority Queue Contents:")
        current = self.queue._head
        # Also: self.queue.display() is available
        # but messy since this one handle both print 
        # but we can do it too
        for _, node in enumerate(self.queue.traverse()):
            priority, item = node.data
            print(f" - {item} (Priority: {priority})")

    def __len__(self):
        """Return the number of items in the priority queue."""
        # alternatively: return self.queue.size
        return len(self.queue) # Yes becuase our dll implements this too 
    
    def __str__(self):
        """Return a string representation of the priority queue."""
        return " -> ".join([f"{node.data[1]} (P: {node.data[0]})" for _, node in enumerate(self.queue.traverse())])
    
    def __repr__(self):
        """Detailed representation for developers."""
        items = [node.data for node in self.queue.traverse()]
        return f"PriorityQueue({items})"

    def __iter__(self):
        """Allow iteration over the items in the priority queue."""
        for node in self.queue.traverse():
            yield node.data[1]  # Yield the item, not the priority
    
    def clear(self):        
        """Remove all items from the priority queue."""
        self.queue.clear()

    def change_priority(self, item: T, new_priority: int):
        """Change the priority of an existing item in the queue."""
        current = self.queue._head
        while current:
            priority, current_item = current.data
            if current_item == item:
                # Remove the item and reinsert it with the new priority
                self.queue.remove_by_data(current.data)
                self.enqueue(item, new_priority)
                return
            current = current.next
        raise ValueError("Item not found in the priority queue")

    def migrate_to_rust(self):
        """The Burmese Eating Protocol."""
        try:
            from burmese_native import PriorityQueue as RustPQ
            rust_pq = RustPQ()
            
            # Batch collect the data
            # We extract (priority, item) tuples
            for node in self.queue.traverse():
                priority, item = node.data
                rust_pq.push(priority, item)
                
            # Swap the engines
            self.engine = "RUST"
            self.native_queue = rust_pq
            
            # Nuke the old swamp to save memory
            self.queue.clear() 
            return True
        except ImportError:
            print("Burmese Native module not found. Build the crate first!")
            return False

class PriorityQueueDatetime:
    """A simple implementation of a priority queue using a list and datetime for priority.
    
    In this implementation, each item is stored as a tuple of (datetime, item), and the queue is sorted based on the datetime to ensure that items with earlier timestamps are processed first.
    """

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """Add an item to the queue with the current datetime as its priority."""
        # Sort the queue based on datetime to maintain the priority order
        # Using insort is better than sort after every insertion for efficiency
        insort(self.queue, (datetime.now(), item), key=lambda x: x[0])  # Sort by datetime


    def dequeue(self):
        """Remove and return the item with the highest priority (earliest datetime)."""
        if not self.queue:
            raise IndexError("Dequeue from an empty priority queue")
        return self.queue.pop(0)[1]  # Return the item, not the datetime
    
    def peek(self):
        """Return the item with the highest priority without removing it from the queue."""
        if not self.queue:
            raise IndexError("Peek from an empty priority queue")
        return self.queue[0][1]  # Return the item, not the datetime
    
    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self.queue) == 0
    
    def print_queue(self):
        """Print the contents of the queue for debugging purposes."""
        print("Priority Queue Contents:")
        for priority, item in self.queue:
            print(f" - {item} (Priority: {priority})")


class DynamicPriorityQueue:
    def __init__(self):
        self.queue = []
        self.time = 0  # Simulates the ongoing nature of the system

    def add_person(self, name, priority):
        # Add a person to the queue with their initial priority
        heapq.heappush(self.queue, (priority, self.time, name))
        self.time += 1  # Increment time to track order of addition

    def step_aside(self, name):
        # Simulate stepping aside and rejoining with a lower priority
        print(f"{name} steps aside to help someone!")
        for i, (_, _, person) in enumerate(self.queue):
            if person == name:
                # Reduce priority and update
                _, time, person = self.queue.pop(i)
                heapq.heappush(self.queue, (2, time, person))  # Lower priority to 2
                break

    def process(self):
        # Continuously process the highest-priority person
        if self.queue:
            priority, _, person = heapq.heappop(self.queue)
            print(f"{person} with priority {priority} keeps moving forward!")

    def print_queue(self):
        print("\nCurrent Queue:")
        for priority, _, name in sorted(self.queue):
            print(f" - {name} (Priority {priority})")
        print()

# Simulating your dream
def main():
    pq = PriorityQueue()
    pq.enqueue("Person A", 1)
    pq.enqueue("Person B", 2)
    pq.enqueue("Person C", 3)
    pq.print_queue()
    pq.dequeue()
    pq.print_queue()
    pq.change_priority("Person C", 1)
    pq.print_queue()
    pq.clear()
    pq.print_queue()


if __name__ == "__main__":
    main()
