import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def calculate_regression(df):
    # Заглушка для независимых переменных и целевой переменной
    X = df[['TрабТМ', 'Qн', 'Обв', 'КВЧ', 'Нд', 'Рбуф', 'Рлин', 'Рзатр', 'Рприем', 'РэцнТМ', 'ТемпПЭД', 'Qж', 'Fвращ', 'Ток']]  # предполагаем, что эти колонки есть в df
    y = df['TдвигТМ']  # целевая переменная

    # Создаем и тренируем модель
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Получаем важность признаков
    feature_importances = model.feature_importances_
    coefficients = dict(zip(X.columns, feature_importances))

    # Составляем формулу в виде строки
    formula = " + ".join([f"{coeff:.3f}*{name}" for name, coeff in coefficients.items()])
    return "y = " + formula
