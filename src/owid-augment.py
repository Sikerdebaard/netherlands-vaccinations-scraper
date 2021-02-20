import pandas as pd
import numpy as np

df_owid = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/79bc3c1a690454579ff275be34a347ab6125fb04/public/data/vaccinations/country_data/Netherlands.csv', index_col=['date'])
df_owid.index = pd.to_datetime(df_owid.index)

df_netherlands = pd.read_csv('vaccine_administered_total.csv', index_col=0)
df_netherlands['source'] = 'https://coronadashboard.rijksoverheid.nl/landelijk/vaccinaties'
df_netherlands.index = pd.to_datetime(df_netherlands.index)
df_netherlands.sort_index(inplace=True)

rename = {
    'source_url': 'source',
    'total_vaccinations': 'reported',
}
df_owid_mod = df_owid[rename.keys()].rename(columns=rename)
df_owid_mod['estimated'] = df_owid_mod['reported']
df_merged = pd.concat([df_netherlands, df_owid_mod[df_owid_mod.index < df_netherlands.index[0]]])
df_merged.sort_index(inplace=True)

df_merged = df_merged[['reported', 'estimated', 'source']]

df_merged.to_csv('augmented/doses_administered_raw.csv')

for col in ['reported', 'estimated']:
    df_diff = df_merged[col].diff()
    df_merged.loc[df_merged.index.isin(df_diff[df_diff < 0].index), col] = np.nan
    df_merged[col] = df_merged[col].astype(pd.Int64Dtype())
                                   
df_merged.to_csv('augmented/doses_administered_cumulative.csv')
