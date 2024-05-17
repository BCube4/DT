import os

def perform_search(query, directory):
    valid_extensions = ('.xlsx', '.xls', '.xlsm', '.xlsb', '.xml', '.xltx', '.csv')
    files = [f for f in os.listdir(directory) if f.endswith(valid_extensions) and f.lower().startswith(query.lower())]
    return files
