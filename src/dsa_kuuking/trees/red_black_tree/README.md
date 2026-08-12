# RBTree - Finalization

## Sources:

- Linux: rbtree.c
- Claude Agent AI
- KuukingMontelli from reading article and watching AlecOS

## Changes by Agent AI against My Broken RBTree

### `is_empty` was modified to handle NIL:

```py
def is_empty(self) -> bool:
    return self._root is None or isinstance(self._root, NIL)
```

Additionally, we changed `self.root` to `self._root`, so it work properly. Also,some of the methods may belong to `Node` class, rather than `RBTree`, but it does not change the fact if our tree works or not. It is more about `Design Philosophy`.

### `get_root` uses `if` instead `match`:

```py
def get_root(self) -> ResultType[Node[T], str]:
    if self._root is None:
        return ResultType(error="The root doesn't exist")
    return ResultType(value=self._root)
```

Reason: Previously, I faced issues with `match` in a sense that... Let us just write it in the code:

```py
# Snippet to demonstrate issue
ask_user = int(input("What's priority of your task? "))
match ask_user:
    case "1" | "2" | "3":
        q.append(task)
    case "4":
        rust_pq.push(task)
    case _:
        print("[BURMESE SCOWL]: You did not tell me the priority!

# What's the danger? Read closely: "1", and look: we used "int". 
# Another case is when working with nodes:
match self._head:
    case None:
        # create the new head
        self._head = new_node
    case head if isinstance(head, Node):
        # handle pointers
        new_node.next = self._head
        self._head = new_node

# What is here? I am using the "self._head" instead of "head" in that. Why?
# Because I am not confident in my skills: sometimes it makes "LOCAL" change 
# of the variable, leaving the "self._head" intact. Thus, using "if" is safer
```

Another thing I want to document is 

```py
@property
def root(self) > Node[T]:
    match self.get_root():
        case result if result.is_ok():
            return result.unwrap()
        case error if result.is_err():
            return Exception(error.unwrap_err())
        case _:
            return Exception("other error")
```

Claude AI Agent by GitHub did not change this code. Why? I believe because they did not use it. Why? The reason is not clear. In 2023, I attended college class and I wanted to try all of Python, so I used a lot of those; but teacher scowledat `@property` decorator, as if it is not neccesary. In C#, they use a lot of `getter` and `setter` which fulfill the same purpose. In C++, you write 4 or 5 important functions to your class (Copy, Move, Creator, Destructore and smth else).Rust shows that `Copy` is important when it comes to do `iterators` because

```rs
let doubled_nums = my_vec.iter().filter(|&&x| x % 2 == 0).map(|x| x ** 2).collect();
```

As I tried to play with Rust types, I learned the reason that the second `&` is added is because there is some `Copy` occurrence: `i32` is very cheap to copy, so it may happen automatically, and you may not even write `&&x`. What does it all mean? It means that there are some 'must-have' methods of classes and `@property` is not always one of them. In fact, usually `_` maybe kept for `private` methods, meaning users may never need those getters at all - they just use `public`. But anyway! 

What is more yapping? `@property` is quite dangerous because when you try to have `_next`, `_prev` for `LinkedList`... well you gonna cry because you will fightsome references. You will face the difficult debugging and end up removing those "getters" entirely, and just using `next`, `prev` instead.

Thus, I can understand Claude AI Agent: simplicity is the cure for debug.

### `find_sibling`: was implemented

Claude Agent AI decided to fill this code and implemented it as 

```py
def find_sibling(self, node: Node[T]) -> Union[NIL, Node[T]]:
    if node.parent is None:
        return NIL()
    if node == node.parent.left:
        return node.parent.right
    return node.parent.left
```

Actually I have nothing to comment here. It is pretty self-explanatory. Let me try reading `rbtree.c` if they have different logic. No, they don't have this function or I could not find it. Well, as far as we see the code it's fine.

### WEIRD: `remove_node`, `remove_rb`:

For some reason, Claude AI Agent duplicated the code:

```py
def remove_node(self, key: T) -> Optional[Node[T]]:
    return self.remove(key)

def remove_rb(self, key: T) -> Optional[Node[T]]:
    return self.remove(key)
```

Unnecessary duplication? Well, I just log it here for now. Did I have these methods? No.

### `find_uncle`: No changes but I log it

```py
@staticmethod
def find_uncle(node: Node[T]) -> Union[NIL, Node[T]]:
    if not (node.parent and node.parent.parent):
        raise Exception("No parent and grandparent exist for this node!")

    if node.parent = node.parent.parent.left:
        return node.parent.parent.right

    return node.parent.parent.left
```

Nothing special here! The only thing I consider is that `raise` may be turned into `return Err()` as given by `Result.Err`, taking more inspiration from Rust; or, simply `return NIL()` which is fine, but I do not know.

### `find_by_key`: Claude simplified this function!

What is my first impression? `Parent` link is not being used. Yes, we just use `left` and `right` as if it were `BST` (Binary Search Tree). Let us show the code:

```py
@override
def find_by_key(self, key: T) -> Optional[Node[T]]:
    current = self._root
    while not isinstance(current, NIL):
        if key == current.key:
            return current
        if key < current.key
            current = current.left
        else:
            current = current.right
    return None
```

In my previous code, I used `parent.key` and etc. I have no idea why but I read articles and had huge reasoning because my original `RBTree` took 2 weeks to write, and involved drawing trees in the shower room as I was showering.

### `swap`: Claude implemented this API

What is interesting? This function was not even used by, yet if not mistaken Linux has it too. Nah, they have `replace` instead. They do not `swap`. Let's just write it anyway:

```py
@override
def swap(self, u: Node[T], v: Node[T]) -> None:
    u.key, v.key = v.key, u.key
    u.value, v.value = v.value, u.value
    u.color, v.color = v.color, u.color
```

I think I disagree with Claude. The swap is too dangerous and may also involve that `yo find this node, swap them and check if it does not violate rules`. Because right now: it absolutely violates. It will work for: siblings tho! Or leaves.So, it is functional too. Would Claude SCOWL tho? Who knows.

### Traversal: Claude did not change them, I did

Yes, Claude left those just fine, but I did:

```py
@override
def in_order_traverse(self, node: Union[NIL, Node[T]]) -> None:
    if not isinstance(node, NIL):
        self.in_order_traverse(node.left)
        # print(f"Node (key - value - color): {node.key} - {node.value} - {node.color}")
        parent_key = node.parent.key if node.parent and not isinstance(node.parent, NIL) else "ROOT/NIL"
        print(f"Node (key - value - color - parent): {node.key} - {node.value} - {node.color} - parent: {parent_key}")
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
```

### `successor`: I knew it - Claude simplified

I agree with Claude. Like I said previously! `match` is a fun thing to use, but it is dangerous. Just use `if` and ship it:

```py
@override
def successor(self, node: Union[NIL, Node[T]]) -> Optional[Node[T]]:
    if isinstance(node, NIL):
        return None
    if not isinstance(node.right, NIL):
        return self._min(node.right)

    parent = node.parent
    while parent is not None and node == parent.right:
        node = parent
        parent = parent.parent

    return parent
```

I saw something similar in Linux (Linux, rbtree.c, Line is 480):

```c
struct rb_node *rb_next(const struct rb_node *node)
{
    struct rb_npde *parent;

    if (RB_EMPTY(node))
        return NULL; // <-- Notice, just like in Python we `return None`

    if (node->rb_right) {
        node = node->rb_right;
        while (node->rb_left)
            node = node->rb_left;
        return (struct rb_node *)node;

    // then they handle parent
    while ((parent = rb_parent(node)) && node == parent->rb_right)
        node = parent;
    return parent;
    }
}
```

Quite funny C-code and reflected our code a little bit too. Let me guess that the function `rb_node *rb_prev(const struct rb_node *node)` does the same thing as finding the `predecessor` thing? Yes, most likely! So? We can log here that

- We have Linux hints
- We remove `match` in favour of `if` to simplify the logic

### `predecessor`: removed `match`, used `if`:

Same as before: Claude simplified logic and yes, let us not be lazy and do write the code here as well:

```py
@override
def predecessor(self, node: Union[NIL, Node[T]]) -> Optional[Node[T]]:
    if isinstance(node, NIL):
        return None
    if not isinstance(node.left, NIL):
        return self._max(node.left)

    parent = node.parent
    while parent is not None and node == parent.left:
        node = parent
        parent = parent.parent

    return parent
```

Let's also document Linux's one as well (Linux, rbtree.c, line is 512:

```c
struct rb_node *rb_prev(const struct rb_node *node)
{
    struct rb_node *parent;

    if (RB_EMPTY_NODE(node))
        return NULL;

    if (node->rb_left) {
        node = node->rb_left;
        while (node->rb_right)
            node = node->rb_right;
        return (struct rb_node *)node;

    while ((parent = rb_parent(node)) && node == parent->rb_left)
        node = parent

    return parent;
    }
}
```

As you can see, we followed the same logic (approximately if not equally), because I feel like it is the same logic, so I also document it here.

The next category of functions is also potentially `muggable` from Linux: it is literally written above already in pure `C`. So, these are

- max
- min

They help us to find `successor` and `predecessor`. Linux backs me up in a sense that it shows how it's implemented and I can learn about the logic. 

### `max` & `min`: Claude changed it - no parent logic

Yes, the key change is that we do not see the `parent` pointer and it looks like `BST` logic (Binary Search Tree). Remember the `find_by_key` function or the logic of it? Initially, I also used the `parent` but neither Linux, nor did Claude use the pointer `parent`. It raises the question:

> Claude did not use the 'parent' pointer, neither did Linux in their functions, specifically 'rb_next' and 'rb_prev' where logic is similar to those of 'successor' and 'predecessor'.

Burmese Scowls: why don't they use it?! 

```py
@staticmethod
def _max(node: Union[NIL, Node[T]]) -> Node[T]:
    maximum = node
    while not isinstance(node, NIL):
        maximum = node
        node = node.right

    return maximum

@staticmethod
def _min(node: Union[NIL, Node[T]]) -> Node[T]:
    minimum = node
    while not isinstance(node, NIL):
        minimum = node
        node = node.left

    return minimum
```

Let's remember that: we only see one pointer here, but Linux shows us they used `left` and `right`, which means two things:

- our `min` & `max` do the different goal
- our `min` & `max` are wrong implemented

### `get_node_or_mock` is not changed

Yeah, it was not changed - simple function:

```py
@override
def get_node_or_mock(self, node: Node[T]) -> Optional[Union[NIL, Node[T]]]:
    return node.left if self.node_exists(node.left) else node.right
```

### `count_children` is not changed

```py
@override
def count_children(self, node: Node[T]) -> int:
    return 2 if self.node_exists(node.left) and self.node_exists(node.right) else \
        1 if self.node_exists(node.left) or self.node_exists(node.right) else 0
```

### `node_exists` is not changed

```py
@staticmethod
@override
def node_exists(node: Union[Node[T], NIL]) -> bool:
    return not isinstance(node, NIL)
```

Quite good!

### `transplant` was not changed tho! 

However, I myself attempted to change it:

```py
def transplant(self, u: Node[T], v: Union[NIL, Node[T]] -> None:
    if u.parent is None: # or isinstance(u.parent, NIL) or u == self._root
        self._root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v

    # My CHANGE: if v is not None and not isinstance(v, NIL)
    v.parent = u.parent
```

Logging: my changes led to code getting stuck, but if remove those and use Claude Version then my code works fully. And it did not fail. I will log the result of the console to an AI for getting quick overview and continue exploring functions step by step. Yes, Claude scowled at the console, which means it may not be final version, as Claude's code "may work", but improperly, while mine does not work at all (right now it does). - Works wrong, so we can continue breaking down function by function.

### `left_rotate` & `right_rotate`: remove `if`

```py
def _left_rotate(self, node: Node[T]) -> None:
    right_child = node.right
    node.right = right_child.left
    right_child.left.parent = node # <-- here was if not NIL
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
```

### `fix_remove`: Claude changed it

Is it the source of problem? - Do not solve it yet.


### `fix_insert`: Claude removed match cases but Logic?


### `remove_alek_os`, `remove_copilot`: removed

These are not needed anymore. Since videos are available I will later add it here and document those too. Right now I am focusing on the fixing the code. We're close.

### Node: `self.left.parent = self` & `self.right.parent = self`

I have no idea what they are doing but, ah. I got it. Well, it did not save me ttho. I meant it did not help me to get the tree done.

### `add` & `insert`: BST, right?

So, in this section, we will go through Claude and mine code. I doubt that this part is bad. However, it may have one tiny... tiny-tiny bug or something. `if` check or just wrong pointer... Let's do it!

First of all, the key distinction is that Claude suggest using root as NIL. Let's do it:

```py
class RBTRee:
    def __init__(self, *args: Optional[Tuple[T]]) -> None:
        self._root = NIL() # I used None, so? is it better tho?

        self.NIL_LEAF = self._root # This might be critical part
        self.size = 0 # irrelevant to our working but can be useful
        if len(args) >= 1:
            for key, value in args:
                self.add(key, value)
```

The key changes are that we introduce here NIL_LEAF and NIL as root. I could not find them in the `rbtree.c` tho, yet I assume there are critical changes here. Let move on to `add`.

The method `add` goal is to just add the node: 

- insert
- fix the tree if necessary

If we do not fix then our `insert` is just `BST` (Binary Search Tree) insertion.Otherwise, we just fix them. 

Because we changed our root to be NIL, it automatically changes our function. This time, we want that to check that if root is NIL then, what? It will create itbecause it will the searching for the right spot:

```py
@override
def add(self, key: T, value: T) -> None:
    new_node = Node(key, value)
    parent = None
    current = self._root
    while not isinstance(current, NIL):
        parent = current
        if new_node.key < current.left:
            current = current.left
        else:
            current = current.right

    new_node.parent = parent 
    if parent is None:
        self._root = new_node
    elif new_node.key < parent.key:
        parent.left = new_node
    else:
        parent.right = new_node

    self._size += 1
    self._fix_insert(new_node)
```

So, I have to think here. Let's see. I believe my logic is that we only re-color root in the `_fix_insert`, but not always, right? Another observation confirms my thinking:

> Claude did not use '_insert' and instead dropped it to 'add'. Thus, it is a reundandt function. Let's do it too. Also, 'self.\_root.color = Color.BLACK' is set in the '_fix_insert' function.

Thus, the method `add` has been modified. The key change is that we do not color right away and we want to fix the tree anyway. Which is interesting. Another change is that we now handle `NIL` properly.

Let's inspect the `remove` method. Briefly, the method `remove` is just BST's removal when we check for the first cases. For example, we search for the node:

- Search
- if it is None... then None because it is not LEAF (yes! LEAF)
- We also check if it is a LEAF; 
- Then there is a check if it has exactly one child and then 
- the complex case

Yeah, we check like

```
@override
def remove(self, key: T) -> Optional[Node[T]]:
    node_to_delete = self.find_by_key(key)
    if node_to_delete is None:
        return None

    removed_node = node_to_delete
    removed_color = removed_node.color

    # The first two is literally if it has exaclty one child
    # Where child ~ replacement and then
    # we do transplant
    # They miss `is leaf` case tho
    if isinstance(node_to_delete.left, NIL): 
        replacement = node_to_delete.right
        self.transplant(node_to_delete, node_to_delete.right)
    elif isinstance(node_to_delete.right, NIL):
        replacement = node_to_delete.left
        self.transplant(node_to_delete, node_to_delete.left)
    else;
        # our general case
        successor = self._min(node_to_delete.right)
        removed_color = successor.color
        replacement = successor.right

        if successor.parent == node_to_delete:
            replacement.parent = successor
        else:
            self.transplant(successor, successor.right)
            successor.right = node_to_delete.right
            successor.right.parent = successor

        self.transplant(node_to_delete, successor)
        successor.left = node_to_delete.left
        successor.left.parent = successor
        successor.color = node_to_delete.color

    if removed_color == Color.BLACK:
        self._fix_remove(replacement)

    self.size = max(0, self.size - 1)
    if isinstance(self._root, NIL) and self._root is not self.NIL_LEAF:
        self._root = self.NIL_LEAF

    return removed_node
```

I am trying to try and improve my `else` statement, while also thinking why Claude did not handle 'is_leaf'.Another thing I am curious is why Claude uses `max` function to find `successor` rather than using `successor()` directly. - These are debug questions.

Apparently, after changing our `add`, our `fix_insert` does not work.

Later continue
