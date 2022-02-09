import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager


os.environ['WDM_LOG_LEVEL'] = '0'
basepath = os.path.dirname(os.path.abspath(__file__))
filename = "output.csv"


def get_chrome_driver():
    # Chrome options
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-logging')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.maximize_window()

    return driver


def make_soup(page_source):
    soup = BeautifulSoup(page_source, "html5lib")
    return soup


def wait_for_element(driver, xpath, timeout=40):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
        (By.XPATH, xpath)))


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def write_to_txt(content):
    with open("html.txt", "w") as f:
        f.write(content)