import unittest
from typing import override

from src.trees.red_black_tree.implementation.red_black_tree import RBTree, Color


class RBTreeLeafDeletionTest(unittest.TestCase):
    @override
    def setUp(self):
        self.rbtree = RBTree[int]((1, 15), (2, 27), (3, 11))

    def test_delete_leaf(self):
        """
        How trees looks before deletion:

                   2
                  /  \\
                 1   3

        After deletion only 1 nodes remains: the root (2).
        """

        deleted_node = self.rbtree.remove_node(key=1)
        delete_one_more = self.rbtree.remove_node(3)

        # check
        self.assertEqual(deleted_node.key, 1)
        self.assertEqual(delete_one_more.key, 3)

    def test_delete_predecessor(self):
        """
        How trees looks before deletion:

                   2
                  /  \\
                 1   4
                    / \\
                   3   5

        After deletion:

                  2
                 / \\
                1   3
                    \\
                     5

        What happened: Node to delete is 4. We find its predecessor
        and copy its value into parent, and make it doubly-black node.
        Then we remove it (if and only if its original color is BLACK).
        """

        # add more nodes
        self.rbtree.add(4, 25)
        self.rbtree.add(5, 20)

        # get the root
        root = self.rbtree.get_root()

        # try remove 4
        self.rbtree.remove_rb(4)

        self.rbtree.in_order_traversal(root)


if __name__ == "__main__":
    unittest.main()