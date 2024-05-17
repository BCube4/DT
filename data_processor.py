import pandas as pd

def transform_excel_data(input_file_path):
    df = pd.read_excel(input_file_path)
    df_cleaned = df.drop(columns=[df.columns[0]])
    transformed_df = pd.DataFrame()
    for state in df_cleaned['Состояние'].unique():
        state_df = df_cleaned[df_cleaned['Состояние'] == state].drop('Состояние', axis=1)
        numbers_list = state_df.values.flatten()
        numbers_list = numbers_list[~pd.isnull(numbers_list)]
        transformed_df[state] = pd.Series(numbers_list)
    transformed_df = transformed_df.fillna('')
    return transformed_df
