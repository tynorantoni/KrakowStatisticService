import pandas as pd

from dbconnector import connect_to_db
from dbmanipulation import insert_to_db, create_table


# get data from csv file
def prepare_dataframe():
    file_path = 'data/export_LICZNIKI_2.csv'
    data_set = pd.read_csv(file_path, index_col='data')
    data_set.index = data_set.index.str.replace('.\d\d.\d\d.\d\d$', '')  # format date of count
    data_frame = pd.DataFrame(data_set).fillna(0) #replace nan with 0
    reversed_df = data_frame.iloc[::-1]  # reverse to get data from oldest dates
    return reversed_df


# insert all archive data from csv file
def insert_data_to_db(dataframe):
    print('started')
    conn = connect_to_db()
    for col in dataframe:
        print('working...')
        if col == 'Średnia temp. (°C)':  # if loop finds "average temp." column it stops
            break
        for index, row in dataframe.iterrows():
            print(index)
            insert_to_db(conn,index, col, row[col])
            conn.commit()
    conn.close()
    print('ended!')


