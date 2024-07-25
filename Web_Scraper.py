import requests
from bs4 import BeautifulSoup
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Get URL from user
url = input("Enter the URL to scrape: ")

# Attempt to retrieve the URL
try:
    response = requests.get(url)
    # Checking Access
    if response.status_code == 200:
        print('Success')
    else:
        logging.error(f"Failed to retrieve the page. Status code: {response.status_code}")
        raise Exception("Error: Unable to access the webpage.")
except requests.exceptions.RequestException as e:
    logging.error(f"Request failed: {e}")
    raise SystemExit(e)

# Parse content
soup = BeautifulSoup(response.content, 'html.parser')

# Locate the data you want to scrape
headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
paragraphs = soup.find_all('p')
lists = soup.find_all(['ul', 'ol', 'li'])
meta = soup.find_all(['title', 'meta'])
links = soup.find_all('a', href=True)
tables = soup.find_all(['tr', 'th', 'td'])
forms = soup.find_all(['input', 'textarea', 'select', 'option'])
media = soup.find_all(['img', 'video', 'source', 'audio'])

data = []

for header in headers:
    data.append(['Headers', header.get_text().strip()])

for paragraph in paragraphs:
    data.append(['Paragraphs', paragraph.get_text().strip()])

for list_item in lists:
    data.append(['Lists', list_item.get_text().strip()])

for meta_tag in meta:
    if meta_tag.get('content'):
        data.append(['Meta', meta_tag['content']])
    else:
        data.append(['Meta', meta_tag.get_text().strip()])

for link in links:
    data.append(['Links', link['href']])

for table in tables:
    data.append(['Tables', table.get_text().strip()])

for form in forms:
    data.append(['Forms', form.get('name', 'Unnamed Form')])

for media_item in media:
    if media_item.name == 'img':
        data.append(['Images', media_item.get('src')])
    elif media_item.name == 'video':
        data.append(['Videos', media_item.get('src')])
    elif media_item.name == 'source':
        data.append(['Source', media_item.get('src')])
    elif media_item.name == 'audio':
        data.append(['Audio', media_item.get('src')])

# Export Data to File
with open('data.csv', "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Type", "Content"])
    for item in data:
        writer.writerow(item)

print("Data has been successfully scraped and saved to 'data.csv'.")
