import json
import re
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

url = input('Input URL: ')

response_body_str =' '
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome() #desired_capabilities=caps
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
            if response_body:
                response_body_str = response_body

time.sleep(1)
# Extract page title for file name
page_title = driver.title
if not page_title:
    page_title = int(time.time())

# Save response bodies to a JSON file
file_name = f"{page_title}.json"

print(response_body_str)

response_body_str = response_body.replace("moraCallback(", "")
response_body_str = re.sub(r'\);$', '', response_body_str)

response_body_json = json.loads(response_body_str)
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(response_body_json, file, ensure_ascii=False, indent=2)

print(f"JSON responses saved to '{file_name}'")
driver.quit()
