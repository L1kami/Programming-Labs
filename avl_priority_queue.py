from typing import Any, Optional, Tuple, List


class Node:
    """Вузол AVL-дерева для черги з пріоритетами."""
    __slots__ = ['value', 'priority', 'left', 'right', 'height']

    def __init__(self, value: Any, priority: int):
        self.value = value
        self.priority = priority
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.height: int = 1


class AVLPriorityQueue:
    """Черга з пріоритетами на основі AVL-дерева.
    Ліва гілка: >= пріоритет батька. Права гілка: < пріоритет батька."""

    def __init__(self):
        self.root: Optional[Node] = None

    def _height(self, node: Optional[Node]) -> int:
        return node.height if node else 0

    def _balance_factor(self, node: Optional[Node]) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _fix_height(self, node: Node) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y: Node) -> Node:
        x = y.left
        if not x: return y
        y.left = x.right
        x.right = y
        self._fix_height(y)
        self._fix_height(x)
        return x

    def _rotate_left(self, x: Node) -> Node:
        y = x.right
        if not y: return x
        x.right = y.left
        y.left = x
        self._fix_height(x)
        self._fix_height(y)
        return y

    def _balance(self, node: Optional[Node]) -> Optional[Node]:
        if not node: return None
        self._fix_height(node)
        bf = self._balance_factor(node)

        if bf > 1 and node.left:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1 and node.right:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value: Any, priority: int) -> None:
        """1. Вставка елемента до черги."""
        self.root = self._insert(self.root, value, priority)

    def _insert(self, node: Optional[Node], value: Any, priority: int) -> Node:
        if not node:
            return Node(value, priority)
        if priority >= node.priority:
            node.left = self._insert(node.left, value, priority)
        else:
            node.right = self._insert(node.right, value, priority)
        return self._balance(node)

    def peek(self) -> Optional[Tuple[Any, int]]:
        """3. Перегляд черги без її зміни."""
        if not self.root: return None
        curr = self.root
        while curr.left:
            curr = curr.left
        return curr.value, curr.priority

    def extract_max(self) -> Optional[Tuple[Any, int]]:
        """2. Видалення та повернення елемента з найвищим пріоритетом."""
        if not self.root: return None
        extracted: List[Tuple[Any, int]] = []
        self.root = self._extract_leftmost(self.root, extracted)
        return extracted[0] if extracted else None

    def _extract_leftmost(self, node: Node, extracted: List[Tuple[Any, int]]) -> Optional[Node]:
        if not node.left:
            extracted.append((node.value, node.priority))
            return node.right
        node.left = self._extract_leftmost(node.left, extracted)
        return self._balance(node)

    def remove_by_value(self, value: Any) -> bool:
        """Додаткове завдання: Видалення довільного елемента за значенням."""
        if not self.root: return False
        self.root, deleted = self._remove_by_value(self.root, value)
        return deleted

    def _get_leftmost(self, node: Node) -> Node:
        while node.left: node = node.left
        return node

    def _remove_by_value(self, node: Optional[Node], value: Any) -> Tuple[Optional[Node], bool]:
        if not node: return None, False

        deleted = False
        if node.value == value:
            deleted = True
            if not node.left: return node.right, True
            if not node.right: return node.left, True

            successor = self._get_leftmost(node.right)
            node.value, node.priority = successor.value, successor.priority
            node.right, _ = self._remove_by_value(node.right, successor.value)
        else:
            node.left, deleted = self._remove_by_value(node.left, value)
            if not deleted:
                node.right, deleted = self._remove_by_value(node.right, value)

        if not deleted: return node, False
        return self._balance(node), True


if __name__ == "__main__":
    print("--- Демонстрація роботи черги з пріоритетами ---")
    pq = AVLPriorityQueue()

    tasks = [("Помити посуд", 2), ("Врятувати світ", 100), ("Випити кави", 50), ("Зробити лабу", 75)]
    for val, prio in tasks:
        pq.insert(val, prio)
        print(f"Додано: {val} (Пріоритет: {prio})")

    print(f"\nНайвищий пріоритет зараз (peek): {pq.peek()}")

    print("\nВидаляємо 'Випити кави' (демонстрація дод. завдання)...")
    pq.remove_by_value("Випити кави")

    print("\nДістаємо всі елементи по черзі (extract_max):")
    while True:
        item = pq.extract_max()
        if not item: break
        print(item)