import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import json
import os

def perform_regression(df, dependent_var, independent_vars):
    try:
        X = df[independent_vars]
        y = df[dependent_var]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        feature_importances = model.feature_importances_
        return dict(zip(independent_vars, feature_importances))
    except Exception as e:
        print(f"Error in perform_regression: {str(e)}")
        return None


def save_coefficients(coefficients, filename="/Corfficients_parametrs/coefficients.json"):
    # Создаем директорию, если она не существует
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as file:
        json.dump(coefficients, file)
