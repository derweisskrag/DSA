"""Contains the linked list class"""
from typing import Optional, override, Iterable, Union, Dict, Set, Type, List

from src.interfaces.linked_list_interface import LinkedListInterface
from src.types.errors.AttributeNotFoundException import AttributeNotFoundException
from src.types.errors.DataclassNotUsedException import DataclassNotUsedException
from src.types.errors.InvalidSearchParameterException import InvalidSearchParameterException
from src.types.errors.LinkedListEmptyException import LinkedListEmptyException
from src.types.errors.NodeNotFoundException import NodeNotFoundException
from src.types.errors.UnsupportedComparisonException import UnsupportedComparisonException
from src.types.nodes.LinkedListNode import LinkedListNode as Node
from src.types.nodes.NodeType import NodeType
from src.types.ResultType import ResultType


class LinkedList[T](LinkedListInterface):
    """
    A generic singly linked list implementation.

    This class implements a singly linked list using nodes of type `Node[T]`.
    It supports operations such as adding nodes to the front or end of the list,
    removing nodes, and checking if the list is empty.

    Attributes:
        _head (Optional[Node[T]]): The head node of the linked list. Initialized to None.

    """

    def __init__(self, *args: Optional[T]):
        self._head: Optional[NodeType[T]] = None
        self.size: int = 0
        self._hash_set: Set[NodeType[T]] = set()

        if len(args) > 0:
            for arg in args:
                self.add_to_front(arg)

    @override
    def add_to_front(self, data: Union[T, NodeType[T]]) -> Optional[ResultType[NodeType[T], str]]:
        """
        Adds a new node with the specified data to the front of the linked list.

        This method creates a new node containing the provided data and places it
        at the beginning of the list. The current head of the list becomes the next
        node of the newly added node.

        Args:
            data (T): The data to be stored in the new node. The type is specified
                      by the generic parameter `T`, allowing for any data type.

        Returns:
            None: This method does not return any value. It modifies the linked list
                  in place by updating the head node.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(10)
            >>> ll.add_to_front(5)
            # Now, the list is: 5 -> 10
        """

        return self.insert_node(data, 0)

    @override
    def insert_node(self, data: Union[T, NodeType[T]], position: int) -> Optional[ResultType[NodeType[T], str]]:
        """
        Inserts a new node with the specified data at the given position in the linked list.

        This method creates a new node containing the provided data and places it at the
        specified position in the list. The position is zero-based, where 0 represents
        the head of the list. If the position is invalid (not an integer), a TypeError is raised.

        Args:
            data (Union[T, Node[T]]): The data to be stored in the new node. If a Node is provided,
                                      it will be inserted directly; otherwise, a new Node will be
                                      created with the given data.
            position (int): The zero-based index at which the new node should be inserted.
                            0 corresponds to inserting at the head of the list.

        Returns:
            Node[T]: The newly created or provided node that has been inserted into the linked list.

        Raises:
            TypeError: If the specified position is not an integer.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.insert_node(10, 0)
            >>> ll.insert_node(5, 1)
            # Now, the list is: 10 -> 5
        """

        # Check if position is an integer
        if not isinstance(position, int):
            return ResultType(error=f"Cannot insert the node into the linked list due to wrong"
                                    f"specified type of 'position' argument: {type(position)}"
                                    f"must be 'integer'.")

        # Create a new node if data is not already a Node
        if not isinstance(data, Node):
            # initialize the node to insert
            new_node = Node(data)
        else:
            # data is a Node already
            new_node = data
        # use the position to identify
        # where to insert the node
        if position == 0:
            match self._head:
                case head if head is not None:
                    # arrange the node in the list
                    new_node.next = self._head

                    # update the head
                    self._head = new_node
                case None:
                    # create new head
                    self._head = new_node

                    if hasattr(self, '_tail'):
                        setattr(self, '_tail', new_node)
                case _:
                    return ResultType(error="Something wrong!")
        elif position == -1 and hasattr(self, "_tail"):
            # arrange the node in the doubly-linked list
            tail = getattr(self, "_tail")
            try:
                # arrange the tail in the list
                setattr(tail, 'next', new_node)

                # maintain the prev pointer
                new_node.prev = tail

                # update the tail
                setattr(self, '_tail', new_node)
            except AttributeError as e:
                return ResultType(error=f"{e!r}")
        else:
            for index, node in enumerate(self.traverse()):
                if index == position - 1:
                    new_node.next = node.next
                    node.next = new_node

        # increment the size
        self.size += 1

        # store this node in the set
        self._hash_set.add(new_node)

        return ResultType(value=new_node)

    @override
    def remove_by_id(self, node_id: int) -> Optional[NodeType[T]]:
        """
        Removes the node in the linked list with the specified unique ID.

        This method searches for the node in the linked list whose unique identifier
        matches the specified `node_id`. If such a node is found, it is removed from the
        list using the `remove_by_data` method, which handles edge cases and updates
        the list appropriately. The removed node is returned. If no node with the given
        ID is found, the method returns `None`.

        Args:
            node_id (int): The unique identifier of the node to be removed. This ID is
                           typically obtained from the `id()` function of a node instance.

        Returns:
            Optional[Node[T]]: The removed node if it is found; otherwise, `None`.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(10)
            >>> node = ll.add_to_front(5)
            >>> deleted_node = ll.remove_by_id(id(node))
            >>> deleted_node.data
            5
            >>> ll.get_size()
            1
            >>> ll.remove_by_id(999)  # Assuming 999 is not a valid ID
            Did not find the node to remove! Please, check your id for the node
            None
        """

        # determine the node
        removed_node = self.find_by_id(node_id)

        # check if the node to delete was found in the linked list.
        if removed_node is None:
            raise NodeNotFoundException(f"Could not find the node with the specified id: {node_id}.")
        else:
            # use the function defined for data (handles edge cases)
            return self.remove_by_data(removed_node.data)

    @override
    def remove_by_data(self, data: T) -> Optional[NodeType[T]]:
        """
       Removes the first node in the linked list that contains the specified data.

       This method searches for the first node in the linked list whose data matches
       the specified value. If such a node is found, it is removed from the list. If
       the node to be removed is the head, the head is updated. If the node is found
       elsewhere in the list, it is removed and the list is re-linked. The removed node
       is returned. If the list is empty or no such node is found, the method returns `None`.

       Args:
           data (T): The data value to search for in the linked list. The type is specified
                     by the generic parameter `T`, allowing for any data type.

       Returns:
           Optional[Node[T]]: The removed node if it is found; otherwise, `None`.

       Example:
           >>> ll = LinkedList[int]()
           >>> ll.add_to_front(10)
           >>> ll.add_to_front(5)
           >>> deleted_node = ll.remove_by_data(10)
           >>> deleted_node.data
           10
           >>> ll.get_size()
           1
           >>> ll.remove_by_data(15)
           Nothing to delete, because the list is empty!
           None
       """

        # cannot delete if empty
        if self.is_empty():
            raise LinkedListEmptyException()

        if self._head.data == data:
            # check if the target to delete is actually head
            # handles the sizes already
            self.remove_head()
        else:
            # the node to delete is not head, so find it
            removed_node_index = self.find_by_data(data)

            removed_node = self[removed_node_index]

            # handle the exception when node is none
            if removed_node is None:
                raise NodeNotFoundException()

            # remove it from set
            self._hash_set.remove(removed_node)

            # find the spot
            spot_node = self.find_spot(removed_node)

            # now the current is the node before the node to delete
            # we can arrange the list and delete it
            spot_node.next = removed_node.next

            # maintain the prev pointer if exists
            if hasattr(removed_node.next, 'prev'):
                removed_node.next.prev = spot_node
                # clean up the prev pointer
                removed_node.prev = None

            # delete the node
            removed_node.next = None

            # decrease the size
            self.size -= 1

            # return the deleted node
            return removed_node

    @override
    def remove_head(self) -> Optional[NodeType[T]]:
        """
        Removes the node at the head of the linked list.

        This method removes the node currently at the head of the list and updates the head
        to the next node in the list. If the list is empty, the method does nothing and returns
        `None`. The removed node is returned, which contains the data and ID of the removed node.

        Returns:
            Optional[Node[T]]: The removed node if the list is not empty. If the list is empty,
                                it returns `None`. The returned node contains the data and ID
                                of the removed node.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(10)
            >>> ll.add_to_front(5)
            >>> deleted_node = ll.remove_head()
            >>> deleted_node.data
            5
            >>> ll._head.data
            10
        """

        if not self._head:
            raise LinkedListEmptyException()

        # define node to remove
        removed_node = self._head

        # remove from set
        self._hash_set.remove(removed_node)

        # update the head
        self._head = self._head.next

        # Clean up the reference to the next node
        removed_node.next = None

        if hasattr(removed_node, 'prev'):
            removed_node.prev = None

        # decrease the size by 1
        self.size -= 1

        # return the removed node
        return removed_node

    @override
    def is_empty(self) -> bool:
        """
        Checks if the linked list is empty.

        This method determines whether the linked list contains any nodes. It returns
        `True` if the list is empty (i.e., if the head of the list is `None`), and
        `False` otherwise.

        Returns:
            bool: `True` if the linked list is empty; `False` if it contains one or more nodes.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.is_empty()
            True
            >>> ll.add_to_front(10)
            >>> ll.is_empty()
            False
        """
        return self._head is None

    def has_head(self) -> bool:
        return self._head is not None

    @override
    def get_head(self) -> ResultType[NodeType[T], str]:
        if not self._head:
            return ResultType(error="Cannot retrieve the head of the empty linked list.")

        return ResultType(value=self._head)

    @override
    def get_size(self) -> int:
        """
        Returns the number of nodes in the linked list.

        This method provides the count of nodes currently present in the linked list.
        It returns an integer representing the number of nodes from the head to the end of the list.

        Returns:
            int: The number of nodes in the linked list.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(10)
            >>> ll.add_to_front(5)
            >>> ll.get_size()
            2
        """
        return self.size

    @override
    def display(self) -> None:
        try:
            for node in self.traverse():
                # '\n' prints the new line for next prints
                print(node, end="->" if node.next else "\n")
        except LinkedListEmptyException as e:
            print(f"Cannot traverse empty linked list: {e!s}")

    @override
    def display_backwards(self) -> None:
        try:
            for node in self.traverse_backwards():
                print(node, end="->" if node.next else "\n")
        except LinkedListEmptyException as e:
            print(f"Cannot traverse empty linked list: {e!r}")

    @override
    def find_by_id(self, node_id: int) -> Optional[NodeType[T]]:
        """
        Searches for a node in the linked list by its unique ID.

        This method traverses the linked list and looks for a node whose ID matches
        the specified `node_id`. If a node with the given ID is found, the method
        returns that node. If no node with the specified ID is found, the method
        returns -1.

        Args:
            node_id (int): The unique identifier of the node to search for. This ID is
                           typically obtained from the `id()` function of a node instance.

        Returns:
            Node[T] | int: The node with the specified ID if found; otherwise, returns
                           -1 to indicate that no such node exists. The returned node
                           contains the data and ID of the node.

        Example:
            >>> ll = LinkedList[int]()
            >>> node1 = Node(10)
            >>> node2 = Node(5)
            >>> ll.add_to_front(node1.data)
            >>> ll.add_to_front(node2.data)
            >>> found_node = ll.find_by_id(id(node1))
            >>> found_node.data
            10
            >>> ll.find_by_id(999)  # Assuming 999 is not a valid ID
            -1
        """

        # no need to search if empty linked list
        if self.is_empty():
            return None

        for node in self.traverse():
            if node.get_id() == node_id:
                # matched the target by id
                return node

        return None  # not found

    @override
    def find_spot(self, target: NodeType[T]) -> Optional[NodeType[T]]:
        if target is None:
            return None

        for node in self.traverse():
            if node.next == target:
                return node

        return None  # raise exception

    @override
    def find_by_data(self, data: T) -> int:
        """
        Searches for a node in the linked list by its data.

        This method traverses the linked list, looking for a node whose data matches the
        specified value. If a matching node is found, it returns the node. If no node
        with the specified data is found, it returns -1. The type of data is specified
        by the generic parameter `T`, which should support equality comparison.

        Args:
            data (T): The data to search for in the linked list. The type is specified
                      by the generic parameter `T`, allowing for any data type that
                      supports equality comparison.

        Returns:
            Node[T] | int: The node containing the specified data if found; otherwise,
                           returns -1. The returned node contains the data and ID of the node.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(10)
            >>> ll.add_to_front(5)
            >>> found_node_index = ll.find_by_data(10)
            >>> found_node_index
            1
            >>> ll.find_by_data(3)
            -1
        """

        if self.is_empty():
            raise LinkedListEmptyException(f"Cannot find the node by specified data {data} in an empty list!")

        if not self.is_primitive_type(type(data)):
            other = data.__class__(**{k: v for k, v in data.__dict__.items()})
            if data != other:
                raise UnsupportedComparisonException(f"The type {type(data)} does not support comparison '__eq__'."
                                                     f"The specified type does not implement the comparison.")

        for i, node in enumerate(self.traverse()):
            if node.data == data:
                return i

        return -1  # not found

    @override
    def find_by_params(self, search_param: Dict[str, Union[str, int, float]]) -> Optional[NodeType[T]]:
        """
        Searches for a node in the linked list by a specified attribute and its value.

        This method traverses the linked list looking for a node where the attribute specified
        by the key in `search_param` matches the value given. It assumes that the attribute exists
        on the data and that the data type can handle comparison with the given value.

        Args:
            search_param (Dict[str, Union[str, int, float]]): A dictionary with a single key-value pair where
                                                              the key is the attribute name and the value is
                                                              the target value to search for. The value must
                                                              be a primitive type that can be compared.

        Returns:
            Optional[Node[T]]: The node containing the data with the specified attribute value if found;
                               otherwise, returns None.

        Example:
            >>> class Person:
            >>>     def __init__(self, name: str, age: int) -> None:
            >>>         self.name = name
            >>>         self.age = age
            >>>
            >>> ll = LinkedList[Person]()
            >>> ll.add_to_front(Person("Alice", 21))
            >>> ll.add_to_front(Person("Bob", 25))
            >>> found_node = ll.find_by_params({"name": "Alice"})
            >>> found_node.data.name
            "Alice"
            >>> ll.find_by_params({"age": 30}) is None
            True
        """

        if self.is_empty():
            raise LinkedListEmptyException(f"Cannot find the node by specified parameters {search_param} in an empty "
                                           f"list!")

        if not isinstance(search_param, dict):
            raise InvalidSearchParameterException()

        if len(search_param) != 1:
            raise InvalidSearchParameterException("Search parameter should have exactly one key-value pair.")

        # unpack the dictionary
        (attribute, target_value), = search_param.items()

        for node in self.traverse():
            try:
                if hasattr(node.data, attribute):
                    if getattr(node.data, attribute) == target_value:
                        return node
                else:
                    raise AttributeNotFoundException(attribute)
            except ValueError as e:
                print(f"ValueError: {e!r}")
            except DataclassNotUsedException as e:
                print(f"DataclassNotUsedException: {e!r}")

        return None

    @override
    def find_by_attribute(self, attribute_name: str, attribute_value: Union[str, int]) -> Optional[NodeType[T]]:
        """
        Searches for a node in the linked list by a specific attribute of its data.

        This method traverses the linked list looking for a node where the attribute specified
        by `attribute_name` matches the `attribute_value`. It assumes that the attribute exists
        on the data and that the data type can handle comparison with the given value.

        Args:
            attribute_name (str): The name of the attribute to search for in the data of the node.
            attribute_value (Union[str, int]): The value to match against the attribute. This must
                                               be a primitive type that can be compared.

        Returns:
            Node[T] | int: The node containing the data with the specified attribute value if found;
                           otherwise, returns -1.

        Example:
            >>> class Person:
            >>>     def __init__(self, name: str, age: int) -> None:
            >>>         self.name = name
            >>>         self.age = age
            >>>
            >>> ll = LinkedList[Person]()
            >>> ll.add_to_front(Person("Alice", 21))
            >>> ll.add_to_front(Person("Bob", 25))
            >>> found_node = ll.find_by_attribute('name', "Alice")
            >>> found_node.data.name
            "Alice"
            >>> ll.find_by_attribute('age', 30)
            -1
        """

        if self.is_empty():
            raise LinkedListEmptyException(f"Cannot find the node by attribute {attribute_name} in an empty list!")

        for node in self.traverse():
            data = node.data
            # Use getattr to dynamically access the attribute
            if getattr(data, attribute_name, None) == attribute_value:
                return node

        return None  # not found

    def _find_by_position(self, index: int) -> Optional[NodeType[T]]:
        """
        Finds the node at the specified index in the linked list.

        This method retrieves the node located at the given index. It supports both positive
        and negative indexing. Negative indexing allows access to nodes from the end of the list
        (e.g., -1 refers to the last node).

        Args:
            index (int): The position of the node to retrieve. It must be an integer. Positive
                         indices start from 0 (head of the list), and negative indices count
                         backward from the end of the list.

        Returns:
            Optional[Node[T]]: The node at the specified index, or None if the index is invalid.

        Raises:
            TypeError: If `index` is not an integer.
            IndexError: If `index` is out of the valid range of the list (negative or greater than
                        or equal to the size of the list).

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(1) # tail
            >>> ll.add_to_front(2) # head
            >>> ll._find_by_position(1)
            Node(data=1)
            >>> ll._find_by_position(-1)
            Node(data=1)
            >>> ll._find_by_position(0)
            Node(data=2)
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")

        # get the size of the linked list
        size = self.get_size()

        if size == 0:
            # return None for empty linked list.
            return None

        if not self._is_index_in_bound(index, size):
            raise IndexError("Index out of range.")

        if index < 0:
            index += size

        for i, node in enumerate(self.traverse()):
            if i == index:
                return node

    @override
    def traverse(self) -> Iterable[NodeType[T]]:
        """
       Iterates over all nodes in the linked list.

       This method yields each node in the linked list starting from the head and
       continuing to the end of the list. It allows for iteration over the nodes
       using a for-loop or any other iteration construct.

       Yields:
           Node[T]: The current node in the linked list during each iteration.

       Example:
           >>> ll = LinkedList[int]()
           >>> ll.add_to_front(10)
           >>> ll.add_to_front(5)
           >>> for node in ll.traverse():
           >>>     print(node.data)
           5
           10
       """
        current = self._head
        while current:
            yield current
            current = current.next

    @override
    def traverse_backwards(self) -> Iterable[NodeType[T]]:
        """
        Iterates over all nodes in the linked list in reverse order.

        This method yields each node in the linked list starting from the end and
        moving to the beginning of the list. It allows for reverse iteration over
        the nodes, but requires that the list be reversible. This is typically useful
        for lists where reversing the order of traversal is necessary.

        Yields:
            Node[T]: The current node in the linked list during each iteration,
                     starting from the last node and moving towards the head.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(1)
            >>> ll.add_to_front(2)
            >>> ll.add_to_front(3)
            >>> for traversed_node in ll.traverse_backwards():
            >>>     print(traversed_node.data)
            1
            2
            3
        """
        for node in reversed(self):
            yield node

    def concat(self, ll: 'LinkedList[T]') -> 'LinkedList[T]':
        """
        Concatenates the current linked list with another linked list.

        This method adds all nodes from the given linked list `ll` to the front of the current linked list.
        If the current linked list is empty, the nodes from `ll` are added directly to the current list.
        If `ll` is empty, the current list remains unchanged.

        Args:
            ll (LinkedList[T]): The linked list to be concatenated with the current list.

        Returns:
            LinkedList[T]: The current linked list after concatenation.

        Example:
            >>> linked_list_1 = LinkedList[int]()
            >>> linked_list_1.add_to_front(10)
            >>> linked_list_1.add_to_front(5)
            >>> linked_list_1.display()
            Node(data=5)->Node(data=10)

            >>> linked_list_2 = LinkedList[int]()
            >>> linked_list_2.add_to_front(15)
            >>> linked_list_2.add_to_front(20)
            >>> linked_list_2.display()
            Node(data=20)->Node(data=15)

            >>> linked_list_1.concat(linked_list_2)
            >>> linked_list_1.display()
            Node(data=15)->Node(data=20)->Node(data=5)->Node(data=10)

            # Additional Example
            >>> empty_list = LinkedList[int]()
            >>> linked_list_3 = LinkedList[int]()
            >>> linked_list_3.add_to_front(30)
            >>> linked_list_3.add_to_front(25)
            >>> linked_list_3.display()
            Node(data=25)->Node(data=30)

            >>> linked_list_3.concat(empty_list)
            >>> linked_list_3.display()
            Node(data=25)->Node(data=30)

            >>> linked_list_4 = LinkedList[int]()
            >>> linked_list_4.add_to_front(1)
            >>> linked_list_4.add_to_front(2)
            >>> linked_list_4.add_to_front(3)
            >>> linked_list_4.display()
            Node(data=3)->Node(data=2)->Node(data=1)

            >>> linked_list_4.concat(empty_list)
            >>> linked_list_4.display()
            Node(data=3)->Node(data=2)->Node(data=1)
        """
        # Traverse the second list and add each node's data to the front of the current list
        for node in ll.traverse():
            self.add_to_front(node.data)

        return self

    def reverse(self) -> Optional['LinkedList[T]']:
        """
        Reverses the linked list in place.

        This method reverses the order of nodes in the linked list. After execution, the
        head of the list will point to what was previously the last node, and the tail will
        point to what was previously the head. The method operates in-place and does not
        require additional memory beyond a few pointers.

        If the list is empty (i.e., the head is `None`), the method returns `None` as there
        is nothing to reverse.

        Returns:
            Optional['LinkedList[T]']: The reversed linked list. Returns `None` if the
            list was empty.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(1) # tail
            >>> ll.add_to_front(2) # middle
            >>> ll.add_to_front(3) # head
            >>> ll.display()
            Node(data=3)->Node(data=2)->Node(data=1)
            >>> reversed_list = ll.reverse()
            >>> reversed_list.display()
            Node(data=1)->Node(data=2)->Node(data=3)
        """
        if not self._head:
            return None

        # reverse the linked list
        curr = self._head
        prev = None
        while curr:
            curr.next, prev, curr = prev, curr, curr.next

        # fix the link list
        self._head = prev

        # return the reversed linked list
        return self

    def swap_two_nodes(self, a: NodeType[T], b: NodeType[T]) -> Optional[ResultType[T, str]]:
        raise NotImplemented("Not supported yet!")

    def to_list(self) -> List[Node[T]]:
        """
        Converts the current linked list instance to a Python list.

        This method converts the current linked list instance into a list
        containing the elements of the linked list in the same order.

        Returns:
            list: A list containing the elements of the linked list.

        Example:
            >>> linked_list = LinkedList[int]()
            >>> linked_list.add_to_front(1)
            >>> linked_list.add_to_front(2)
            >>> linked_list.add_to_front(3)
            >>> linked_list.to_list()
            [3, 2, 1]
        """
        return list(node for node in self.traverse())

    @staticmethod
    def is_primitive_type(type_check: Type) -> bool:
        """
        Checks if the given type is a primitive type.

        This method determines whether the type specified by `type_check` is
        one of the primitive types: `int`, `float`, or `str`. It returns `True`
        if the type is among these primitive types and `False` otherwise.

        Args:
            type_check (Type): The type to check.

        Returns:
            bool: `True` if `type_check` is one of `int`, `float`, or `str`;
                  otherwise, `False`.

        Example:
            >>> LinkedList.is_primitive_type(int)
            True
            >>> LinkedList.is_primitive_type(float)
            True
            >>> LinkedList.is_primitive_type(str)
            True
            >>> LinkedList.is_primitive_type(list)
            False
            >>> LinkedList.is_primitive_type(dict)
            False
        """
        return issubclass(type_check, (int, float, str))

    @staticmethod
    def _is_index_in_bound(index: int, size: int) -> bool:
        """
        Checks if a given index is within the valid bounds of a list.

        This method determines whether a specified index is within the valid range of a list,
        considering both positive and negative indices. Positive indices start from 0 (head of
        the list), while negative indices count backward from the end of the list.

        Args:
            index (int): The index to check. Can be either positive or negative.
            size (int): The size of the list. Must be a non-negative integer.

        Returns:
            bool: True if the index is within bounds, False otherwise.

        Notes:
            - For positive indices, the valid range is from 0 to size-1.
            - For negative indices, the valid range is from -size to -1.

        Example:
            >>> LinkedList._is_index_in_bound(0, 5)
            True
            >>> LinkedList._is_index_in_bound(4, 5)
            True
            >>> LinkedList._is_index_in_bound(5, 5)
            False
            >>> LinkedList._is_index_in_bound(-1, 5)
            True
            >>> LinkedList._is_index_in_bound(-6, 5)
            False
        """
        if index == 0 or 0 < index < size:
            return True

        # negative index case
        absolute_value_index = -index

        if 0 < size - absolute_value_index < size:
            return True

    @staticmethod
    def to_list_static(ll: 'LinkedList[T]'):
        """
        Converts a linked list to a Python list.

        This method takes a linked list and returns a list containing the elements
        of the linked list in the same order.

        Args:
            ll (LinkedList[T]): The linked list to be converted.

        Returns:
            list: A list containing the elements of the linked list.

        Raises:
            ValueError: If the provided linked list is None.

        Example:
            >>> linked_list = LinkedList[int]()
            >>> linked_list.add_to_front(1)
            >>> linked_list.add_to_front(2)
            >>> linked_list.add_to_front(3)
            >>> LinkedList.to_list(ll)
            [3, 2, 1]
        """
        if not ll:
            raise ValueError("None is not iterable! Please, provide the linked list.")

        return list(ll.traverse())

    @staticmethod
    def from_list(iterable: Iterable[T]) -> 'LinkedList[T]':
        """
        Creates a linked list from an iterable.

        This method takes an iterable (e.g., list, queue) and returns a linked list
        containing the elements of the iterable in reverse order.

        Args:
            iterable (Iterable[T]): The iterable to be converted into a linked list.

        Returns:
            LinkedList[T]: A linked list containing the elements of the iterable.

        Raises:
            ValueError: If the provided iterable is empty or None.

        Example:
            >>> original_list = [1, 2, 3]
            >>> linked_list = LinkedList.from_list(original_list)
            >>> list(linked_list.traverse())
            [3, 2, 1]
        """
        if not iterable:
            raise ValueError("Please, provide the iterable (list, queue)")

        # create a linked list
        ll = LinkedList[T]()

        for value in iterable:
            ll.add_to_front(value)

        return ll

    def __contains__(self, item: NodeType[T]) -> bool:
        """
        Checks if the specified node is present in the linked list.

        This method allows checking for the existence of a node in the linked list using
        the `in` operator. It leverages an internal hash set to efficiently determine if
        the given node is part of the linked list.

        Args:
            item (Node[T]): The node to check for presence in the linked list.

        Returns:
            bool: True if the node is present in the linked list, False otherwise.

        Example:
            >>> ll = LinkedList[int]()
            >>> node1_result = ll.add_to_front(1)
            >>> node2_result = ll.add_to_front(2)
            >>> if node1_result.is_ok():
            >>>     node1_result.unwrap() in ll
            True
            >>> node3 = Node(3)
            >>> node3 in ll
            False
            >>> node4 = Node(2)
            >>> node4 in ll # because node4.next is None, while node2.next is node1
            False
        """
        return item in self._hash_set

    def __len__(self) -> int:
        """
        Returns the number of elements in the linked list (length).

        This method provides the size of the linked list, which is the total number of nodes
        present in the list. It allows the use of Python's built-in `len()` function to obtain
        the count of elements in the linked list.

        Returns:
            int: The number of elements (nodes) in the linked list.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(1)
            >>> ll.add_to_front(2)
            >>> len(ll)
            2
        """
        return self.size

    def __reversed__(self) -> Iterable[NodeType[T]]:
        """
        Iterates over all nodes in the linked list in reverse order.

        This method provides an iterator that yields nodes in the linked list starting
        from the last node and moving towards the head. It is implemented using the
        `reverse` method to reverse the linked list and then iterate over the reversed list.

        Returns:
            Iterable[Node[T]]: An iterator that yields each node in the linked list
                                in reverse order.

        Example:
            >>> ll = LinkedList[int]()
            >>> ll.add_to_front(1)
            >>> ll.add_to_front(2)
            >>> ll.add_to_front(3)
            >>> for node_in_the_list in reversed(ll):
            >>>     print(node_in_the_list.data)
            1
            2
            3
        """

        if self.get_size() == 0:
            return None

        for node in self.reverse().traverse():
            yield node

    def __getitem__(self, index: int) -> Optional[NodeType[T]]:
        """
       Retrieves the data of the node at the specified index in the linked list.

       This method allows access to nodes using both positive and negative indices. Positive indices
       start from 0 (head of the list), and negative indices count backward from the end of the list
       (e.g., -1 refers to the last node). It provides an interface similar to list indexing in Python.

       Args:
           index (int): The position of the node to retrieve. Positive indices start from 0 (head
                        of the list), and negative indices count backward from the end of the list.

       Returns:
           T: The data of the node at the specified index.

       Raises:
           IndexError: If the index is out of the valid range of the list (negative or greater than
                       or equal to the size of the list).

       Example:
           >>> ll = LinkedList[int]()
           >>> ll.add_to_front(1)
           >>> ll.add_to_front(2)
           >>> ll[1]
           1
           >>> ll[-1]
           1
       """
        return self._find_by_position(index)

    def __setitem__(self, index: int, value: NodeType[T]) -> None:
        # define the node to replace
        node_to_replace = self[index]

        # remove it and insert new one into its position
        self.remove_by_data(node_to_replace.data)
        self.insert_node(value, index)
