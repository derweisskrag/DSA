import unittest
from typing import override

from src.trees.red_black_tree.implementation.red_black_tree import RBTree


class RBTreeInitializationTest(unittest.TestCase):
    @override
    def setUp(self):
        self.rbtree = RBTree()

    def test_rbtree_creation(self):
        self.assertTrue(self.rbtree.is_empty(), "The Red-black tree should be empty upon initialization")

    def test_empty_tree(self):
        self.assertEqual(self.rbtree.size, 0, "The size should be 0 when the Red-black tree is empty")
        self.assertEqual(self.rbtree.get_root(), self.rbtree.NIL_LEAF, "The root is None because nothing was added")


if __name__ == "__main__":
    unittest.main()
