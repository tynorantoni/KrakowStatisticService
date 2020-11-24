import datetime
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dbmanipulation import insert_to_db



def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1420,1080')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)





def get_counters_urls():
    driver = webdriver.Chrome(chrome_options=set_chrome_options())
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


def get_street_names():
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get("http://mobilnykrakow.pl/rowery/")
    driver.implicitly_wait(5)
    streets = driver.find_elements_by_class_name('title.uppercase.pt-3.pl-3.mb-0')
    # driver.quit()
    return streets


def dict_of_streets_with_counters_urls(list_of_counters, list_of_street_names):
    streets_with_counters = {}
    j = 0
    for i in range(int(len(list_of_counters) / 2)):
        streets_with_counters['{}-YEAR'.format(list_of_street_names[i].text)] = list_of_counters[j]
        streets_with_counters['{}-DAILY'.format(list_of_street_names[i].text)] = list_of_counters[j + 1]
        j += 2
    return streets_with_counters


def get_values_from_counters(dict_of_counters):
    driver = webdriver.Chrome(options=set_chrome_options())
    todays_the_day = datetime.today()
    for count in dict_of_counters:
        driver.get(dict_of_counters[count])
        elem = driver.find_element_by_id('corps')
        insert_to_db(todays_the_day, count, elem.text)
        print(count, ' ', elem.text)
    # driver.quit()

