import unittest
from typing import override

from src.trees.red_black_tree.implementation.red_black_tree import RBTree, Color


class RBTreeInitializationTest(unittest.TestCase):
    @override
    def setUp(self):
        # create a tuple test
        test_data = [(1, 15), (2, 35)]
        self.rbtree = RBTree[int](*test_data)

    def test_rbtree_creation(self):
        self.assertFalse(self.rbtree.is_empty(), "The Red-black tree should not be empty upon initialization with args")

    def test_tree_values(self):
        # at this point the tree is not rotated
        # because there is no rule violations
        # The structure is root -> node where
        # node's location depends on its key, because
        # the function "add" inserts nodes according to the key

        # For this test, I compare the root according to
        #   1. Color
        #   2. Key
        #   3. Value

        # get the root
        root = self.rbtree.get_root()

        # define the expected root node data
        # Notice! We have to define pointers too
        # if we were to compare the next
        expected_root = {
            "key": 1,
            "value": 15,
            "color": Color.BLACK,
            "left": None,
            "right": None,
            "parent": None,
        }

        # Define right child
        right_child = {
            "key": 2,
            "value": 35,
            "color": Color.RED,
            "left": None,
            "right": None,
            "parent": expected_root,
        }

        # Set the pointer
        expected_root["right"] = right_child

        # Now we can test

        # check values
        self.assertEqual(root.data, expected_root['value'], "Root is the node whose value is 15")
        self.assertEqual(root.right.data, right_child['value'], "The right child is Node(key=2, data=35)")

        # check keys
        self.assertEqual(root.key, expected_root['key'], "Root is the node whose key is 1")
        self.assertEqual(root.right.key, right_child['key'], "The key of the root's right child is 2")

        # Check the parent's reference:
        self.assertEqual(root.right.parent.data, expected_root['value'], "The parent of the right child is root")

        # Check if the left node from the root's perspective exists
        self.assertEqual(root.left, None, "We added only 2 nodes, so the third one is None")

        # test size
        self.assertEqual(self.rbtree.size, 2, "The size is 2, because there are 2 nodes in the tree")

    def test_colours(self):
        # get the root
        root = self.rbtree.get_root()

        # Check the colors
        self.assertEqual(root.color, Color.BLACK, "Root is always BLACK!")
        self.assertEqual(root.right.color, Color.RED, "New Node is RED if no balancing!")


if __name__ == "__main__":
    unittest.main()
