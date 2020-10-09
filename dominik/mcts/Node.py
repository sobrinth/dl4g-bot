import numpy as np


class Node:

    def __init__(self):
        self._parent = None
        self._children = []

    def set_parent(self, parent: 'Node'):
        self._parent = parent

    def get_parent(self) -> 'Node':
        return self._parent

    def get_children(self) -> []:
        return self._children

    def get_random_child(self) -> 'Node':
        return np.random.choice(self._children)

    def add_child(self, node: 'Node'):
        self._children.append(node)