from collections import defaultdict


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1

        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

        self.size = 0

    def add_node(self, node):
        # Add right after head
        node.next = self.head.next
        node.prev = self.head

        self.head.next.prev = node
        self.head.next = node

        self.size += 1

    def remove_node(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

        self.size -= 1

    def remove_last(self):
        # Remove least recently used
        if self.size > 0:
            node = self.tail.prev
            self.remove_node(node)
            return node


class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0

        self.key_map = {}  # key -> node
        self.freq_map = defaultdict(DoublyLinkedList)

    def update_freq(self, node):
        freq = node.freq

        # Remove node from old freq list
        self.freq_map[freq].remove_node(node)

        # Update min frequency
        if freq == self.min_freq and self.freq_map[freq].size == 0:
            self.min_freq += 1

        # Increase frequency
        node.freq += 1

        # Add to new frequency list
        self.freq_map[node.freq].add_node(node)

    def get(self, key: int) -> int:
        if key not in self.key_map:
            return -1

        node = self.key_map[key]
        self.update_freq(node)

        return node.value

    def put(self, key: int, value: int) -> None:

        if self.capacity == 0:
            return

        # Update existing key
        if key in self.key_map:
            node = self.key_map[key]
            node.value = value

            self.update_freq(node)
            return

        # Remove LFU node if full
        if len(self.key_map) >= self.capacity:
            lfu_list = self.freq_map[self.min_freq]

            node_to_remove = lfu_list.remove_last()

            del self.key_map[node_to_remove.key]

        # Insert new node
        new_node = Node(key, value)

        self.key_map[key] = new_node
        self.freq_map[1].add_node(new_node)

        self.min_freq = 1
