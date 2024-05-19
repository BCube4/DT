import pandas as pd

def transform_excel_data(input_file_path):
    """
    Преобразует данные из Excel файла, группируя значения по состоянию и размещая их в отдельные колонки,
    сохраняя оригинальные названия столбцов.

    Параметры:
    input_file_path (str): Путь к входному Excel файлу.

    Возвращает:
    pd.DataFrame: Преобразованный DataFrame.
    """
    df = pd.read_excel(input_file_path)  # Чтение данных из Excel файла

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
    """
    Обрабатывает указанный файл, выполняя преобразование данных и возвращая результат.

    Параметры:
    filename (str): Имя файла для обработки.

    Возвращает:
    dict: Результат обработки файла, включающий статус и данные или сообщение об ошибке.
    """
    try:
        transformed_data = transform_excel_data(filename)  # Преобразование данных из Excel файла
        # Преобразование DataFrame в список словарей
        data_list = transformed_data.to_dict(orient='records')
        return {"status": "success", "data": data_list}  # Успешная обработка
    except Exception as e:
        return {"status": "error", "message": str(e)}  # Ошибка при обработке
