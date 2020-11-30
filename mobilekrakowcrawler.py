import datetime
import re

from selenium import webdriver

from dbconnector import connect_to_db
from dbmanipulation import insert_to_db

#chrome webdriver options set to work online
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


#function returns list of counters urls
def get_counters_urls():
    driver.get("http://mobilnykrakow.pl/rowery/")
    counters = []
    page_source = driver.page_source
    page_source_lines = page_source.split('\n')
    for line in page_source_lines:
        if '<iframe src="https://eco-public.' in line:
            regs = re.search('(http.+)"\sw', line)

            counters.append(regs.group(1))
    # driver.quit()
    return counters


#function crawls webpage and returns list of street names with bicycle counters
def get_street_names():
    driver.get("http://mobilnykrakow.pl/rowery/")
    driver.implicitly_wait(5)
    streets = driver.find_elements_by_class_name('title.uppercase.pt-3.pl-3.mb-0') #finds street names in counter titles
    # driver.quit()
    return streets


#aggregate two lists into a dictionary (combine street name with counter url
def dict_of_streets_with_counters_urls(list_of_counters, list_of_street_names):
    streets_with_counters = {}
    j = 0
    for i in range(int(len(list_of_counters) / 2)):
        streets_with_counters['{}-YEAR'.format(list_of_street_names[i].text)] = list_of_counters[j] #url of cyclist from begining of the year
        streets_with_counters['{}-DAILY'.format(list_of_street_names[i].text)] = list_of_counters[j + 1] #daily cyclist count
        j += 2
    return streets_with_counters

#returns number of cyclist from the daily counters and insert data to DB
def get_values_from_counters(dict_of_counters):
    todays_the_day = datetime.date.today() - datetime.timedelta(days=1) #yesterday | day -1 !
    connection_to_db = connect_to_db()
    for count in dict_of_counters:
        driver.get(dict_of_counters[count])
        elem = driver.find_element_by_id('corps') #selenium finds value of cyclist in each counter
        insert_to_db(connection_to_db,todays_the_day, count, elem.text)
        print(count, ' ', elem.text)
    connection_to_db.close()
    driver.quit()

