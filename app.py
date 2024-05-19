from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from services.search_service import perform_search
from services.validation_service import validate_and_process
import os
import json
from config import DIRECTORY_LIST_ESP, DEPENDENT_VARIABLES, INDEPENDENT_VARIABLES

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

# Главная страница
@app.route('/')
def index():
    return render_template('index.html',
                           dependentVariables=DEPENDENT_VARIABLES,
                           independentVariables=INDEPENDENT_VARIABLES)

# Поиск файлов по запросу
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    files = perform_search(query, DIRECTORY_LIST_ESP)
    return jsonify(files)

# Валидация и обработка файла
@app.route('/validate', methods=['POST'])
def validate():
    filename = request.form.get('filename', '')
    response = validate_and_process(filename, DIRECTORY_LIST_ESP)
    if response.get("status") == "success":
        data_directory = 'temp_data'
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)  # Создаем директорию, если она не существует
        data_file = os.path.join(data_directory, filename)
        with open(data_file, 'w') as f:
            json.dump(response['data'], f)
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "Validation failed"})

# Анализ данных и предсказание
@app.route('/analyze', methods=['POST'])
def analyze_data():
    filename = request.form.get('filename')
    if not filename:
        return jsonify({"status": "error", "message": "Filename is required"})

    days_ahead = int(request.form.get('days_ahead', 1))  # Получаем days_ahead из формы запроса POST
    data_directory = 'temp_data'
    data_file = os.path.join(data_directory, filename)
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "Data not found"})

    df = pd.DataFrame(data)
    if not all(var in df.columns for var in DEPENDENT_VARIABLES + INDEPENDENT_VARIABLES):
        return jsonify({"status": "error", "message": "Data does not contain necessary columns"})

    X = df[INDEPENDENT_VARIABLES]
    y = df[DEPENDENT_VARIABLES[0]]

    # Обучение линейной регрессии
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    coefficients = dict(zip(X.columns, lr_model.coef_))

    # Обучение случайного леса
    rf_model = RandomForestRegressor()
    rf_model.fit(X, y)
    feature_importances = dict(zip(X.columns, rf_model.feature_importances_))

    # Обучение градиентного бустинга
    gb_model = GradientBoostingRegressor()
    gb_model.fit(X, y)

    # Получение последних данных для предсказаний
    X_pred = X.iloc[-1:].copy()
    predictions = []

    for _ in range(days_ahead):
        pred = gb_model.predict(X_pred)[0]
        predictions.append(pred)

        # Создание новых данных для следующего дня предсказания
        new_data = X_pred.iloc[-1:].copy()

        # Обновление зависимой переменной с предсказанным значением
        new_data[DEPENDENT_VARIABLES[0]] = pred

        # Обновление временных признаков или любых других зависимостей, если применимо
        if 'date' in new_data.columns:
            new_data['date'] = pd.to_datetime(new_data['date']) + pd.DateOffset(days=1)

        X_pred = pd.concat([X_pred, new_data[INDEPENDENT_VARIABLES]], ignore_index=True)

    mean = y.mean()
    std_dev = y.std()
    first_row_data = df.iloc[0]
    last_day_independent_vars = {var: first_row_data[var] for var in INDEPENDENT_VARIABLES}
    last_day_dependent_vars = {var: first_row_data[var] for var in DEPENDENT_VARIABLES}

    return jsonify({
        "status": "success",
        "coefficients": coefficients,
        "feature_importances": feature_importances,
        "predictions": predictions,  # Предсказания на нужное количество дней
        "mean": mean,
        "std_dev": std_dev,
        "last_day_independent_vars": last_day_independent_vars,
        "last_day_dependent_vars": last_day_dependent_vars
    })

if __name__ == '__main__':
    app.run(debug=True)
