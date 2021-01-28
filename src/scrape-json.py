import requests
import pandas as pd


data = requests.get('https://coronadashboard.rijksoverheid.nl/json/NL.json').json()
df = pd.DataFrame(data['vaccine_delivery']['values'])
for col in df.columns:
    if 'date' in col:
        df[col] = pd.to_datetime(df[col], unit='s')
    else:
        df[col] = df[col].astype(int)
        
#df = df.set_index('date_start_unix')
df['year-week'] = df['date_start_unix'].dt.strftime('%G-%V')
df = df.set_index('year-week')
df.to_csv('vaccine-dose-deliveries-by-manufacturer.csv')

