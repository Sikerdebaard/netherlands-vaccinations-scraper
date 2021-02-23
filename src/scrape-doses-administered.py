import pandas as pd
import requests


data = requests.get('https://coronadashboard.rijksoverheid.nl/json/NL.json')
data.raise_for_status()

for k, v in data.json().items():
    if 'vaccine_administered' in k:
        df = pd.DataFrame(data.json()[k]['values'])
        if 'date_unix' in df.columns:
            df = df.set_index('date_unix').astype(pd.Int64Dtype())
            df.index = pd.to_datetime(df.index, unit='s')
            df.index.rename('date', inplace=True)
            df.sort_index(inplace=True)

        df.to_csv(f'{k}.csv')
