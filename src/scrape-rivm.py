import pandas as pd
import requests
from bs4 import BeautifulSoup
import dateparser
from pathlib import Path


req = requests.get('https://www.rivm.nl/covid-19-vaccinatie/cijfers-vaccinatieprogramma')
req.raise_for_status()

page = req.text

soup = BeautifulSoup(page)

for h2 in soup.find_all('h2'):
    if 'Vaccinatiecijfers' in h2.text and 't/m' in h2.text:
        date = dateparser.parse(h2.text.split('t/m', 1)[1].strip(), languages=['nl']).date()
        break  # break loop, no need to continue

table = soup.find_all('table')[0]
[el.decompose() for el in table.find_all('span')]  # remove span tags in the table, they mess up pandas read_html


df_doses_per_manufacturer = pd.read_html(str(table), thousands='.', decimal=',')[0]

df_doses_per_manufacturer = df_doses_per_manufacturer.pivot_table(index='Doelgroep', values=['Eerste dosis', 'Tweede dosis'], columns='Vaccin').astype(pd.Int64Dtype()).T.reset_index()
df_doses_per_manufacturer.rename(columns={'level_0': 'Dosis'}, inplace=True)
df_doses_per_manufacturer['date'] = pd.to_datetime(date)
df_doses_per_manufacturer.set_index('date', inplace=True)

outfile = Path('doses-administered-per-manufacturer.csv')

if outfile.exists():
    df_original = pd.read_csv(outfile, index_col=0)
    df_original.index = pd.to_datetime(df_original.index)
    
    for col in df_original.columns:
        if col not in ['Dosis', 'Vaccin']:
            df_original[col] = df_original[col].astype(pd.Int64Dtype())

    if df_doses_per_manufacturer.index[0] in df_original.index:
        df_original = df_original[~(df_original.index == df_doses_per_manufacturer.index[0])]

    df_doses_per_manufacturer = pd.concat([df_original, df_doses_per_manufacturer])

df_doses_per_manufacturer.sort_index(inplace=True)

df_doses_per_manufacturer.to_csv(outfile)
