import pandas as pd


def transform_excel_data(input_file_path):
    """
    Преобразует данные из Excel файла, группируя значения по состоянию и размещая их в отдельные колонки,
    сохраняя оригинальные названия столбцов.
    """
    df = pd.read_excel(input_file_path)

    # Подготовка DataFrame: удаляем первую колонку, если она не нужна, и сохраняем остальные названия
    df_cleaned = df.drop(columns=[df.columns[0]])

    transformed_df = pd.DataFrame()

    # Обходим каждое уникальное состояние
    for state in df_cleaned['Состояние'].unique():
        # Выбираем данные по текущему состоянию и удаляем столбец 'Состояние'
        state_df = df_cleaned[df_cleaned['Состояние'] == state].drop('Состояние', axis=1)
        # Преобразуем DataFrame в список, удаляем NaN значения
        numbers_list = state_df.values.flatten()
        numbers_list = numbers_list[~pd.isnull(numbers_list)]
        # Создаем новый столбец для каждого состояния с оригинальными названиями столбцов
        transformed_df[state] = pd.Series(numbers_list)

    # Заполняем пропуски пустыми строками
    transformed_df = transformed_df.fillna('')
    return transformed_df


def process_file(filename):
    try:
        transformed_data = transform_excel_data(filename)
        # Преобразование DataFrame в список словарей
        data_list = transformed_data.to_dict(orient='records')
        return {"status": "success", "data": data_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}
