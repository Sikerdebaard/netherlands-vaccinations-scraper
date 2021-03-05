import pandas as pd
import requests
from pathlib import Path


data = requests.get('https://coronadashboard.rijksoverheid.nl/json/NL.json')
data.raise_for_status()

for k, v in data.json().items():
    if 'vaccine_administered' in k:
        df = pd.DataFrame(data.json()[k]['values'])
        out_file = Path(f'{k}.csv')
        if 'date_unix' in df.columns:
            df = df.set_index('date_unix').astype(pd.Int64Dtype())
            df.index = pd.to_datetime(df.index, unit='s')
            df.index.rename('date', inplace=True)
            df.sort_index(inplace=True)

            if out_file.exists():
                df_org = pd.read_csv(out_file, index_col=0)
                df_org.index = pd.to_datetime(df_org.index)

                for idx, row in df.iterrows():
                    for col in df.columns:
                        df_org.at[idx, col] = row[col]

                df = df_org


        df.sort_index(inplace=True)
        df.astype(pd.Int64Dtype()).to_csv(out_file)
