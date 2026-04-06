import unittest
import io
from contextlib import redirect_stdout

from balanced_tree import BinaryTree, is_tree_balanced, deserialize_postorder, top_view, print_tree


def n(val, left=None, right=None):
    return BinaryTree(val, left, right)


class TestPrivateFields(unittest.TestCase):
    def test_fields(self):
        node = BinaryTree(10)
        self.assertEqual(node.value, 10)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_setters(self):
        node = BinaryTree(1)
        node.left = BinaryTree(2)
        node.right = BinaryTree(3)
        self.assertEqual(node.left.value, 2)
        self.assertEqual(node.right.value, 3)


class TestIsBalanced(unittest.TestCase):
    def test_none(self):
        self.assertTrue(is_tree_balanced(None))

    def test_single(self):
        self.assertTrue(is_tree_balanced(n(1)))

    def test_balanced(self):
        root = n(1, n(2, n(4), n(5)), n(3))
        self.assertTrue(is_tree_balanced(root))

    def test_unbalanced(self):
        root = n(1, n(2, n(3)))
        self.assertFalse(is_tree_balanced(root))

    def test_diff_one(self):
        root = n(1, n(2, n(4)), n(3))
        self.assertTrue(is_tree_balanced(root))


class TestDeserialize(unittest.TestCase):
    def test_simple(self):
        data = [None, None, 4, None, None, 5, 2, None, None, 3, 1]
        root = deserialize_postorder(data)
        self.assertEqual(root.value, 1)
        self.assertEqual(root.left.value, 2)
        self.assertEqual(root.right.value, 3)
        self.assertEqual(root.left.left.value, 4)
        self.assertEqual(root.left.right.value, 5)

    def test_none_nodes(self):
        data = [None, None, None, 2, 1]
        root = deserialize_postorder(data)
        self.assertIsNone(root.left)
        self.assertEqual(root.right.value, 2)

    def test_single(self):
        data = [None, None, 42]
        root = deserialize_postorder(data)
        self.assertEqual(root.value, 42)

    def test_balanced_after(self):
        data = [None, None, 4, None, None, 5, 2, None, None, 3, 1]
        root = deserialize_postorder(data)
        self.assertTrue(is_tree_balanced(root))


class TestTopView(unittest.TestCase):
    def test_none(self):
        self.assertEqual(top_view(None), [])

    def test_single(self):
        self.assertEqual(top_view(n(1)), [1])

    def test_basic(self):
        root = n(1, n(2, n(4), n(5)), n(3))
        self.assertEqual(top_view(root), [4, 2, 1, 3])

    def test_right_chain(self):
        root = n(1, None, n(2, None, n(3)))
        self.assertEqual(top_view(root), [1, 2, 3])

    def test_hidden_node(self):
        root = n(1, n(2, None, n(4)), n(3))
        self.assertEqual(top_view(root), [2, 1, 3])


class TestLargeTree(unittest.TestCase):
    def setUp(self):
        self.root = n(10,
                      n(5, n(3, n(1), n(4)), n(7, None, None)),
                      n(20, n(15, None, n(17)), n(30, n(25), None))
                      )

    def test_balanced(self):
        self.assertTrue(is_tree_balanced(self.root))

    def test_top_view(self):
        result = top_view(self.root)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[-1], 30)
        self.assertIn(10, result)


class TestPrintTree(unittest.TestCase):
    def test_print_tree_horizontal_layout(self):
        # Дерево: 1 в центрі, 2 зліва, 3 справа (горизонталь)
        root = n(1, n(2), n(3))
        f = io.StringIO()
        with redirect_stdout(f):
            print_tree(root)
        output = f.getvalue()

        self.assertIn("2", output)
        self.assertIn("1", output)
        self.assertIn("3", output)

        lines = output.rstrip().split('\n')
        found_line = False
        for line in lines:
            if '2' in line and '1' in line and '3' in line:
                found_line = True
                self.assertTrue(line.find('2') < line.find('1') < line.find('3'),
                                "Вузли не розташовані у правильному горизонтальному порядку: 2 -> 1 -> 3")
        self.assertTrue(found_line, "Кореневі вузли не опинились на одній лінії")

    def test_print_tree_vertical_branches(self):
        # Перевірка правила: Праві діти йдуть вгору (Top), Ліві - вниз (Bottom)
        root = BinaryTree(3)
        root.left = BinaryTree(10)
        root.right = BinaryTree(11)

        # Робимо `root` гілкою, щоб застосувались правила зміщення по вертикалі
        mock_root = BinaryTree(1)
        mock_root.right = root

        f = io.StringIO()
        with redirect_stdout(f):
            print_tree(mock_root)
        lines = f.getvalue().rstrip().split('\n')

        idx_11 = idx_3 = idx_10 = -1
        for i, line in enumerate(lines):
            if '11' in line: idx_11 = i
            if '3' in line: idx_3 = i
            if '10' in line: idx_10 = i

        self.assertTrue(idx_11 < idx_3 < idx_10,
                        "Праві діти мають бути вище, а ліві нижче (відносно батька)")


if __name__ == '__main__':
    unittest.main()