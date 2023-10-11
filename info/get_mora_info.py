import json
import re

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

url = input('Input URL: ')

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get(url)
pattern = r'https://cf\.mora\.jp/contents/package/(.*)/packageMeta\.jsonp.*$'
logs = driver.get_log('performance')
for item in logs:
    log = json.loads(item['message'])['message']
    if log['method'] == 'Network.responseReceived':
        url = log['params']['response']['url']
        match = re.match(pattern, url)
        if match:
            matched_content = match.group(1)
            request_id = log['params']['requestId']
            response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body']
            print(response_body)

driver.quit()
