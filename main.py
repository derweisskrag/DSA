# from dsa_kuuking.queues.priority_queue.implementation.priority_queue import PriorityQueue as Regina
# from dsa_kuuking.burmese_native import PriorityQueue as Sceriffa
# import time

# # Test Regina (Python)
# start = time.time()
# r = Regina()
# for i in range(10000):
#     r.enqueue(f"Task {i}", i)
# print(f"Regina (Python) 10k enqueues: {time.time() - start:.4f}s")

# # Test Sceriffa (Rust)
# start = time.time()
# s = Sceriffa()
# for i in range(10000):
#     s.push(i, f"Task {i}")
# print(f"Sceriffa (Rust) 10k enqueues: {time.time() - start:.4f}s")

# from dsa_kuuking.linked_lists.doubly_linked_list.implementation.doubly_linked_list import DoublyLinkedList

# dll = DoublyLinkedList()
# dll.add_to_end(1)
# dll.add_to_end(2)
# dll.add_to_end(3)
# dll.display()
# dll.insert_node(4, 1)
# dll.display()
# # assume it exists
# node_two = dll[2]
# dll.insert_before(node_two, 10)
# dll.display()

# node_ten = dll[2]
# dll.insert_after(node_ten, 20)
# dll.display()
# print("REVERSE")
# dll.display_backwards()

from dsa_kuuking.linked_lists.linked_list.implementation.linked_list import LinkedList

# ll = LinkedList()

# ll.add_to_front(1)
# ll.add_to_front(2)
# ll.add_to_front(3)
# ll.add_to_front(4)
# ll.add_to_front(5)
# ll.display()
# new_head = ll.reverse_order() # error?
# print(f"NEW HEAD: {new_head}")
# ll.display()
# print("LET'S TRY TRAVERSE USING NEW_HEAD")
# while new_head:
#     print(f"[TRAVERSING]: {new_head}")
#     new_head = new_head.next
# print("[TRARVERSIN]: Ended")

# TEST DEL_FIRST

# ll = LinkedList()
# ll.add_to_front(1)
# ll.add_to_front(2)
# ll.add_to_front(3)

# print("Before Pop:")
# ll.display() # Node(3) -> Node(2) -> Node(1)

# popped_node = ll.del_first()
# print(f"Popped Node Value: {popped_node.data}") # Should be 3

# print("After Pop:")
# ll.display() # Node(2) -> Node(1)

# TRY METHODS: compare_and_swap and del_first_this
ll = LinkedList()
ll.add_to_front(1)
ll.add_to_front(2)
print("Before compare_and_swap:")
ll.display() # Node(2) -> Node(1)
result = ll.compare_and_swap(2, 3)
print(f"compare_and_swap result: {result}") # Should be True
print("After compare_and_swap:")
ll.display() # Node(3) -> Node(1)

# Try del_first_this
print("Before del_first_this:")
ll.display() # Node(3) -> Node(1)
popped_node = ll.del_first_this()
print(f"del_first_this popped node value: {popped_node.data}") # Should be 3
print("After del_first_this:")
ll.display() # Node(1)

# zig cc -shared -o llist.dll llist.c

