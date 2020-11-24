import pandas as pd

from dbmanipulation import insert_to_db


def prepare_dataframe():
    file_path = 'data/export_LICZNIKI.csv'
    data_set = pd.read_csv(file_path, index_col='data')
    data_set.index = data_set.index.str.replace('.\d\d.\d\d.\d\d$', '')
    data_frame = pd.DataFrame(data_set)
    reversed_df = data_frame.iloc[::-1]
    return reversed_df

def insert_data_to_db(dataframe):
    for col in dataframe:
        if col == 'Średnia temp. (°C)':
            break
        for index, row in dataframe.iterrows():
            insert_to_db(index, col, row[col])
