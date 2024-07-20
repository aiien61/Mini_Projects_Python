from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional, Any


class Node(ABC):
    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.next: 'Node' = None


class LinkedList:
    def __init__(self, node: Node = None):
        self.head: Node = node if node is not None else None
        self.tail: Node = node if node is not None else None
        self.length: int = 1 if node is not None else 0

    def append(self, node: Node) -> bool:
        if self.length == 0:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1
        return True

    def pop_first(self) -> Node:
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return temp


class Answer(Enum):
    TRUE = auto()
    FALSE = auto()


class QuestionNode(Node):
    def __init__(self, q_text: str, q_answer: Answer):
        self.text: str = q_text
        self.answer: Answer = q_answer
        self.next = None
