from src.interfaces.priority_queue_interface import PriorityQueueInterface


class PriorityQueue(PriorityQueueInterface):
    pass

import heapq

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
    dpq = DynamicPriorityQueue()
    
    # Initial queue setup
    dpq.add_person("You", 1)
    dpq.add_person("Person Behind", 1)
    dpq.add_person("Person Ahead", 1)

    dpq.print_queue()

    # You step aside
    dpq.step_aside("You")
    dpq.print_queue()

    # Simulate ongoing motion
    print("Processing the queue in real-time:")
    for _ in range(3):
        dpq.process()
        dpq.print_queue()


if __name__ == "__main__":
    main()
