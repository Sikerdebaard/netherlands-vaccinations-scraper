import re
import json
import dateparser
import requests
import pandas as pd
from datetime import datetime, date
from pathlib import Path
from bs4 import BeautifulSoup


baseurl = 'https://coronadashboard.rijksoverheid.nl'
page = requests.get(baseurl + '/landelijk/vaccinaties')
soup = BeautifulSoup(page.text, 'html.parser')


administered_by_mapper = {
    "ggd'en": 'GGD',
    'ziekenhuizen': 'Hospitals',
    'langdurige zorginstellingen': 'Long-term Care Facilities',
}

def dict_to_csv(d, file):
    df = pd.DataFrame(d, index=[0])
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    
    if Path(file).exists():
        df_org = pd.read_csv(file, index_col=0)
        df_org.index = pd.to_datetime(df_org.index)
        
        for idx, row in df.iterrows():
            #if idx in df_org.index:
            for col in df.columns:
                df_org.at[idx, col] = row[col]
                    
        df = df_org
    
    df.sort_index(inplace=True)
    df.to_csv(file)

def parse_administered_doses(el):
    data_doses = {}
    data_doses_by_administering_instance = {}
    
    data_doses['total_vaccinations'] = int(el.select('[class*="kpi-value_"]')[0].text.replace('.', ''))
    
    for h4 in el.find_all('h4'):
        if 'toegediend door' in h4.text:
            amount = int(h4.find('span').text.replace('.', ''))
            administered_by = h4.text.split('toegediend door')[1].strip().rstrip('*')
            
            if administered_by.lower() in administered_by_mapper:
                administered_by = administered_by_mapper[administered_by.lower()]
            
            data_doses_by_administering_instance[administered_by] = amount
            
    for p in el.find_all('p'):
        if 'Waarde van' in p.text:
            date = ' '.join(p.text.split('van', 1)[1].strip().split(' ')[:3])
            date = dateparser.parse(date, languages=["nl"]).date()
            data_doses_by_administering_instance['date'] = date
            data_doses['date'] = date
    
    dict_to_csv(data_doses, 'people-vaccinated.csv')
    dict_to_csv(data_doses_by_administering_instance, 'people-vaccinated-by-instance.csv')
    

def parse_expected_delivery_vaccins(el):
    data = {}
    
    data['expected_deliveries_within_six_weeks'] = int(el.select('[class*="kpi-value_"]')[0].text.replace('.', ''))
    
    for p in el.find_all('p'):
        if 'Waarde van' in p.text:
            date = ' '.join(p.text.split('van', 1)[1].strip().split(' ')[:3])
            date = dateparser.parse(date, languages=["nl"]).date()
            data['date'] = date
    
    dict_to_csv(data, 'expected-doses-delivered-within-six-weeks.csv')

def parse_expected_deliveries_per_week(el):
    return {}


mapper = {
    'Aantal toegediende vaccins': parse_administered_doses,
    'Verwachte levering goedgekeurde vaccins': parse_expected_delivery_vaccins,
    #'Verwachte leveringen per week': parse_expected_deliveries_per_week,
}

for p in soup.find_all('p'):
    if 'Laatste waardes verkregen op' in p.text:
        date = ' '.join(p.text.split('.')[0].split('op')[1].strip().split(' ')[:3])
        date = dateparser.parse(date, languages=["nl"]).date()
        
for article in soup.find_all('article'):
    for h3 in article.find_all('h3'):
        key = h3.text.strip()
        if key in mapper:
            mapper[key](article)
