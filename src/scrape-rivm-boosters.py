import requests
import json
from bs4 import BeautifulSoup
import pandas as pd


page_url = 'https://www.rivm.nl/covid-19-vaccinatie/cijfers-vaccinatieprogramma'

req = requests.get(page_url)
req.raise_for_status()

soup = BeautifulSoup(req.text, 'html.parser')

item = soup.select_one('script[data-drupal-selector="drupal-settings-json"]').text
jsondata = json.loads(item)

keywords = ['Cumulatief', 'extra dosis']

chartdatas = []

for easychart_key, data in jsondata['easychart'].items():
    config = json.loads(data['config'])
    
    if 'title' in config and all([True if x in config['title']['text'] else False for x in keywords]):
        assert 'week' in config['xAxis'][0]['title']['text'].lower()
        data = config['series'][0]['data']
        
        chartdatas.append(data)
        
# make sure we only select one single chart
# if that is not the case the website has changed
assert len(chartdatas) == 1

df_boosters = pd.DataFrame(chartdatas[0])

assert df_boosters.columns.shape[0] == 2

df_boosters.columns = ['week', 'cumulative_number_of_booster1_shots']

df_boosters['date'] = df_boosters['week'].map(lambda x: pd.to_datetime(f'2021-{int(x)}-7', format='%G-%V-%u'))
df_boosters.set_index('date', inplace=True)
df_boosters.sort_index()

df_boosters.to_csv('booster-shots-immune-disorders.csv')
