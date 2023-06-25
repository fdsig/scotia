import numpy as np
import pandas as pd
import requests 
import json
import webbrowser
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import zipfile
import copy
import json
import time
from tqdm import tqdm

def get_prices(po=None):
    url = 'https://scotlis.ros.gov.uk/results?searchType=prices&postcode='
    url += f'{po[0]}+{po[1]}&sortBy=address&sortDir=asc'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4)'
    user_agent += ' AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'
    headers = {'User-Agent': user_agent} 
    try:
        req = requests.get(url,headers=headers,timeout=20).text
    except:
        print(f'{po} timed_out')
        return {'dates': None }
    soup = BeautifulSoup(req, 'html.parser')
    dates = [table.text for table in soup.find_all('td',headers='date')]
    address = [table.text for table in soup.find_all('td',headers='address')]
    prices = [table.text.strip('£').replace(',','') for table in soup.find_all('td',headers='price')]
    prices = [0 if not p.isnumeric() else int(p) for p in prices]
    return  {'dates':dates,'address':address,'prices':prices,'url':url}
def get_post_codes():
    df_pc = pd.read_csv('post_codes.csv/LargeUser.csv',low_memory=False)
    post_codes = list(set(df_pc['Postcode'].values))
    post_codes.sort()
    return [code.split(' ') for code in post_codes]

po_codes = get_post_codes()
rands = iter(np.random.uniform(0.01,0.1,len(po_codes)))
all_prices = { }
for code in tqdm(po_codes):
    time.sleep(next(rands))
    data = get_prices(code)
    key = f'{code[0]} {code[1]}'
    if data['dates']:
        all_prices[key]=data
        with open('scotland_house_prices_0.json','w') as handl:
            json.dump(all_prices,handl)
