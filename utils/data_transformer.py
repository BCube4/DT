from __future__ import annotations

import pandas as pd
from typing import Any, Dict


def transform_excel_data(input_file_path: str) -> pd.DataFrame:
    """
    Поворачивает Excel‑таблицу с колонкой «Состояние» в формат «один столбец = одна переменная». Пропущенные значения заполняются нулями.
    """
    df = pd.read_excel(input_file_path, sheet_name=0)
    # удаляем первый безымянный столбец
    if df.columns.size > 0 and (df.columns[0] == 'Unnamed: 0' or df.columns[0].startswith('Unnamed')):
        df = df.drop(columns=[df.columns[0]])
    if 'Состояние' in df.columns:
        df_cleaned = df.drop(columns=[col for col in df.columns if col == df.columns[0] and col != 'Состояние'])
        transformed = pd.DataFrame()
        for state in df_cleaned['Состояние'].dropna().unique():
            state_df = df_cleaned[df_cleaned['Состояние'] == state].drop('Состояние', axis=1)
            values = state_df.values.flatten()
            values = values[pd.notna(values)]
            transformed[state] = pd.Series(values)
        transformed = transformed.fillna(0)
        return transformed
    else:
        return df.fillna(0)


def process_file(file_path: str) -> Dict[str, Any]:
    """
    Чтение CSV или Excel и возврат данных в виде списка словарей.
    """
    try:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path).fillna(0)
        else:
            df = transform_excel_data(file_path)
        data_list = df.to_dict(orient='records')
        return {'status': 'success', 'data': data_list}
    except Exception as exc:
        return {'status': 'error', 'message': str(exc)}
