from __future__ import annotations
from typing import Optional, Any, Callable
import math
import copy as cpy


class BinarySearchTree:

    def __init__(self, root: Optional[Any]) -> None:

        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def set_left_to(self, tree: BinarySearchTree) -> None:
        if isinstance(tree, BinarySearchTree):
            self._left = tree
        else:
            raise TypeError

    def set_right_to(self, tree: BinarySearchTree) -> None:
        if isinstance(tree, BinarySearchTree):
            self._right = tree
        else:
            raise TypeError

    @property
    def root(self) -> Any:
        """Root of the BST"""
        return cpy.copy(self._root)

    @property
    def left(self) -> Any:
        """Return copy of left child of the BST"""
        return self._left.copy()

    @property
    def right(self) -> Any:
        """Return copy of right child of the BST"""
        return self._right.copy()

    @property
    def is_balanced(self) -> bool:

        if self.is_empty():
            return True

        if abs(self._left.height - self._right.height) <= 1 and \
                self._left.is_balanced and self._right.is_balanced:
            return True

        return False

    @property
    def height(self) -> int:
        """Return the height of the tree"""
        if self.is_empty():
            return 0
        else:
            return 1 + max(self._left.height, self._right.height)

    def is_empty(self) -> bool:
        """Return whether this BST is empty.
        """
        return self._root is None

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return self._left.__contains__(item)
        else:
            return self._right.__contains__(item)

    def __copy__(self) -> BinarySearchTree:
        """Return a copy of the BST"""
        tree = BinarySearchTree(self._root)
        tree.set_right_to(self._right)
        tree.set_left_to(self._left)
        return tree

    def copy(self) -> BinarySearchTree:
        """Return a copy of the BST"""
        if self.is_empty():
            return BinarySearchTree(self.root)
        else:
            tree = BinarySearchTree(self.root)
            tree.set_right_to(self._right.copy())
            tree.set_left_to(self._left.copy())
            return tree

    def __abs__(self) -> BinarySearchTree:
        """Return BST similar to self, but with abs values"""
        return self.map(lambda x: abs(x))

    def abs(self) -> BinarySearchTree:
        """Return BST similar to self, but with abs values"""
        return self.map(lambda x: abs(x))

    def __eq__(self, other: BinarySearchTree) -> bool:
        """Check weather two BST's ate same or not"""
        return self.to_list() == other.to_list()

    def floor(self) -> BinarySearchTree:
        """Return BST similar to self, but with floor values"""
        return self.map(lambda x: math.floor(x))

    def ceil(self) -> BinarySearchTree:
        """Return BST similar to self, but with ceil values"""
        return self.map(lambda x: math.ceil(x))

    def __floor__(self) -> BinarySearchTree:
        """Return BST similar to self, but with floor values"""
        return self.map(lambda x: math.floor(x))

    def __ceil__(self) -> BinarySearchTree:
        """Return BST similar to self, but with ceil values"""
        return self.map(lambda x: math.ceil(x))

    def map(self, key=Callable) -> BinarySearchTree:
        """Map the BST to key and return mapped BST"""
        copy = self.copy()

        if not copy.is_empty():
            copy._root = key(self._root)
            copy.set_left_to(copy._left.map(key))
            copy.set_right_to(self._right.map(key))

        return copy

    def apply(self, key=Callable) -> None:
        """Map the BST to key"""

        if not self.is_empty():
            self._root = key(self._root)
            self._left.map(key)
            self._right.map(key)

    def __str__(self) -> str:
        """Return a string representation of this BST.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.
        """
        if self.is_empty():
            return ''
        else:
            return (
                    depth * '  ' + f'{self._root}\n'
                    + self._left._str_indented(depth + 1)
                    + self._right._str_indented(depth + 1)
            )

    def maximum(self) -> Optional[int]:
        """Return the maximum number in this BST, or None if this BST is empty.
        """
        if self.is_empty():
            return None
        else:
            curr_max = self._root

            if self._right._root and curr_max < self._right._root:
                curr_max = self._right.maximum()

            return curr_max

    def minimum(self) -> Optional[Any]:
        """Return the minimum number in this BST, or None if this BST is empty.
        """
        if self.is_empty():
            return None
        else:
            curr_min = self._root

            if self._right._root and curr_min > self._left._root:
                curr_min = self._left.maximum()

            return curr_min

    def count(self, item: Any) -> int:
        """Return the number of occurrences of <item> in this BST.
        """
        if self.is_empty():
            return 0
        else:
            count = 0
            if self._root == item:
                count += 1
            if self._left._root and item <= self._root:
                count += self._left.count(item)
            if self._right._root and item >= self._root:
                count += self._right.count(item)
            return count

    def items(self) -> list:
        """Return all of the items in the BST in sorted order.
        """
        if self.is_empty():
            return []
        else:
            return self._left.items() + [self._root] + self._right.items()

    def smaller(self, item: Any) -> list:
        """Return all of the items in this BST less than <item> in sorted order.
        """
        if self.is_empty() or item is None:
            return []
        else:
            if self._root >= item:
                return self._left.smaller(item)
            else:
                return self._left.items() + [self._root] + self._right.smaller(item)

    def bigger(self, item: Any) -> list:
        """Return all of the items in this BST greater than <item> in sorted order.
        """
        if self.is_empty() or item is None:
            return []
        else:
            if self._root <= item:
                return self._right.bigger(item)
            else:
                return self._left.bigger(item) + [self._root] + self._right.items()

    def insert(self, item: Any) -> None:
        """Insert item into the list
        """
        if self.is_empty():
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item > self._root:
            self._right.insert(item)
        else:
            self._left.insert(item)

    def remove(self, item) -> bool:
        """Remove the item from the tree
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()
        else:
            if item > self._root:
                return self._right.remove(item)
            else:
                return self._left.remove(item)

    def _delete_root(self) -> None:

        if self._left.is_empty() and self._right.is_empty():

            self._root = None
            self._right._root = None
            self._left._root = None

        elif self._left.is_empty():

            self._root, self._left, self._right = self._right._root, \
                                                  self._right._left, \
                                                  self._right._right

        elif self._right.is_empty():

            self._root, self._left, self._right = self._left._root, \
                                                  self._left._left, \
                                                  self._left._right
        else:
            self._root = self._extract_max()

    def _extract_max(self) -> Any:

        if self._right._root is None:  # if this is the case then _root is the largest number
            max_item = self._root
            self._root, self._right._root, self._left._root = None, None, None
            return max_item
        else:
            return self._right._extract_max()

    def invert(self) -> None:
        """Invert the BST"""
        if not self.is_empty():

            if not self._left.is_empty():
                self._left.invert()
            if not self._right.is_empty():
                self._right.invert()

            temp = self._left
            self._left = self._right
            self._right = temp

    @staticmethod
    def create_tree(lst: list) -> BinarySearchTree:
        """Return a balanced binary search tree"""
        if len(lst) == 1:
            return BinarySearchTree(lst[0])

        elif len(lst) > 1:

            lst = sorted(lst)

            middle = len(lst) // 2

            left = BinarySearchTree.create_tree(lst[:middle])

            right = None

            if middle + 1 < len(lst):
                right = BinarySearchTree.create_tree(lst[(middle + 1):])

            tree = BinarySearchTree(lst[middle])

            tree._left = left

            if right:
                tree._right = right

            return tree

    def to_list(self) -> list:
        """Return all of the items in the BST in sorted order.
        """
        if self.is_empty():
            return []
        else:
            return self._left.to_list() + [self._root] + self._right.to_list()

    def balance(self) -> None:
        """Convert the BST to a balanced BST"""
        tree = BinarySearchTree.create_tree(self.to_list())

        self._root = tree._root
        self._left = tree._left
        self._right = tree._right