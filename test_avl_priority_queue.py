import unittest
from avl_priority_queue import AVLPriorityQueue


class TestAVLPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.pq = AVLPriorityQueue()

    def test_basic_operations(self):
        """Перевірка базових операцій та пустої черги."""
        self.assertIsNone(self.pq.peek())
        self.assertIsNone(self.pq.extract_max())

        self.pq.insert("low", 1)
        self.assertEqual(self.pq.peek(), ("low", 1))

        self.pq.insert("high", 10)
        self.assertEqual(self.pq.peek(), ("high", 10))

    def test_extract_max_ordering(self):
        """Перевірка правильного порядку вилучення елементів."""
        items = [("Task D", 5), ("Task A", 100), ("Task C", 10), ("Task B", 50)]
        for val, prio in items:
            self.pq.insert(val, prio)

        self.assertEqual(self.pq.extract_max(), ("Task A", 100))
        self.assertEqual(self.pq.extract_max(), ("Task B", 50))
        self.assertEqual(self.pq.extract_max(), ("Task C", 10))
        self.assertEqual(self.pq.extract_max(), ("Task D", 5))

    def test_equal_priorities(self):
        """Перевірка обробки елементів з однаковим пріоритетом."""
        self.pq.insert("First 10", 10)
        self.pq.insert("Second 10", 10)

        res1 = self.pq.extract_max()
        res2 = self.pq.extract_max()

        self.assertEqual(res1[1], 10)
        self.assertEqual(res2[1], 10)
        self.assertEqual({res1[0], res2[0]}, {"First 10", "Second 10"})

    def test_remove_by_value(self):
        """Перевірка додаткового завдання: видалення за значенням."""
        self.pq.insert("A", 10)
        self.pq.insert("B", 50)
        self.pq.insert("C", 100)

        self.assertTrue(self.pq.remove_by_value("B"))
        self.assertFalse(self.pq.remove_by_value("Z"))

        self.assertEqual(self.pq.extract_max(), ("C", 100))
        self.assertEqual(self.pq.extract_max(), ("A", 10))
        self.assertIsNone(self.pq.extract_max())


if __name__ == '__main__':
    unittest.main()