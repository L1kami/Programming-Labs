from collections import deque


class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.__value = value
        self.__left = left
        self.__right = right

    @property
    def value(self):
        return self.__value

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, node):
        self.__left = node

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, node):
        self.__right = node


def get_height(node: BinaryTree) -> int:
    if node is None:
        return 0
    lh = get_height(node.left)
    if lh == -1:
        return -1
    rh = get_height(node.right)
    if rh == -1:
        return -1
    if abs(lh - rh) > 1:
        return -1
    return max(lh, rh) + 1


def is_tree_balanced(node: BinaryTree) -> bool:
    return get_height(node) != -1


def build_level_order(data: list) -> BinaryTree:
    """Будує повне бінарне дерево з масиву (за рівнями)."""
    if not data:
        return None
    nodes = [BinaryTree(val) for val in data]
    for i in range(len(nodes)):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < len(nodes):
            nodes[i].left = nodes[left_idx]
        if right_idx < len(nodes):
            nodes[i].right = nodes[right_idx]
    return nodes[0]


def deserialize_postorder(data: list) -> BinaryTree:
    """Десеріалізує дерево з post-order обходу, де None позначає відсутність вузла."""
    if not data:
        return None

    # Створюємо копію, щоб не змінювати оригінальний масив
    data_copy = data.copy()

    def helper():
        if not data_copy:
            return None

        # Дістаємо елементи з кінця (в post-order корінь знаходиться в самому кінці)
        val = data_copy.pop()

        if val is None:
            return None

        node = BinaryTree(val)
        # Оскільки ми йдемо з кінця post-order (L, R, Root),
        # після Root ми зустрінемо праве піддерево, а потім ліве.
        node.right = helper()
        node.left = helper()
        return node

    return helper()


def top_view(root: BinaryTree) -> list:
    if root is None:
        return []
    hd_map = {}
    queue = deque([(root, 0)])
    while queue:
        node, hd = queue.popleft()
        if hd not in hd_map:
            hd_map[hd] = node.value
        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))
    return [hd_map[k] for k in sorted(hd_map)]


def print_tree(root: BinaryTree):
    if root is None:
        return

    # 1. Знаходимо максимальну глибину дерева для розрахунку відступів
    def get_max_depth(node):
        if not node: return 0
        return max(get_max_depth(node.left), get_max_depth(node.right)) + 1

    max_d = get_max_depth(root)

    coords = {}
    XS = 6
    YS = 2

    # 2. Призначаємо координати з динамічним кроком по Y
    def assign_coords(node, x, y, direction, is_root=False, depth=0):
        if node is None:
            return

        coords[id(node)] = (x, y, node.value)

        # Динамічний відступ: чим ближче до кореня, тим ширше розходяться гілки по вертикалі
        y_step = 2 ** max(0, max_d - depth - 2)

        if is_root:
            assign_coords(node.left, x - 1, y, -1, is_root=False, depth=depth + 1)
            assign_coords(node.right, x + 1, y, 1, is_root=False, depth=depth + 1)
        else:
            assign_coords(node.left, x + direction, y + y_step, direction, is_root=False, depth=depth + 1)
            assign_coords(node.right, x + direction, y - y_step, direction, is_root=False, depth=depth + 1)

    assign_coords(root, 0, 0, 0, is_root=True)

    canvas = {}

    def put_char(col, row, char):
        if row not in canvas:
            canvas[row] = {}
        # Не затираємо вже існуючі символи іншими лініями
        if col in canvas[row] and canvas[row][col] not in [' ', '-', '/', '\\']:
            return
        canvas[row][col] = char

    def put_str(col, row, s):
        if row not in canvas:
            canvas[row] = {}
        for i, c in enumerate(s):
            canvas[row][col + i] = c

    # 3. Відмальовування вузлів та з'єднань
    def draw(node_id, node):
        x, y, val = coords[node_id]
        col = x * XS
        row = y * YS

        val_str = str(val)
        start_col = col - len(val_str) // 2
        put_str(start_col, row, val_str)

        children = []
        if node.left:
            children.append((id(node.left), node.left))
        if node.right:
            children.append((id(node.right), node.right))

        for child_id, child_node in children:
            nx, ny, _ = coords[child_id]
            ncol = nx * XS
            nrow = ny * YS

            if row == nrow:  # Горизонтальна лінія (від кореня 1 до 2 та 3)
                for c in range(min(col, ncol) + 2, max(col, ncol) - 1):
                    put_char(c, row, '-')
            else:  # Діагональна лінія (всі інші зв'язки)
                char = '\\' if (ncol > col and nrow > row) or (ncol < col and nrow < row) else '/'

                r_start, r_end = (row, nrow) if row < nrow else (nrow, row)
                c_start, c_end = (col, ncol) if row < nrow else (ncol, col)

                r_diff = r_end - r_start
                c_diff = c_end - c_start

                # Малюємо безперервну діагональну лінію через усі пусті рядки
                for i in range(1, r_diff):
                    cur_r = r_start + i
                    cur_c = int(round(c_start + c_diff * (i / r_diff)))
                    put_char(cur_c, cur_r, char)

            draw(child_id, child_node)

    draw(id(root), root)

    if not canvas:
        return

    min_row = min(canvas.keys())
    max_row = max(canvas.keys())

    all_cols = [c for r in canvas.values() for c in r.keys()]
    if not all_cols:
        return
    min_col = min(all_cols)
    max_col = max(all_cols)

    # 4. Вивід у термінал
    for r in range(min_row, max_row + 1):
        if r in canvas:
            line = "".join(canvas[r].get(c, ' ') for c in range(min_col, max_col + 1))
            print(line.rstrip())
        else:
            print()


if __name__ == '__main__':
    def postorder(node):
        if node is None:
            return []
        return postorder(node.left) + postorder(node.right) + [node.value]


    # Дані від 1 до 20
    data = list(range(1, 21))
    root = build_level_order(data)

    print('=== Дерево (Рознесене) ===')
    print_tree(root)

    print('\n=== Post-order ===')
    print(' -> '.join(str(v) for v in postorder(root)))

    print('\n=== Top View ===')
    print(' -> '.join(str(v) for v in top_view(root)))

    print('\n=== Збалансоване ===')
    print(is_tree_balanced(root))