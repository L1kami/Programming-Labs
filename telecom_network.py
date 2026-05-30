import csv


class DisjointSetUnion:
    """
    Клас для реалізації структури даних системи неперетинних множин (Disjoint Set Union).
    Використовується для ефективного знаходження циклів у графі під час побудови
    мінімального кістякового дерева.
    """

    def __init__(self, vertices: set):
        """
        Ініціалізує структуру для заданої множини вершин.
        Кожна вершина спочатку є коренем власної підмножини.
        """
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item: str) -> str:
        """
        Знаходить корінь множини, до якої належить елемент,
        використовуючи оптимізацію стиснення шляху для прискорення наступних запитів.
        """
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x: str, y: str) -> bool:
        """
        Об'єднує дві множини, до яких належать елементи x та y.
        Повертає True, якщо об'єднання відбулося успішно, і False, якщо елементи
        вже належать до однієї множини (утворення циклу).
        """
        xroot = self.find(x)
        yroot = self.find(y)

        if xroot != yroot:
            if self.rank[xroot] < self.rank[yroot]:
                self.parent[xroot] = yroot
            elif self.rank[xroot] > self.rank[yroot]:
                self.parent[yroot] = xroot
            else:
                self.parent[yroot] = xroot
                self.rank[xroot] += 1
            return True

        return False


def calculate_minimum_cable_length(csv_file_path: str) -> int:
    """
    Обчислює мінімальну загальну довжину оптоволоконного кабелю для
    з'єднання всіх телекомунікаційних колодязів за допомогою алгоритму Крускала.

    Читає дані з CSV-файлу, де кожен рядок містить два ідентифікатори
    колодязів та відстань між ними.

    Повертає:
        int: Мінімальна сумарна довжина кабелю. Повертає -1, якщо граф є
        незв'язним (існують колодязі, до яких неможливо провести мережу).
    """
    edges = []
    vertices = set()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            u = row[0].strip()
            v = row[1].strip()
            weight = int(row[2].strip())

            edges.append((weight, u, v))
            vertices.add(u)
            vertices.add(v)

    if not vertices:
        return 0

    dsu = DisjointSetUnion(vertices)
    edges.sort(key=lambda x: x[0])

    mst_weight = 0
    edges_used = 0

    for weight, u, v in edges:
        if dsu.union(u, v):
            mst_weight += weight
            edges_used += 1

    if edges_used != len(vertices) - 1:
        return -1

    return mst_weight