import os
from typing import Dict, Any

from utils.data_transformer import process_file


def validate_and_process(filename: str, directory: str) -> Dict[str, Any]:
    """Проверка существования файла и его обработка."""
    full_path = os.path.join(directory, filename)
    if not os.path.exists(full_path):
        return {'status': 'error', 'message': 'Файл не найден'}
    return process_file(full_path)
