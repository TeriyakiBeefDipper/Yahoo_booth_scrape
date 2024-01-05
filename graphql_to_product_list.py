"""
Chrome F12 -> Network -> graphql -> copy and paste to new json file
"""
import csv
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import os

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

base_dir = os.path.dirname(os.path.realpath(__file__))
images_dir = os.path.join(base_dir, 'images')
if not os.path.exists(images_dir):
    os.mkdir('images')


def extract_products_from_graphql(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'products':
                return value
            elif isinstance(value, (dict, list)):
                result = extract_products_from_graphql(value)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = extract_products_from_graphql(item)
            if result is not None:
                return result
    return None


# *Load and parse the JSON files
with open('graphql1.json', 'r') as file:
    graphql_data1 = json.load(file)
with open('graphql2.json', 'r') as file:
    graphql_data2 = json.load(file)

# *Extract 'products' from both files
products1 = extract_products_from_graphql(graphql_data1)
products2 = extract_products_from_graphql(graphql_data2)

# *Merge the product lists from both files
merged_products = products1 + products2 if products1 and products2 else []

# *go into each product link and parse info into csv file
csv_data = [['ID', 'Title', 'Price', 'Description', 'Hashtags']]
# count = 1
for product in merged_products:
    link = product.get('url')
    yahoo2 = requests.get(link, headers=header).text
    soup2 = BeautifulSoup(yahoo2, 'html.parser')
    data2 = soup2.find(id="isoredux-data").text
    pattern = r'window\.ISO_REDUX_DATA\s*=\s*(\{.*?\});'
    match = re.search(pattern, data2, re.DOTALL)
    if match:
        json_string = match.group(1)
    else:
        json_string = None
    # print(count, json_string)
    json_obj2 = json.loads(json_string)
    p_set = json_obj2["item"]
    p_id = p_set["id"]
    p_title = p_set["title"]
    p_price = p_set["price"]
    p_description = p_set["description"]
    p_description = BeautifulSoup(p_description, 'html.parser')
    p_description = ' '.join(p_description.stripped_strings)
    p_hashtags = p_set["hashtags"]
    csv_data.append([p_id, p_title, p_price, p_description, p_hashtags])
    # print(count)
    # print(p_id)
    # print(p_title)
    # print(p_price)
    # print(p_hashtags)
    # print(p_description)
    # print()
    # count += 1
    # *Process images links and download to /images directory
    img_sets = p_set["oImage"]
    count = 1
    for i in img_sets:
        indi_img = i["origin"]["url"]
        response = urllib.request.urlopen(indi_img)
        img_path = os.path.join(images_dir, f'{p_id}-{count}.jpg')
        with open(img_path, 'wb') as file:
            file.write(response.read())
        count += 1

# *Output the csv object to file
# with open("product_list.csv", mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(csv_data)
