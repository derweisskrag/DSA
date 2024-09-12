import unittest
from typing import override

from src.trees.red_black_tree.implementation.red_black_tree import RBTree, Color


class RBTreeInsertTest(unittest.TestCase):
    @override
    def setUp(self):
        self.rbtree = RBTree()

    def test_add_left_rotate(self):
        # add some node into the tree
        self.rbtree.add(1, 15)
        self.rbtree.add(2, 16)
        self.rbtree.add(3, 27)

        # Case 3. 1 - We just rotate left
        # on Grandparent and recolour:
        # P -> BLACK (parent)
        # G -> RED (grandparent)
        # K -> RED (new node)

        # get the root
        root = self.rbtree.get_root()

        # First check if the root is P (parent) of K
        self.assertDictEqual({
            "key": root.key,
            "value": root.data,
        }, {
            "key": 2,
            "value": 16
        }, "New root must be the parent (key: 2, value: 16)")

        # Checks its Color
        self.assertEqual(self.rbtree.get_root().color, Color.BLACK)

        # Check if the left child is indeed Grandparent (left-rotate result)
        self.assertDictEqual({
            "key": root.left.key,
            "value": root.left.data,
        }, {
            "key": 1,
            "value": 15,
        }, "The left child of new root is Grandparent (key: 1, value: 15)")

        # Check if the right child is inded K (new node)
        self.assertDictEqual({
            "key": root.right.key,
            "value": root.right.data,
        }, {
            "key": 3,
            "value": 27
        }, "The right child of new root is K (new node) with (key: 3, value: 27)")

        # Check colours
        self.assertEqual(root.left.color, Color.RED, "Grandparent is re-coloured to RED")
        self.assertEqual(root.right.color, Color.RED, "New node remains RED")

    def test_add_right_rotate(self):
        # test with negative key
        # WARN: Handle this case later
        self.rbtree.add(1, 15)
        self.rbtree.add(2, 16)
        self.rbtree.add(3, 27)
        self.rbtree.add(-1, 10)
        self.rbtree.add(0, 12)

        """
        Case: 3.1 mirror (rotate on Grandparent)
        
        Yes, this is a mirror case. However, it is starting 
        from another case that brings you to this case (3.1 mirror).
        
        In this case, you see the tree
                       
                       2
                      / \\
                     1   3
                     
        It is balanced (Colours are BLACK -> RED, RED). Interesting 
        that to test the right rotation, I don't need to add the key
        -1 and then 0, because adding (3, 2, 1) exactly triggers this 
        right rotation already (like in 1, 2, 3, you would right on G)
        
        Example:
            >>> rbtree = RBTree[int](3, 2, 1) # use args initialization 
        
        This tree is balanced, but before balance:
        
                        3                      2
                       /                      / \\
                      2        =>            1   3
                     /
                    1
                    
        The "=>" indicates right rotation on G (in this case, root). Please,
        notice that this process is repeated because we traverse the tree
        using "node = node.parent.parent", which means that after applying
        left rotation in the right subtree (from the perspective of the root)
        on the grandparent of the newly added node, tree may apply the same
        rotation on the root, because root is a grandparent for other nodes.
        
        Why this happens? This is more specific to our current test case.
        Let us see how the RBTree looks like when we add (1, 2, 3, -1, 0):
        
                     2
                    / \\
                   1   3
                  /
                 -1
                  \\
                   0
                   
        Notice that when inserting the node, we add them according to the key.
        So, this tree is clearly imbalanced. If you try to apply the left 
        rotation on the parent (-1) of the node (0), you get the following:
        
                    2                        2
                   / \\                     / \\
                  1   3                    0   3
                 /                        / \\
                0            =>        -1   1
               / 
             -1      
                
        The "=>" uses the mirror case of RR (LL), which is resolved by applying 
        the right rotation in this case. Subsequently, you can try to trigger the
        same pattern in the right subtree (from the root's perspective):
        
                  2
                 / \\
                1   4
                     \\
                      5
                     /
                    3
                    
        Please, notice that this is exactly the mirror case of the previous. You
        can indeed try to apply the right rotation on the parent, and then the left
        rotation on the grandparent, and please notice that we change the node here:
        
            >>> node = node.parent
            >>> self._right_rotate(node)
            >>> ... 
            
        Thanks for reading this explanation. It is really simple as long as you under-
        stand how left and right rotation works.              
        """

        # get the root for comparison
        root = self.rbtree.get_root()

        # Define the nodes involved in right rotation
        grandparent = root.left.right
        parent = root.left.left
        new_node = root.left

        # Test their data
        # Test Grandparent
        self.assertDictEqual({
            "key": grandparent.key,
            "value": grandparent.data,
        }, {
            "key": 1,
            "value": 15
        }, "Grandparent moved to the right (rotate right) (key: 1, value: 15)")

        # Test Parent
        self.assertDictEqual({
            "key": parent.key,
            "value": parent.data
        }, {
            "key": -1,
            "value": 10,
        }, "Parent is went to the left child of new node (key: -1, value: 10)")

        # Test new node
        self.assertDictEqual({
            "key": new_node.key,
            "value": new_node.data,
        }, {
            "key": 0,
            "value": 12,
        }, "New node is the parent of the Grandparent and Parent (key: 0, value: 12)")

    def test_insert_many(self):
        self.rbtree.add(1, 10)
        self.rbtree.add(2, 11)
        self.rbtree.add(3, 12)
        self.rbtree.add(4, 13)
        self.rbtree.add(5, 14)

        self.assertEqual(self.rbtree.get_root().right.key, 4)


if __name__ == "__main__":
    unittest.main()
