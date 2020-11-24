import datetime
import os
import re

import psycopg2
import pytest
from selenium.webdriver.chrome.options import Options

from archivedata import prepare_dataframe
from dbconnector import connect_to_db
from selenium import webdriver

from mobilekrakowcrawler import get_street_names, get_counters_urls, dict_of_streets_with_counters_urls, \
    set_chrome_options


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1420,1080')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)



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

            query = cur.execute('SELECT day_cnt FROM krakow_data_test_table;')
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

    def test_prepare_dataframe(self):
        data_columns = prepare_dataframe().columns
        assert "wielicka" in data_columns
        assert "dworzec główny" in data_columns
        assert "Strzelców" not in data_columns

    def test_get_counters_urls(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': os.getcwd(),
            'download.prompt_for_download': False,
        })
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("http://mobilnykrakow.pl/rowery/")
        counters = []
        page_source = driver.page_source
        page_source_lines = page_source.split('\n')
        for line in page_source_lines:
            if '<iframe src="https://eco-public.' in line:
                regs = re.search('(http.+)"\sw', line)

                counters.append(regs.group(1))
        # driver.quit()
        assert 'eco-public' in counters[3]
        assert len(counters) >= 1

    def test_get_street_names(self):
        driver = webdriver.Chrome(options=set_chrome_options())
        data_columns = prepare_dataframe().columns
        driver.get("http://mobilnykrakow.pl/rowery/")
        driver.implicitly_wait(5)
        streets = driver.find_elements_by_class_name('title.uppercase.pt-3.pl-3.mb-0')
        # driver.quit()
        j = 0
        for street in streets:
            assert street.text.lower() in data_columns[j]
            j += 1
            if "wielicka" in data_columns[j]:
                break

    def test_dict_of_streets_with_counters_urls(self):
        list_of_counters = get_counters_urls()
        list_of_street_names = get_street_names()
        streets_with_counters = {}
        url_check = 'https://eco-public.com/eco-widget/total.jsp?id=100034392&amp;w=100&amp;h=30&amp;c=000000&amp;bg=e33488&amp;lang=se&amp;font=arial&amp;lang=pl'
        j = 0
        for i in range(int(len(list_of_counters) / 2)):
            streets_with_counters['{}-YEAR'.format(list_of_street_names[i].text)] = list_of_counters[j]
            streets_with_counters['{}-DAILY'.format(list_of_street_names[i].text)] = list_of_counters[j + 1]
            j += 2
        print(streets_with_counters['WIELICKA-YEAR'])
        print(url_check)
        assert streets_with_counters['WIELICKA-YEAR'] == url_check

    def test_get_values_from_counters(self):
        driver = webdriver.Chrome()
        dict_of_counters = dict_of_streets_with_counters_urls(
            get_counters_urls(),
            get_street_names()
        )
        todays_the_day = datetime.date.today()
        for count in dict_of_counters:
            driver.get(dict_of_counters[count])
            elem = driver.find_element_by_id('corps')

            assert elem.text is not None
            assert int((elem.text).replace(" ", "")) >= 0
        assert isinstance(todays_the_day, datetime.date)

    # @pytest.fixture()
    # def setUpFlask(self):
    #     main.app.testing = True
    #
    #     with main.app.test_client() as client:
    #         with main.app.app_context():
    #             main.start()
    #         yield client
    #
    # def test_pong(self,setUpFlask):
    #     value = setUpFlask.get('/ping')
    #     assert '200' in str(value)


if __name__ == '__main__':
    pytest.main()
