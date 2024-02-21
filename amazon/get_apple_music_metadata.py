#!/usr/bin/env python3
import json
import re
import time
import sys

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

if len(sys.argv) < 2:
    print("Missing URL argument.")
    sys.exit(1)

url = ' '.join(sys.argv[1:])

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome()
driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 10)
play_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'play-button')))
driver.find_element(By.CLASS_NAME, 'play-button').click()

time.sleep(5)

pattern = r'https://amp-api\.music\.apple\.com/v1/catalog/jp/albums/(.*)\?l=ja'
logs = driver.get_log('performance')

response_body_str = ''

for item in logs:
    log = json.loads(item['message'])['message']
    if log['method'] == 'Network.responseReceived':
        url = log['params']['response']['url']
        match = re.match(pattern, url)
        if match:
            matched_content = match.group(1)
            request_id = log['params']['requestId']
            try:
                response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body']
                if response_body:
                    response_body_str = response_body
            except exceptions.WebDriverException:
                print('response body is null')

time.sleep(5)

"""
# Extract page title for file name
page_title = driver.title
if not page_title:
    page_title = int(time.time())
"""

# Save response body to a JSON file
file_name = f"{int(time.time())}.json"

response_body_json = json.loads(response_body_str)
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(response_body_json, file, ensure_ascii=False, indent=2)

print(f"JSON responses saved to '{file_name}'")
driver.quit()
