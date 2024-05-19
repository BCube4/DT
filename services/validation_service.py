from utils.data_transformer import process_file
import os

def validate_and_process(filename, directory):
    """
    Выполняет валидацию и обработку указанного файла.

    Параметры:
    filename (str): Имя файла, который необходимо валидировать и обработать.
    directory (str): Директория, в которой находится файл.

    Возвращает:
    dict: Результат валидации и обработки файла.
    """
    file_path = os.path.join(directory, filename)  # Полный путь к файлу
    if os.path.exists(file_path):  # Проверка существования файла
        result = process_file(file_path)  # Обработка файла
        if result['status'] == 'success':
            return {"status": "success", "data": result['data']}  # Успешная обработка
        else:
            return {"status": "error", "message": result['message']}  # Ошибка при обработке
    else:
        return {"status": "error", "message": "Файл не найден"}  # Файл не найден
