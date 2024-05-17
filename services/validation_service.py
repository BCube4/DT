from utils.data_transformer import process_file
import os

def validate_and_process(filename, directory):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        result = process_file(file_path)
        if result['status'] == 'success':
            return {"status": "success", "data": result['data']}
        else:
            return {"status": "error", "message": result['message']}
    else:
        return {"status": "error", "message": "Файл не найден"}
