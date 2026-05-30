from typing import List, Dict


def _build_bad_character_table(needle: str) -> Dict[str, int]:
    """
    Будує таблицю зміщень для правила поганого символу.

    Приймає шуканий рядок і повертає словник, де ключем є символ,
    а значенням - індекс його останнього входження у рядок.
    """
    table = {}
    for i, char in enumerate(needle):
        table[char] = i
    return table


def boyer_moore_search(haystack: str, needle: str) -> List[int]:
    """
    Шукає всі входження підрядка у рядок за алгоритмом Боєра-Мура.

    Приймає довільний текст (haystack) та шуканий рядок (needle).
    Використовує евристику поганого символу для оптимізації пошуку.
    Повертає список початкових індексів усіх знайдених входжень.
    """
    if not needle or not haystack:
        return []

    needle_len = len(needle)
    haystack_len = len(haystack)
    bad_char_table = _build_bad_character_table(needle)
    occurrences = []

    shift = 0
    while shift <= (haystack_len - needle_len):
        j = needle_len - 1

        while j >= 0 and needle[j] == haystack[shift + j]:
            j -= 1

        if j < 0:
            occurrences.append(shift)
            if shift + needle_len < haystack_len:
                next_char = haystack[shift + needle_len]
                shift += needle_len - bad_char_table.get(next_char, -1)
            else:
                shift += 1
        else:
            mismatched_char = haystack[shift + j]
            char_last_index = bad_char_table.get(mismatched_char, -1)
            shift += max(1, j - char_last_index)

    return occurrences