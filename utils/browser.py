import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVE_NAME = 'chromedriver.exe'
CHROMEDRIVE_PATH = ROOT_PATH / 'bin' / CHROMEDRIVE_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if bool(int(os.environ.get('SELENIUM_HEADLESS', '1'))):
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CHROMEDRIVE_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('http://www.udemy.com/')
    time.sleep(5)
    browser.quit()
