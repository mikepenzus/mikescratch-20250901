import csv
from datetime import *
from time import *
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def show_timestamp():
    print(datetime.now())


show_timestamp()
service = Service()
options = webdriver. ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument('disable-notifications')
options.add_argument("window-size=1920,1080")
browser = webdriver.Chrome(
    service=service,
    options=options
)
show_timestamp()
browser.get("https://www.google.com")
show_timestamp()
wait = WebDriverWait(browser, 20)

wait.until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Accept all']"))).click()
search = browser.find_element(By.NAME, 'q')
show_timestamp()
search.click()
show_timestamp()
search.send_keys('"Igor Makarov" and "Vladimir Putin" and ICIJ')
search.send_keys(Keys.RETURN)
show_timestamp()
sleep(5)
anchors = browser.find_elements(By.TAG_NAME, "a")

sites_to_skip = [re.compile(regexp) for regexp in [r'https://.*\.google\.com']]
sites_to_keep = []
for anchor in anchors:
    href = anchor.get_property('href')
    text = anchor.text
    if text and href:
        for site_to_skip in sites_to_skip:
            if not site_to_skip.search(href):
                text = text.replace("\n", " ").replace("\r", " ")
                site_to_keep = {'href': href, 'text': text}
                sites_to_keep.append(site_to_keep)
print(sites_to_keep)
show_timestamp()

with open('links.csv', 'w') as output_csv_file:
    writer = csv.DictWriter(output_csv_file, fieldnames=['href', 'text'], delimiter=',')
    writer.writeheader()
    writer.writerows(sites_to_keep)

browser.quit()
show_timestamp()
