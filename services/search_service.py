import os
from typing import List

ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.xlsm'}

def perform_search(query: str, directory: str) -> List[str]:
    """Поиск файлов по префиксу в указанной директории."""
    results: List[str] = []
    if not os.path.isdir(directory):
        return results
    query_lower = query.lower()
    for name in os.listdir(directory):
        ext = os.path.splitext(name)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            if not query_lower or name.lower().startswith(query_lower):
                results.append(name)
    return results
