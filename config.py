import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Папка с исходными файлами Excel/CSV
EXCEL_DIR = os.path.join(BASE_DIR, 'Excel')

# Зависимая переменная (целевая)
DEPENDENT_VARIABLES = ['Тдвиг ТМ']

# Независимые переменные (признаки)
INDEPENDENT_VARIABLES = [
    'Tраб (ТМ)',
    'Qн',
    'Обв',
    'КВЧ',
    'Нд',
    'Рбуф',
    'Рлин',
    'Рзатр',
    'Рприем',
    'Рэцн ТМ',
    'Темп. ПЭД',
    'Qж',
    'Fвращ',
    'Ток',
]
