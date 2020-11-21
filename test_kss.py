import datetime

import psycopg2
import pytest

import pingpong
from dbconnector import connect_to_db



class TestClass:

    @pytest.fixture()
    def setUp(self):
        connection = connect_to_db()
        yield connection
        connection.close()

    def test_connect_to_db(self, setUp):

        cur = setUp.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        assert db_version is not None

    def test_create_table(self, setUp):
        try:
            cur = setUp.cursor()

            cur.execute('''CREATE TABLE krakow_data_test_table
            (id SERIAL PRIMARY KEY NOT NULL,
            date_of_count DATE,
            street_name TEXT,
            day_cnt VarChar(10));'''
                        )

            setUp.commit()
            query = cur.execute('SELECT * FROM krakow_data_test_table;')
            assert query == 'None'

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            cur.close()


    def test_insert_to_db(self, setUp):
        date = datetime.date(2019, 12, 24)
        try:
            cur = setUp.cursor()

            cur.execute('''INSERT INTO krakow_data_test_table
            (date_of_count, street_name, day_cnt) VALUES 
            ({},{},{});'''.format(date, "'test_street'", 666)
                        )

            setUp.commit()

            query = cur.execute('SELECT day_cnt FROM brussels_data_test_table;')
            assert query == 666

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            cur.close()


    def test_drop_table(self, setUp):
        with pytest.raises(psycopg2.DatabaseError):

            cur = setUp.cursor()

            cur.execute('''DROP TABLE krakow_data_test_table;''')
            setUp.commit()
            cur.execute('SELECT * FROM krakow_data_test_table;')


    @pytest.fixture()
    def setUpFlask(self):
        pingpong.app.testing = True

        with pingpong.app.test_client() as client:
            with pingpong.app.app_context():
                pingpong.start()
            yield client

    def test_pong(self,setUpFlask):
        value = setUpFlask.get('/ping')
        assert '200' in str(value)



if __name__ == '__main__':
    pytest.main()

