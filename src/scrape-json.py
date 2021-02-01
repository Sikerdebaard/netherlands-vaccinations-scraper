import requests
import pandas as pd
from pathlib import Path


data = requests.get('https://coronadashboard.rijksoverheid.nl/json/NL.json').json()
df = pd.DataFrame(data['vaccine_delivery']['values'])
for col in df.columns:
    if 'date' in col:
        df[col.replace('_unix', '')] = pd.to_datetime(df[col], unit='s')
        df.drop(columns=col, inplace=True)
    else:
        df[col] = df[col].astype(int)
        
df['year-week'] = df['date_start'].dt.strftime('%G-%V')
df = df.set_index('year-week')

outfile = Path('vaccine-dose-deliveries-by-manufacturer.csv')

if outfile.exists():
    df_org = pd.read_csv(outfile, index_col=0)

    for idx, row in df.iterrows():
        for col in df.columns:
            df_org.at[idx, col] = row[col]

    df = df_org


df.to_csv('vaccine-dose-deliveries-by-manufacturer.csv')

