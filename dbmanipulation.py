import psycopg2

from dbconnector import connect_to_db

#basic database functions: create, drop, insert


def create_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''CREATE TABLE krakow_data
        (id SERIAL PRIMARY KEY NOT NULL,
        date_of_count DATE,
        street_name TEXT,
        day_cnt VarChar(10));'''
                    )

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()


def drop_table():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute('''DROP TABLE krakow_data;''')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cur.close()
        conn.close()


def insert_to_db(connection, date_of_counting, street_name, total_cyclists):
    try:
        cur = connection.cursor()

        cur.execute('''INSERT INTO krakow_data 
        (date_of_count, street_name, day_cnt) VALUES 
        ('{}','{}',{});'''.format(date_of_counting, street_name, total_cyclists)
                    )
        # connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


