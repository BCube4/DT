from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from services.search_service import perform_search
from services.validation_service import validate_and_process
import uuid
import os
import json
from config import DIRECTORY_LIST_ESP, DEPENDENT_VARIABLES, INDEPENDENT_VARIABLES

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

@app.route('/')
def index():
    return render_template('index.html',
                           dependentVariables=DEPENDENT_VARIABLES,
                           independentVariables=INDEPENDENT_VARIABLES)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    files = perform_search(query, DIRECTORY_LIST_ESP)
    return jsonify(files)

@app.route('/validate', methods=['POST'])
def validate():
    filename = request.form.get('filename', '')
    response = validate_and_process(filename, DIRECTORY_LIST_ESP)
    if response.get("status") == "success":
        session_id = uuid.uuid4().hex
        data_directory = 'temp_data'
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)  # Создаем директорию, если она не существует
        data_file = os.path.join(data_directory, f'{session_id}.json')
        with open(data_file, 'w') as f:
            json.dump(response['data'], f)

        response['session_id'] = session_id
        return jsonify(response)
    else:
        return jsonify({"status": "error", "message": "Validation failed"})

@app.route('/analyze', methods=['POST'])
def analyze_data():
    session_id = request.form.get('session_id')
    data_directory = 'temp_data'
    data_file = os.path.join(data_directory, f'{session_id}.json')
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "Session data not found"})

    df = pd.DataFrame(data)
    if not all(var in df.columns for var in DEPENDENT_VARIABLES + INDEPENDENT_VARIABLES):
        return jsonify({"status": "error", "message": "Data does not contain necessary columns"})

    days_ahead = int(request.args.get('days_ahead', 1))
    X = df[INDEPENDENT_VARIABLES]
    y = df[DEPENDENT_VARIABLES[0]]

    lr_model = LinearRegression()
    lr_model.fit(X, y)
    coefficients = dict(zip(X.columns, lr_model.coef_))

    rf_model = RandomForestRegressor()
    rf_model.fit(X, y)
    feature_importances = dict(zip(X.columns, rf_model.feature_importances_))

    gb_model = GradientBoostingRegressor()
    gb_model.fit(X, y)
    predictions = gb_model.predict(X.iloc[-days_ahead:])

    mean = y.mean()
    std_dev = y.std()
    first_row_data = df.iloc[0]
    last_day_independent_vars = {var: first_row_data[var] for var in INDEPENDENT_VARIABLES}
    last_day_dependent_vars = {var: first_row_data[var] for var in DEPENDENT_VARIABLES}

    return jsonify({
        "status": "success",
        "coefficients": coefficients,
        "feature_importances": feature_importances,
        "predictions": predictions.tolist(),
        "mean": mean,
        "std_dev": std_dev,
        "last_day_independent_vars": last_day_independent_vars,
        "last_day_dependent_vars": last_day_dependent_vars
    })

if __name__ == '__main__':
    app.run(debug=True)
