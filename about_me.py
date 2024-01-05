"""
Created on Fri May 19 15:44:36 2023

@author: teriyakibeefdipper

Purpose: to scrape our own Yahoo store data for transferring to Shopee
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import re
import urllib.request

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

url = 'https://tw.bid.yahoo.com/booth/Y77********'

yahoo = requests.get(url, headers=header).text
soup = BeautifulSoup(yahoo, 'html.parser')
data = soup.find(id='isoredux-data').text
pattern = r'window\.ISO_REDUX_DATA\s*=\s*(\{.*?\});'
match = re.search(pattern, data, re.DOTALL)
if match:
    json_string = match.group(1)
else:
    json_string = None
# print(data)
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4)
json_obj = json.loads(json_string)
about_me = json_obj['booth']['aboutme']
about_me = BeautifulSoup(about_me, 'html.parser')
about_me = ' '.join(about_me.stripped_strings)
name = json_obj['booth']['name']
with open(f"{name}.txt", 'w') as f:
    f.write(about_me)
