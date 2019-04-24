from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import csv
domain = 'https://www.thoughtworks.com/radar/'
path = 'd:\\radar.csv'
urls = ['languages-and-frameworks','techniques','tools','platforms']
list_rows = [["name","ring","quadrant","isNew","description"]]
for url in urls:
    response = get(domain + url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    quadrant = html_soup.title.text.split(' | ')[0]
    
    platforms = html_soup.find("div", id = "quadrant-blip-list").find_all('div', recursive=False)
    
    for platform in platforms:
        ring = platform.get('id')
        lists = platform.find_all('li')
        for listItem in lists:
            name = listItem.find('span','blip-name').text
            isNew = "TRUE" if listItem.find('span', 'new-blip-marker') else "FALSE" 
            description = listItem.find('div','blip-description').p.decode_contents()
            row = [name, ring, quadrant, isNew, description]
            list_rows.append(row)
            
df = pd.DataFrame(list_rows)
header = df.iloc[0]
df = df[1:]
df.columns = header
df.head(100) 
df.to_csv(path, index=False)
