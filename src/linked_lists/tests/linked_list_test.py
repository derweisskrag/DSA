import unittest
from typing import override

from src.linked_lists.linked_list.implementation.linked_list import LinkedList


class LinkedListTest(unittest.TestCase):
    @override
    def setUp(self):
        self.ll = LinkedList[int]()
        self.node1_data = 10
        self.node2_data = 20
        self.node1 = self.ll.add_to_front(self.node1_data)
        self.node2 = self.ll.add_to_front(self.node2_data)

    def test_find_by_data(self):
        found_node = self.ll.find_by_data(self.node1.data)
        self.assertEqual(found_node.data, 10)

        # with self.assertRaises(NodeNotFoundException):
        # self.ll.find_by_id(999)  # Assuming 999 is not a valid ID

    def test_find_by_id(self):
        # create a dummy linked list
        linked_list = LinkedList[int]()

        # populate the linked list
        node1 = linked_list.add_to_front(1)
        node2 = linked_list.add_to_front(2)
        node3 = linked_list.add_to_front(3)

        # retrieve them from the linked list
        found_node1 = linked_list.find_by_id(id(node1))
        found_node2 = linked_list.find_by_id(id(node2))
        found_node3 = linked_list.find_by_id(id(node3))

        # test the function
        self.assertEqual(found_node1.data, node1.data)
        self.assertEqual(found_node2.data, node2.data)
        self.assertEqual(found_node3.data, node3.data)

    def test_is_empty(self):
        self.assertFalse(self.ll.is_empty())
        empty_ll = LinkedList[int]()
        self.assertTrue(empty_ll.is_empty())

    def test_size(self):
        # create a linked list
        ll = LinkedList[int]()

        # let us some nodes
        a = ll.add_to_front(1)
        b = ll.add_to_front(2)

        # test the size
        self.assertEqual(ll.get_size(), 2)

        # also assert:
        self.assertEqual(self.ll.get_size(), 2)

    def test_remove_by_data(self):
        self.ll.remove_by_data(10)
        self.assertEqual(self.ll.size, 1)
        self.assertEqual(self.ll.find_by_data(10), None)

    def test_remove_by_id(self):
        node_id = self.node2.get_id()
        self.ll.remove_by_id(node_id)
        self.assertEqual(self.ll.size, 1)
        self.assertEqual(self.ll.find_by_id(node_id), None)

    def test_insert_node(self):
        # create dummy linked list
        ll = LinkedList[int]()
        # add some nodes
        a = ll.add_to_front(1)
        b = ll.add_to_front(2)
        c = ll.add_to_front(3)

        # now let us add another node to position = 2
        d = ll.insert_node(4, 2)  # data = 4, position = 2

        # the linked list is
        # 3 -> 2 -> 1
        # 0      1      2

        # so after insert_node
        # 3 -> 2 -> 4 -> 1

        # check that
        found_node_by_data = ll.find_by_data(2)  # search for node 2

        # make sure that its next is 4, and after is 1
        self.assertEqual(found_node_by_data.next.data, 4)
        self.assertEqual(found_node_by_data.next.next.data, 1)

        # check if exception is raised
        with self.assertRaises(TypeError) as context:
            self.ll.insert_node(5, "str")

        # check if the exception message is as expected
        self.assertEqual(str(context.exception),
                         f"Cannot insert the node into the linked list due to wrong"
                         f"specified type of 'position' argument: {type('str')}"
                         f"must be 'integer'.")


if __name__ == '__main__':
    unittest.main()
