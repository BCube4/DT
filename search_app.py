from flask import Blueprint, request, jsonify
import os

# Create a Blueprint
search_bp = Blueprint('search', __name__)

# Function to search files in a directory
def search_files(query, path):
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if query.lower() in file.lower():
                results.append(os.path.join(root, file))
    return results

@search_bp.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('query', 'http://127.0.0.1:5000/')
    path = request.args.get('path', 'D:\App\PyCharm Community Edition 2024.1.1\PycharmProjects\DT\Excel')  # Установите нужный путь
    suggestions = []
    if query:
        for root, dirs, files in os.walk(path):
            for file in files:
                if query.lower() in file.lower():
                    suggestions.append(file)
                    if len(suggestions) >= 10:  # Limit to 10 suggestions
                        break
            if len(suggestions) >= 10:
                break
    return jsonify(suggestions)

