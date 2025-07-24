from __future__ import annotations

import json
import os
from typing import Dict, Any

import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from config import EXCEL_DIR, DEPENDENT_VARIABLES, INDEPENDENT_VARIABLES
from services.search_service import perform_search
from services.validation_service import validate_and_process


def create_app() -> Flask:
    """Factory function to create and configure the Flask application."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'replace_this_with_a_random_value'

    @app.route('/')
    def index() -> str:
        return render_template(
            'index.html',
            dependentVariables=DEPENDENT_VARIABLES,
            independentVariables=INDEPENDENT_VARIABLES
        )

    @app.route('/search', methods=['POST'])
    def search() -> Any:
        query: str = request.form.get('query', '').strip()
        files = perform_search(query, EXCEL_DIR)
        return jsonify(files)

    @app.route('/validate', methods=['POST'])
    def validate() -> Any:
        filename: str = request.form.get('filename', '').strip()
        if not filename:
            return jsonify({'status': 'error', 'message': 'Имя файла не указано'})
        result = validate_and_process(filename, EXCEL_DIR)
        if result['status'] == 'success':
            data_dir = os.path.join(os.path.dirname(__file__), 'temp_data')
            os.makedirs(data_dir, exist_ok=True)
            json_path = os.path.join(data_dir, f"{filename}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result['data'], f, ensure_ascii=False)
            return jsonify({
                'status': 'success',
                'message': 'Файл успешно загружен',
                'data': result['data']
            })
        return jsonify({'status': 'error', 'message': result.get('message', 'Ошибка обработки')})

    @app.route('/analyze', methods=['POST'])
    def analyze() -> Any:
        filename: str = request.form.get('filename', '').strip()
        if not filename:
            return jsonify({'status': 'error', 'message': 'Имя файла не указано'})
        try:
            days_ahead = int(request.form.get('days_ahead', 1))
            if days_ahead <= 0:
                raise ValueError()
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Неверное значение days_ahead'})
        data_dir = os.path.join(os.path.dirname(__file__), 'temp_data')
        json_path = os.path.join(data_dir, f"{filename}.json")
        if not os.path.exists(json_path):
            return jsonify({'status': 'error', 'message': 'Данные не найдены'})
        with open(json_path, 'r', encoding='utf-8') as f:
            records = json.load(f)
        df = pd.DataFrame(records)
        missing_cols = [c for c in DEPENDENT_VARIABLES + INDEPENDENT_VARIABLES if c not in df.columns]
        if missing_cols:
            return jsonify({'status': 'error', 'message': f'Отсутствуют колонки: {", ".join(missing_cols)}'})
        X = df[INDEPENDENT_VARIABLES]
        y = df[DEPENDENT_VARIABLES[0]]
        lr_model = LinearRegression()
        lr_model.fit(X, y)
        coefficients: Dict[str, float] = dict(zip(INDEPENDENT_VARIABLES, lr_model.coef_))
        intercept: float = float(lr_model.intercept_)
        rf_model = RandomForestRegressor(random_state=42)
        rf_model.fit(X, y)
        feature_importances: Dict[str, float] = dict(zip(INDEPENDENT_VARIABLES, rf_model.feature_importances_))
        gb_model = GradientBoostingRegressor(random_state=42)
        gb_model.fit(X, y)
        last_features = X.iloc[-1].copy()
        predictions = []
        current_features = last_features.copy()
        for _ in range(days_ahead):
            next_val = float(gb_model.predict([current_features])[0])
            predictions.append(next_val)
            current_features = current_features
        mean_value = float(y.mean())
        std_dev = float(y.std()) if len(y) > 1 else 0.0
        last_day_independent_vars: Dict[str, float] = last_features.to_dict()
        last_day_dependent_vars: Dict[str, float] = {DEPENDENT_VARIABLES[0]: float(y.iloc[-1])}
        return jsonify({
            'status': 'success',
            'coefficients': coefficients,
            'intercept': intercept,
            'feature_importances': feature_importances,
            'predictions': predictions,
            'mean': mean_value,
            'std_dev': std_dev,
            'last_day_independent_vars': last_day_independent_vars,
            'last_day_dependent_vars': last_day_dependent_vars
        })

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
