from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Путь к папке с данными, относительно расположения этого файла
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'Excel')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_file = request.form['selected_file']
        input_file_path = os.path.join(data_path, selected_file)
        # Здесь ваша логика обработки файла
        return render_template('index.html', files=os.listdir(data_path))
    else:
        file_list = [file for file in os.listdir(data_path) if file.endswith('.xlsx')]
        return render_template('index.html', files=file_list)

if __name__ == "__main__":
    app.run(debug=True)
