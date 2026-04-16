class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked List
class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        temp = self.head
        result = []
        while temp:
            result.append(temp.data)
            temp = temp.next
        return result

# Stack (Linked List से बना हुआ)
class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if not self.top:
            return None
        data = self.top.data
        self.top = self.top.next
        return data

    def peek(self):
        return None if  not self.top else self.top.data

# Binary Search Tree
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def inorder(self, node=None, result=None):
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.key)
            self.inorder(node.right, result)
        return result
