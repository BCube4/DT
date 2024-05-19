import os

def perform_search(query, directory):
    """
    Выполняет поиск файлов в указанной директории, соответствующих запросу и допустимым расширениям.

    Параметры:
    query (str): Строка запроса для поиска файлов.
    directory (str): Директория, в которой будет выполняться поиск.

    Возвращает:
    list: Список файлов, соответствующих критериям поиска.
    """
    valid_extensions = ('.xlsx', '.xls', '.xlsm', '.xlsb', '.xml', '.xltx', '.csv')  # Допустимые расширения файлов
    files = [f for f in os.listdir(directory)
             if f.endswith(valid_extensions) and f.lower().startswith(query.lower())]  # Фильтрация файлов по запросу и расширениям
    return files
