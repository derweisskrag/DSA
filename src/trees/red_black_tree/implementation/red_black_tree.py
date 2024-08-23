from typing import Optional, Tuple, Union, override

from src.linked_lists.types.ResultType import ResultType
from src.trees.enums.rbtree_colours import Color
from src.trees.red_black_tree.interface.red_black_tree_interface import RBTreeInterface
from src.trees.types.red_black_tree_node import NIL, Node

"""
This module contains the Red-black tree implementation
"""

"""
INSERT

    Denote Nodes:
        New node - K
        Parent - P ('parent')
        Uncle - U (Defined as 'parent.parent.left')
        Sibling - S ('parent.left' or 'parent.right' depending on K's location)
        Grandparent - G ('parent.parent')

    case 1: Tree is empty: create new root and colour it to be black.
    case 2: If K's parent is Black - Ok.
    case 3: K's P is RED: property 4 is violated: new node and parent are RED
    the G must be BLACK node because the tree before insertion must be a
    valid red-black tree. To resolve this case, we need to check if new node uncle is
    RED or BLACK.
        case 3.1: Uncle is RED too (P=RED, U=RED). We have to flip the colours of
        P, G and U. That means, P becomes Black, U becomes Black and G becomes RED.
        Conclusion: Re-colour.
        Edge Case at 3.1: If G is a root, we don't colour it RED (root is never RED).
    
        case 3.2: P is RED and U is either BLACK or None (NIL). This is more complicated
        than the previous case. If the Uncle (U) is BLACK, we need single double tree
        rotations depending upon whether K is a left or right child of P.
            case 3.2.1: P is the right child of G and K is right child of P:
            Example plot:
                2 (Black) = Root                     2 (Black)
              /  \\                                 /   \\
        1 (Black) 4 (Black) = G   --->       1 (Black)  5 (Red) = Make Black
                /  \\                                   / \\
          3 (Black) 5 (Red) = P            Make Red:  4 (Black) 6 (Red)
          This is U  \\                              /
                 /    6 (Red) This is K         None
        S: sibling is None
    
            First, we perform the left-rotation at G that makes G to be S of K. Next, we change
            the colour of S to RED and P's to BLACK.
            Case 3.2.2: P is right child of G and K is the left child of P. In this case, we
            have to right-rotation at P. This reduces it to the case 3.2.1. We next use the rules
            given in 3.2.1 to fix the tree.
            Case 3.2.3: P is the left child of G and K is the left child of P. This is the mirror of
            the case 3.2.1 (solution is symmetric to 3.2.1 - Apply Right-rotation and re-colour).
            Case 3.2.4: P is the left child of G and K is the right child of P. This is mirror of the
            case 3.2.2. Therefore, we have to apply left-rotation, and then right-rotation (3.2.2).
                
               
REMOVE NODE 
                
    x - node to delete
    S - Sibling
    G - Grandparent
    P - Parent
    
    The first step is to follow BST deletion process. Then we fix the balance.
    
    Case 1: x is a RED node. In this case, we simply delete x, because the removal
    of a red nodes doesn't violate the rules.
    Case 2: x has a RED child. We replace x by its child and change the colour of
    the child to RED. This way, we retain the property 5 (Every path from root to leaf
    must be equal for BLACK Nodes).
    Case 3: x is a BLACK node. Deleting a BLACK node violates the aforementioned rule.
    So, we add an extra BLACK node to the deleted node and call it a "double black" node.
    Now we need to convert this "double black node" into the BLACK node. For this, we consider
    the following 8 cases in total (4 are mirror).
    
    Case 3.1: x's S is RED. In this case, we switch the colours of S and 'x.parent', and then
    perform the left rotation on 'x.parent'. This reduces the case 3.1 to case 3.2, 3.3 or 3.4
    
    Case 3.2: x's S is BLACK, and both children of S are BLACK. The color of x's parent can
    be BLACK or RED. We switch the colour of S to RED. If the colour of x's parent is RED, we switch
    its colour to BLACK and this becomes terminal case. Otherwise, we make x's parent a new x and repeat
    the process from case 3.1.
    
    Case 3.3: x's S is BLACK, and S's left child is RED, and the right child of S is BLACK. We can
    switch the colours of S and its left child 'S.left' and then perform right rotation on S without
    violating any of the red-black properties. This transforms the tree into 3.4 case.
    
    Case 3.4: x's S is BLACK, and S's right child is RED. This is the terminal case. We change the colour
    of S's right child to BLACK, 'x.parent' colour to BLACK, x' S to RED and then perform the left rotation on the x's
    parent node. This way, we remove the extra black node on x.
    X is the node to removed, but target was x.parent. We just copy value it into parent.
"""


class RBTree[T](RBTreeInterface):
    def __init__(self, *args: Optional[Tuple[T]]) -> None:
        self._root = None

        if len(args) >= 1:
            for key, value in args:
                self.add(key, value)

    @override
    def add(self, key: T, value: T) -> None:
        # create new node
        new_node = Node(key, value)

        match self._root:
            case _ if self._root is None:
                # create new root
                self._root = new_node

                # re-colour
                self._root.color = Color.BLACK
            case _ if self._root is not None:
                # find the spot and insert
                new_node = self._insert(new_node)

                if not new_node.parent.parent:
                    return None

                self._fix_insert(new_node)

    def _insert(self, node: Node[T]) -> Node[T]:
        current = self._root
        parent = None
        while not isinstance(current, NIL):
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent

        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        return node

    def remove_copilot(self, key: T) -> Optional[Node[T]]:
        """
        Just like BST removal

        Returns
            Node_to_remove (Node[T]) - removed node
        """

        node_to_delete = self.find_by_key(key)

        if node_to_delete is None:
            return None

        removed_color = node_to_delete.color
        child = None

        if self.is_leaf(node_to_delete):
            parent = node_to_delete.parent
            if node_to_delete == node_to_delete.parent.left:
                parent.left = NIL()
            elif node_to_delete == node_to_delete.parent.right:
                parent.right = NIL()
            node_to_delete.parent = None
        elif isinstance(node_to_delete.left, NIL) or isinstance(node_to_delete.right, NIL):
            # node to removed has exactly one child
            child = node_to_delete.left if self.node_exists(node_to_delete.left) else node_to_delete.right
            self.transplant(node_to_delete, child)
        else:
            # has both children
            # find the largest left child of the node to delete
            predecessor = self.predecessor(node_to_delete)
            removed_color = predecessor.color

            # Transplant predecessor with its left child
            if predecessor.parent != node_to_delete:
                self.transplant(predecessor, predecessor.left)
                predecessor.left = node_to_delete.left
                predecessor.left.parent = predecessor

            # Transplant node_to_delete with predecessor
            self.transplant(node_to_delete, predecessor)
            predecessor.right = node_to_delete.right
            predecessor.right.parent = predecessor

            # Copy predecessor's key and value to node_to_delete
            node_to_delete.key = predecessor.key
            node_to_delete.value = predecessor.value

            # fix the color
            predecessor.color = Color.BLACK

        if removed_color == Color.BLACK:
            print("Gotta fix the tree!")

        return child

    @override
    def remove(self, key: T) -> Optional[Node[T]]:
        """
        Just like BST removal

        Returns
            Node_to_remove (Node[T]) - removed node
        """

        node_to_delete = self.find_by_key(key)

        if node_to_delete is None:
            return None

        removed_color = node_to_delete.color
        child = None

        if self.is_leaf(node_to_delete):
            parent = node_to_delete.parent
            if node_to_delete == node_to_delete.parent.left:
                parent.left = NIL()
            elif node_to_delete == node_to_delete.parent.right:
                parent.right = NIL()
            node_to_delete.parent = None
        elif isinstance(node_to_delete.left, NIL) or isinstance(node_to_delete.right, NIL):
            # node to removed has exactly one child
            child = node_to_delete.left if self.node_exists(node_to_delete.left) else node_to_delete.right
            self.transplant(node_to_delete, child)
        else:
            # has both children
            # find the largest left child of the node to delete
            predecessor = self.predecessor(node_to_delete)
            node_to_delete.key = predecessor.key
            node_to_delete.value = predecessor.value
            removed_color = predecessor.color

            child = self.get_node_or_mock(predecessor)
            self.transplant(predecessor, child)

        if removed_color == Color.BLACK:
            print("Gotta fix the tree!")

        return child

    def remove_node_alek_os(self, key: T) -> Optional[Node[T]]:
        node_to_delete = self.find_by_key(key)

        if node_to_delete is None:
            return None

        removed_color = node_to_delete.color
        child = None
        if self.count_children(node_to_delete) < 2:
            child = self.get_node_or_mock(node_to_delete)
            self.transplant(node_to_delete, child)
        else:
            min_node = self._min(node_to_delete.right)
            node_to_delete.key = min_node.key
            node_to_delete.value = min_node.value
            removed_color = min_node.color
            child = self.get_node_or_mock(min_node)
            self.transplant(min_node, child)

        if removed_color == Color.BLACK:
            print("Gotta fix the rules, bro!")

        return child

    def _fix_insert(self, node: Node[T]) -> None:
        while node != self._root and node.parent.color == Color.RED:
            uncle = self.find_uncle(node)
            match uncle.color:
                case Color.RED:
                    # Case 3.1
                    # Re-colour:
                    """
                        P -> Black
                        U -> Black
                        G -> RED
                    """
                    node.parent.parent.color = Color.RED
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK

                    # move to the next iteration
                    node = node.parent.parent
                case Color.BLACK:
                    # Cases 3.2.1-3.2.4
                    if node == node.parent.right and node.parent == node.parent.parent.left:
                        # left-right case
                        self._left_rotate(node.parent)
                        node = node.left
                    elif node == node.parent.left and node.parent == node.parent.parent.right:
                        # right-left case
                        self._right_rotate(node.parent)
                        node = node.right

                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED

                    if node == node.parent.left:
                        self._right_rotate(node.parent.parent)
                    else:
                        self._left_rotate(node.parent.parent)

                case _:
                    break

        self._root.color = Color.BLACK

    def _fix_remove(self, node: Node[T]) -> None:
        while node != self._root and node.color == Color.BLACK:
            if node == node.parent.left:
                sibling = node.parent.right

                # case 3. 1
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                if sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    # Case 3. 2
                    # both children are black
                    # color sibling to red
                    sibling.color = Color.RED

                    # move in the loop (to next iteration)
                    node = node.parent
                else:
                    if sibling.right.color == Color.BLACK:
                        # Case 3. 3
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._right_rotate(sibling)

                        # update sibling
                        sibling = node.parent.right

                    # Case 3. 4
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self._left_rotate(node.parent)

                    node = self.root
            else:
                sibling = node.parent.left

                # case 3. 1
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left

                if sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    # Case 3. 2
                    # both children are black
                    # color sibling to red
                    sibling.color = Color.RED

                    # move in the loop (to next iteration)
                    node = node.parent
                else:
                    if sibling.left.color == Color.BLACK:
                        sibling.color = Color.RED
                        sibling.right.color = Color.BLACK
                        self._left_rotate(sibling)
                        sibling = node.parent.left

                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self._right_rotate(node.parent)
                    node = self.root

        self._root.color = Color.BLACK

    def _left_rotate(self, node: Node[T]) -> None:
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not NIL:
            right_child.left.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self._root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    def _right_rotate(self, node: Node[T]) -> None:
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self._root = left_child
        elif node == node.parent.left:
            node.parent.left = left_child
        else:
            node.parent.right = left_child

        left_child.right = node
        node.parent = left_child

    def transplant(self, u: Node[T], v: Union[NIL, Node[T]]) -> None:
        if u.parent is None:
            self._root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        u.parent = v.parent

    @staticmethod
    @override
    def node_exists(node: Union[Node[T], NIL]) -> bool:
        return not isinstance(node, NIL)

    @override
    def count_children(self, node: Node[T]) -> int:
        return 2 if self.node_exists(node.left) and self.node_exists(node.right) else \
            1 if self.node_exists(node.left) or self.node_exists(node.right) else 0

    @override
    def get_node_or_mock(self, node: Node[T]) -> Optional[Union[NIL, Node[T]]]:
        return node.left if self.node_exists(node.left) else node.right

    @staticmethod
    def _min(node: Union[NIL, Node[T]]) -> Node[T]:
        parent = None
        while not isinstance(node, NIL):
            parent = node.parent
            node = node.left

        return parent.right

    @staticmethod
    def _max(node: Union[NIL, Node[T]]) -> Node[T]:
        parent = None
        while not isinstance(node, NIL):
            parent = node.parent
            node = node.right

        return parent.left

    @override
    def predecessor(self, node: Union[NIL, Node[T]]) -> Node[T]:
        match node.left:
            case _ if isinstance(node, NIL):
                parent = node.parent
                while parent is not None and node == node.parent.left:
                    node = parent
                    parent = parent.parent

                return parent
            case _ if not isinstance(node, NIL):
                return self._max(node.left)

    @override
    def successor(self, node: Union[NIL, Node[T]]) -> Node[T]:
        match node.right:
            case _ if isinstance(node, NIL):
                parent = node.parent
                while parent is not None and node == node.parent.right:
                    node = parent
                    parent = parent.parent

                return parent
            case _ if not isinstance(node, NIL):
                return self._min(node.right)

    @override
    def in_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
        if not isinstance(node, NIL):
            self.in_order_traverse(node.left)
            print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")
            self.in_order_traverse(node.right)

    @override
    def pre_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
        if not isinstance(node, NIL):
            print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")
            self.in_order_traverse(node.left)
            self.in_order_traverse(node.right)

    @override
    def post_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
        if not isinstance(node, NIL):
            self.in_order_traverse(node.left)
            self.in_order_traverse(node.right)
            print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")

    @override
    def swap(self, u: Node[T], v: Node[T]) -> None:
        ...

    @override
    def find_by_key(self, key: T) -> Optional[Node[T]]:
        try:
            current = self.root

            if key == current.key:
                return current

            parent = None
            while not isinstance(current, NIL):
                parent = current.parent

                if key < current.key:
                    current = current.left
                else:
                    current = current.right

            if parent is None:
                return None

            if key < parent.key:
                return parent.left
            elif key > parent.key:
                return parent.right
            else:
                return parent
        except ValueError as e:
            print(f"Error occurred: {e!s}")

    @staticmethod
    def find_uncle(node: Node[T]) -> Union[NIL, Node[T]]:
        if not (node.parent and node.parent.parent):
            raise Exception("No parent and grandparent exist for this node!")

        if node.parent == node.parent.parent.left:
            return node.parent.parent.right

        return node.parent.parent.left

    def find_sibling(self, node: Node[T]) -> Union[NIL, Node[T]]:
        ...

    @property
    def root(self) -> Node[T]:
        match self.get_root():
            case result if result.is_ok():
                return result.unwrap()
            case error if result.is_error():
                raise Exception(error.unwrap_err())
            case _:
                raise Exception("Other error")

    def get_root(self) -> ResultType[Node[T], str]:
        """Retrieves the root"""
        match self._root:
            case root if not isinstance(root, NIL):
                return ResultType(value=root)
            case nil if isinstance(nil, NIL):
                return ResultType(error=f"The root doesn't exist")

    @override
    def is_empty(self) -> bool:
        return self.root is NIL

    @staticmethod
    @override
    def is_leaf(node: Union[Node[T], NIL]) -> bool:
        # has no children
        return isinstance(node.left, NIL) and isinstance(node.right, NIL)


def main():
    rb = RBTree[int]()
    rb.add(key=1, value=15)
    rb.add(key=2, value=13)
    rb.add(key=3, value=16)
    rb.add(key=4, value=19)
    rb.add(key=5, value=20)
    rb.add(key=6, value=23)
    rb.add(key=7, value=29)
    rb.add(key=8, value=31)
    rb.add(key=9, value=32)
    rb.add(key=10, value=33)
    rb.add(key=11, value=51)
    rb.add(key=12, value=39)
    print("BEFORE REMOVAL")
    rb.in_order_traverse(rb.root)

    print()
    print("AFTER REMOVAL")
    rb.remove(10)
    rb.in_order_traverse(rb.root)


if __name__ == "__main__":
    main()
