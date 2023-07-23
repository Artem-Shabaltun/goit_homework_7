import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str: # отримуємо назву файлу строкою та повертаємо нормалізовану назву також строкою
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '.', t_name) # при нормалізації найменування файлу, ми перебираємо його назву повністю, неприпустимі символи міняємо на "_" і записуємо "." щоб проігнорувати, та залишити як оригінальний символ
    return t_name # повертаємо нормалізоване ім'я файлу